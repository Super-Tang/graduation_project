import re
English_Sentence_End_One = ['.', '!', '?']
English_Sentence_End_Two = ['.\'', '.\"', '!\'', '!\"', '?\'', '?\"']
Fake_Ending_Label = ['...']
Number_Pattern = re.compile('\d+')
CHINESE = 0
ENGLISH = 1
FRENCH = 2
GERMAN = 3
RUSSIAN = 4
JAPAN = 5
ARABIA = 6
KOREAN = 7
SPAIN = 8
PORTUGAL = 9


def chinese_paragraph_segment(file_name,  is_file, count=0):
    if is_file:
        try:
            if count == 0:
                file = open(file_name, 'r', encoding='gbk')
            elif count == 1:
                file = open(file_name, 'r', encoding='utf-8')
            else:
                return []
            paragraphs = []
            for line in file:
                paragraphs.append(line.strip())
            file.close()
            return paragraphs
        except:
            count += 1
            return chinese_paragraph_segment(file_name,is_file, count)
    else:
        #print(len(file_name.split('\n')))
        return file_name.split('\n')


def chinese_sentence_segment(paragraph):
    paragraph1 = paragraph
    paragraph = re.sub('([。！？?])([^”’])', r"\1\n\2", paragraph)
    paragraph = re.sub('(…{2})([^”’])', r"\1\n\2", paragraph)
    paragraph = re.sub('([。！？?][”’])([^，。！？?])', r'\1\n\2', paragraph)
    paragraph = paragraph.rstrip()
    if '。' in paragraph or '！' in paragraph or '？' in paragraph or '：' in paragraph or '，' in paragraph:
        return paragraph.split('\n')
    elif paragraph1 == paragraph:
        return paragraph.split('\n')
    else:
        return None


def efgrs_paragraph_segment(file_name, is_file):
    if is_file:
        try:
            file = open(file_name, 'r', encoding='utf-8')
            paragraphs = []
            for line in file:
                paragraphs.append(line.strip())
            file.close()
            return paragraphs
        except:
            return []
    else:
        #print(len(file_name.split('\n')))
        return file_name.split('\n')


def efgrs_sentence_segment(paragraph):
    words = paragraph.split(' ')
    for i in range(len(words)):
        if len(words[i]) > 0 and words[i][-2:] in English_Sentence_End_Two:
            words[i] = words[i] + '\n'
        elif len(words[i]) > 0 and words[i][-1] in English_Sentence_End_One and \
                words[i] not in Fake_Ending_Label:
            words[i] = words[i] + '\n'
    paragraph = " ".join(words)
    if paragraph[-1] == '\n':
        paragraph = paragraph[:-1]
    return paragraph.split('\n')


