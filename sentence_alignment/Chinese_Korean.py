import sentence_alignment.Globals as Globals


def korean_paragraph_segment(file_name, is_file=True):
    if is_file:
        try:
            file = open(file_name, 'r', encoding='EUC-KR')
            paragraphs = []
            for line in file:
                paragraphs.append(line.strip())
            file.close()
            return paragraphs
        except:
            return []
    else:
        return file_name.split('\n')


def korean_sentence_segment(paragraph):
    words = paragraph.split(' ')
    for i in range(len(words)):
        if words[i].endswith('.') or words[i].endswith('.\"') or words[i].endswith('!'):
            words[i] = words[i] + '\n'
        elif words[i].endswith('!\"') or words[i].endswith('?') or words[i].endswith('?\"'):
            words[i] = words[i] + '\n'
    paragraph = ' '.join(words)
    if paragraph[-1] == '\n':
        paragraph = paragraph[:-1]
    return paragraph.split('\n')


def pip_line(source, target, is_file=True):
    source_para = korean_paragraph_segment(source, is_file)
    # print(source_para)
    if len(source_para) == 0:
        return []
    target_para = Globals.chinese_paragraph_segment(target, is_file)
    #print(target_para)
    if len(target_para) == 0:
        return None
    save_content = []
    for i in range(len(source_para)):
        source_sentence = korean_sentence_segment(source_para[i])
        target_sentence = Globals.chinese_sentence_segment(target_para[i])
        if target_sentence is None:
            return None
        save_content.append(Globals.chinese_efgrs(source_sentence, target_sentence))
    return save_content


def write_into_file(aligned_sentence, output_file):
    f = open(output_file, 'w', encoding='utf-8')
    for sentences in aligned_sentence:
        for line in sentences:
            f.write(line.strip() + '\n')
        f.write('\n')
    f.close()


if __name__ == '__main__':
    save = pip_line('source7.txt', 'target7.txt')
    write_into_file(save, 'output.txt')