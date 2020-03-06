import heapq
import time
import numpy as np
import threading
import inspect
import ctypes
from phrase_alignment.predict_thread import Predict_thread
from phrase_alignment.source_node import source_node
from phrase_alignment.target_node import target_node
from phrase_alignment.text_node import text_node
import random
chinese_pun = ['！', '？', '｡', '：', '；', '，', '!', ',', '?']


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

# TODO 去除source_words 中的字节码 'b\'\\xe2\\x96\\x81\''
def process_source(source):
    source_segs = source.split()
    source_nodes = []
    node_index = 0
    for seg in source_segs:
        node = source_node(node_index)
        if str(seg[0].encode()) == 'b\'\\xe2\\x96\\x81\'':
            seg = seg[1:]
            node.set_text(seg)
        else:
            node.set_text(seg)
            source_nodes[node_index - 1].alter_tag()
        source_nodes.append(node)
        node_index += 1
    return source_nodes


# TODO 去除target_words 中的字节码 'b\'\\xe2\\x96\\x81\''
def process_target(target):
    target_segs = target.split()
    target_nodes = []
    node_index = 0
    for seg in target_segs:
        node = target_node(node_index)
        if str(seg[0].encode()) == 'b\'\\xe2\\x96\\x81\'':
            # print(seg[0])
            seg = seg[1:]
            node.set_text(seg)
        else:
            node.set_text(seg)
            if seg[0] in chinese_pun:
                node.alter_pun()
        node_index += 1
        target_nodes.append(node)
    return target_nodes


# TODO 去除attention_matrix中的最后一行和每一行的最后一列
# 这两部分分别为source_sentence和target_sentence中的<eos>部分
def process_matrix(matrix):
    matrix = matrix[1]
    filter_matrix = []
    for line in matrix:
        # print(line)
        line = line[0:-1]
        filter_matrix.append(line)
    filter_matrix = filter_matrix[0:-1]
    return filter_matrix


# TODO 根据处理后的attention_matrix确定与每一个source_word对齐的target_word位置
def source_word_align(source, target, weights):
    # print(len(source), len(weights), len(target), len(weights[0]))
    assert len(source) == len(weights) and len(target) == len(weights[0])
    for i in range(len(source)):
        a = list(weights[i])
        # print(a)
        max_index = list(map(a.index, heapq.nlargest(2, a)))[0]
        shortlist = list(map(a.index, heapq.nlargest(2, a)))[1]
        source[i].set_align_index(max_index)
        source[i].set_shortlist(shortlist)
    return source


# TODO 根据处理后的attention_matrix确定与每一个target_word对齐的source_word位置
def target_word_align(source, target, weights):
    assert len(source) == len(weights) and len(target) == len(weights[0])
    weights = np.array(weights).transpose()
    for i in range(len(target)):
        a = list(weights[i])
        max_index = list(map(a.index, heapq.nlargest(2, a)))[0]
        shortlist = list(map(a.index, heapq.nlargest(2, a)))[1]
        target[i].set_align_index(max_index)
        target[i].set_shortlist(shortlist)
    return target