def chinese_efgrs(efgrs, chinese):
    #print(len(efgrs), len(chinese))
    aligned_sentences = []
    if len(efgrs) == len(chinese):
        for i in range(len(efgrs)):
            aligned_sentences.append(efgrs[i])
            aligned_sentences.append(chinese[i])
    elif len(efgrs) > len(chinese):
        current_index = 0
        for i in range(len(chinese)):
            if current_index >= len(efgrs):
                last_chinese = aligned_sentences[-1]
                aligned_sentences.remove(last_chinese)
                j = i
                while j < len(chinese):
                    last_chinese += chinese[j]
                    j += 1
                aligned_sentences.append(last_chinese)
                break
            if i == len(chinese) - 1 and current_index < len(efgrs):
                last_efgrs = ''
                while current_index < len(efgrs):
                    last_efgrs += efgrs[current_index]
                    current_index += 1
                aligned_sentences.append(last_efgrs)
                aligned_sentences.append(chinese[i])
                break
            chinese_result = Number_Pattern.search(chinese[i])
            efgrs_result = Number_Pattern.search(efgrs[current_index])
            if chinese_result is not None:
                anchor = chinese_result.group()
                current_index1 = current_index
                s = ''
                while efgrs_result is None and current_index1 - current_index <= 2:
                    current_index1 += 1
                    efgrs_result = Number_Pattern.search(efgrs[current_index1])
                    if efgrs_result is not None and anchor == efgrs_result.group():
                        s = efgrs[current_index]
                        j = current_index
                        while j <= current_index1:
                            s += efgrs[j]
                            j += 1
                        aligned_sentences.append(s)
                        aligned_sentences.append(chinese[i])
                if len(s) == 0:
                    aligned_sentences.append(efgrs[current_index])
                    aligned_sentences.append(chinese[i])
                    current_index += 1
                else:
                    current_index = current_index1
            else:
                if 0.4 <= (len(efgrs[current_index].split()) + 0.0) / len(chinese[i]) <= 0.9:
                    aligned_sentences.append(efgrs[current_index])
                    aligned_sentences.append(chinese[i])
                    current_index += 1
                elif current_index + 1 < len(efgrs) and 0.4 <= (len(efgrs[current_index].split()) +
                            len(efgrs[current_index + 1].split()) + 0.0) / len(chinese[i]) <= 1.2:
                    aligned_sentences.append(efgrs[current_index] + efgrs[current_index + 1])
                    aligned_sentences.append(chinese[i])
                    current_index += 2
                else:
                    if current_index + 2 < len(efgrs):
                        aligned_sentences.append(efgrs[current_index] + efgrs[current_index + 1] + efgrs[current_index + 2])
                        aligned_sentences.append(chinese[i])
                        current_index += 3
                    elif current_index + 2 == len(efgrs):
                        aligned_sentences.append(efgrs[current_index] + efgrs[current_index + 1])
                        aligned_sentences.append(chinese[i])
                        current_index += 2
                    else:
                        aligned_sentences.append(efgrs[current_index])
                        aligned_sentences.append(chinese[i])
                        current_index += 1
    else:
        current_index = 0
        for i in range(len(efgrs)):
            #print(i, current_index, len(chinese))
            if current_index >= len(chinese):
                last_chinese = aligned_sentences[-1]
                aligned_sentences.remove(last_chinese)
                last_efgrs = aligned_sentences[-1]
                aligned_sentences.remove(last_efgrs)
                j = i
                while j < len(efgrs):
                    last_efgrs += efgrs[j]
                    j += 1
                aligned_sentences.append(last_efgrs)
                aligned_sentences.append(last_chinese)
                break
            if i == len(efgrs) - 1 and current_index < len(chinese):
                aligned_sentences.append(efgrs[i])
                last_chinese = ''
                while current_index < len(chinese):
                    last_chinese += chinese[current_index]
                    current_index += 1
                aligned_sentences.append(last_chinese)
                break
            chinese_result = Number_Pattern.search(chinese[current_index])
            efgrs_result = Number_Pattern.search(efgrs[i])
            if efgrs_result is not None:
                anchor = efgrs_result.group()
                current_index1 = current_index
                s = ''
                while chinese_result is None and current_index1 - current_index <= 2:
                    #print(current_index1)
                    current_index1 += 1
                    if current_index1 >= len(chinese):
                        break
                    chinese_result = Number_Pattern.search(chinese[current_index1])
                    if chinese_result is not None and anchor == chinese_result.group():
                        s = chinese[current_index]
                        j = current_index
                        while j <= current_index1:
                            s += efgrs[j]
                            j += 1
                        aligned_sentences.append(efgrs[i])
                        aligned_sentences.append(s)
                #print(s + "cnjanvfjaf")
                if len(s) == 0:
                    aligned_sentences.append(efgrs[i])
                    aligned_sentences.append(chinese[current_index])
                    current_index += 1
                else:
                    current_index = current_index1
            else:
                if 0.4 <= (len(efgrs[i].split()) + 0.0) / len(chinese[current_index]) <= 1.2:
                    aligned_sentences.append(efgrs[i].strip())
                    aligned_sentences.append(chinese[current_index])
                    current_index += 1
                elif current_index + 1 < len(chinese) and 0.4 <= (len(efgrs[i].split()) + 0.0) / \
                        (len(chinese[current_index]) + len(chinese[current_index + 1].split())) <= 1.2:
                    temp_sentence = chinese[current_index] + chinese[current_index + 1]
                    aligned_sentences.append(efgrs[i])
                    aligned_sentences.append(temp_sentence)
                    current_index += 2
                else:
                    aligned_sentences.append(efgrs[i])
                    aligned_sentences.append(chinese[current_index])
                    current_index += 1
    return aligned_sentences


def pip_line(source, target, is_file):
    #print(is_file)
    source_para = efgrs_paragraph_segment(source, is_file)
    #print(source_para)
    if len(source_para) == 0:
        return []
    target_para = chinese_paragraph_segment(target, is_file)
    #print(target_para)
    if len(target_para) == 0:
       # print("here")
        return None
    if len(source_para) != len(target_para):
        return None
    save_content = []
    for i in range(len(source_para)):
        # print(i, source_para[i])
        # print(i, target_para[i])
        source_sentence = efgrs_sentence_segment(source_para[i])
        target_sentence = chinese_sentence_segment(target_para[i])
        # print(source_sentence)
        # print(target_sentence)
        if target_sentence is None:
            return None
        save_content.append(chinese_efgrs(source_sentence, target_sentence))
    #print(save_content)
    return save_content