# TODO 根据都已经单向对齐的source_words和target_words合成对齐的短语,对齐的短语设置相同的颜色编号
def phrase_alignment(source, target):
    color_index = 0
    # 第一次遍历 source 寻找双向对齐节点 并设置相同颜色
    for node in source:
        if node.color_index != -1:
            continue
        align_target_index = node.align_target_index
        node_index = node.node_index
        left_source_node = None
        if node_index > 0:
            left_source_node = source[node_index -1]
        if target[align_target_index].align_source_index == node_index:
            # 如果该source左端和该target已经对齐 则将颜色设置为与左端相同
            if left_source_node is not None and ((left_source_node.align_target_index == align_target_index - 1 and
                                                  left_source_node.node_index == target[align_target_index - 1].align_source_index) or
                                                 (len(target) > align_target_index + 1 == left_source_node.align_target_index
                 and target[align_target_index + 1].align_source_index == left_source_node.node_index)):
                left_color_index = left_source_node.color_index
                node.set_color(left_color_index)
                target[align_target_index].set_color(left_color_index)
                while node.has_next:
                    next_node_index = node.node_index + 1
                    node = source[next_node_index]
                    node.set_color(left_color_index)
            else:
                node.set_color(color_index)
                target[align_target_index].set_color(color_index)
                while node.has_next:
                    next_node_index = node.node_index + 1
                    node = source[next_node_index]
                    node.set_color(color_index)
                color_index += 1
    # 第二次遍历 source 寻找单向对齐节点 并设置颜色
    for node in source:
        if node.color_index == -1: # 没有对齐节点
            node_index = node.node_index
            align_target_index = node.align_target_index
            left_source_node = None
            right_source_node = None
            if node_index > 0:
                left_source_node = source[node_index - 1]
            if node_index < len(source) - 1:
                right_source_node = source[node_index + 1]
            if target[align_target_index].shortlist == node_index:
                node.set_color(target[align_target_index].color_index)
                while node.has_next:
                    next_node_index = node.node_index + 1
                    node = source[next_node_index]
                    node.set_color(target[align_target_index].color_index)
            elif left_source_node is not None and left_source_node.color_index == target[align_target_index].color_index:
                node.set_color(target[align_target_index].color_index)
                while node.has_next:
                    next_node_index = node.node_index + 1
                    node = source[next_node_index]
                    node.set_color(target[align_target_index].color_index)
            elif right_source_node is not None and right_source_node.color_index == target[align_target_index].color_index:
                node.set_color(target[align_target_index].color_index)
                while node.has_next:
                    next_node_index = node.node_index + 1
                    node = source[next_node_index]
                    node.set_color(target[align_target_index].color_index)
    # 第三次遍历 target 寻找单向对齐节点 并设置颜色
    for node in target:
        if node.color_index == -1:
            node_index = node.node_index
            align_source_index = node.align_source_index
            left_target_node = None
            right_target_node = None
            if node_index > 0:
                left_target_node = target[node_index - 1]
            if node_index < len(target) - 1:
                right_target_node = target[node_index + 1]
            if source[align_source_index].shortlist == node_index:
                node.set_color(source[align_source_index].color_index)
            elif left_target_node is not None and left_target_node.color_index == source[align_source_index].color_index:
                node.set_color(source[align_source_index].color_index)
            elif right_target_node is not None and right_target_node.color_index == source[align_source_index].color_index:
                node.set_color(source[align_source_index].color_index)
    # 最后抽取出短语
    source_sentence = []
    target_sentence = []
    text = ''
    source_colors = []
    target_colors = []
    add_flag = False
    # 根据设置的颜色抽取source_sentence中的短语
    for node in source:
        add_flag = False
        if text == '':
            text = text + node.text
        else:
            if node.color_index == source[node.node_index - 1].color_index:
                if source[node.node_index - 1].has_next:
                    text = text + node.text
                else:
                    text = text + ' ' + node.text
            elif node.color_index == -1 and node.node_index + 1 < len(source) and source[node.node_index + 1].color_index == source[node.node_index - 1].color_index:
                node.set_color(source[node.node_index + 1].color_index)
                text = text + ' ' + node.text
            else:
                color_index = source[node.node_index - 1].color_index
                source_sentence.append(text_node(text, color_index))
                add_flag = True
                source_colors.append(color_index)
                text = node.text
    if not add_flag:
        source_sentence.append(text_node(text, source[-1].color_index))
        source_colors.append(source[-1].color_index)
    text = ''
    add_flag = False
    # 根据设置的颜色抽取target_sentence中的短语
    for node in target:
        add_flag = False
        if text == '':
            text = text + node.text
        else:
            if node.color_index == target[node.node_index - 1].color_index:
                text = text + node.text
            elif node.is_pun:
                text = text + node.text
            else:
                color_index = target[node.node_index - 1].color_index
                if color_index not in source_colors:
                    color_index = -1
                target_colors.append(color_index)
                target_sentence.append(text_node(text, color_index))
                add_flag = True
                text = node.text
    # 修改在source_sentence中出现, 但在target_sentence中没有出现的颜色
    rand_number = random.randint(1, 10)
    if not add_flag:
        color_index = target[-1].color_index
        if color_index not in source_colors:
            color_index = -1
        target_sentence.append(text_node(text, color_index))
        if color_index != -1:
            target_colors.append(color_index)

    for node in source_sentence:
        if node.color not in target_colors:
            node.color = -1
        else:
            node.color += rand_number
    for node in target_sentence:
        if node.color != -1:
            node.color += rand_number
    # 转换成元组返回
    source_phrases = [node.to_text() for node in source_sentence]
    target_phrases = [node.to_text() for node in target_sentence]
    return source_phrases, target_phrases


def write_weights(weight):
    file = open('weights.txt', 'w', encoding='utf-8')
    for line in weight:
        s = ''
        for w in line:
            s = s + '\t' + str(w)
        file.write(s + '\n')
    file.close()


class phrase_extract(threading.Thread):
    def __init__(self, language, args):
        threading.Thread.__init__(self)
        self.language = language
        self.finished = False
        self.started = False
        self.values = []
        self.args = args

    def run(self):
        self.started = True
        self.finished = False
        predicting_thread = Predict_thread(self.args)
        predicting_thread.start()
        while not predicting_thread.done:
            # print('here')
            time.sleep(0.1)
        test_file = open(self.args.predict_file, 'r', encoding='utf-8')
        sentences = []
        for line in test_file:
            line = line.strip().split('\t')
            # print(line)
            sentences.append({'src': line[1], 'trg': line[0]})
        for (sentence, weights) in zip(sentences, predicting_thread.weights):
            sources = sentence['src']
            targets = sentence['trg']
            source_nodes = process_source(sources)
            target_nodes = process_target(targets)
            weight = process_matrix(weights)
            source_word_alignments = source_word_align(source_nodes, target_nodes, weight)
            target_word_alignments = target_word_align(source_nodes, target_nodes, weight)
            s, t = phrase_alignment(source_word_alignments, target_word_alignments)
            self.values.append(s)
            self.values.append(t)
        test_file.close()
        self.finished = True
