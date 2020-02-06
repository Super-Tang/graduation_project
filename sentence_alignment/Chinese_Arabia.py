import sentence_alignment.Globals as Globals


def arabic_paragraph_segment(file_name, is_file=True):
    if is_file:
        try:
            file = open(file_name, 'r', encoding='utf-8')
            paragraphs = []
            for line in file:
                paragraphs.append(line.strip())
            file.close()
        #paragraphs.reverse()
            return paragraphs
        except:
            return []
    else:
        return file_name.split("\n")


def arabic_sentence_segment(paragraph):
    words = paragraph.split(' ')
    # print(words)
    for i in range(len(words)):
        if words[i].endswith('.') or words[i].endswith('!') or words[i].endswith('!'):
            words[i] = words[i] + '\n'
        elif words[i].endswith('!\"') or words[i].endswith('?') or words[i].endswith('?\"'):
            words[i] = words[i] + '\n'
    paragraph = ' '.join(words)
    if paragraph[-1] == '\n':
        paragraph = paragraph[:-1]
    return paragraph.split('\n')


def chinese_arabic(source, target):
    save_content = []
    if len(source) == len(target):
        #print('length equal')
        for i in range(len(source)):
            save_content.append(source[i])
            save_content.append(target[i])
        return save_content
    elif len(source) > len(target):
        current_index = 0
        for i in range(len(target)):
            if current_index >= len(source):
                last_chinese = save_content[-1]
                save_content.remove(last_chinese)
                last_japan = save_content[-1]
                save_content.remove(last_japan)
                j = i
                while j < len(source):
                    last_japan += source[j]
                    j += 1
                save_content.append(last_japan)
                save_content.append(last_chinese)
                break
            if i == len(source) - 1 and current_index < len(target):
                save_content.append(source[i])
                last_chinese = ''
                while current_index < len(target):
                    last_chinese += target[current_index]
                    current_index += 1
                save_content.append(last_chinese)
                break
            else:
                if 0.3 <= (len(source[current_index].split())) / len(target[i]) <= 0.9:
                    save_content.append(source[current_index].strip())
                    save_content.append(target[i])
                    current_index += 1
                elif current_index + 1 < len(target) and 0.6 <= (len(source[current_index].split())
                        + len(source[current_index+1].split())) / (len(target[i])) <= 1.2:
                    temp_sentence = source[current_index].strip() + source[current_index + 1].strip()
                    save_content.append(temp_sentence)
                    save_content.append(target[i])
                    current_index += 2
                else:
                    if current_index + 2 < len(source):
                        save_content.append(source[current_index].strip() + source[current_index + 1].strip()
                                            + source[current_index + 2].strip())
                        save_content.append(target[i])
                        current_index += 3
                    elif current_index + 2 == len(source):
                        save_content.append(source[current_index].strip() + source[current_index + 1].strip())
                        save_content.append(target[i])
                        current_index += 2
                    else:
                        save_content.append(source[current_index])
                        save_content.append(target[i])
                        current_index += 1
    else:
        current_index = 0
        for i in range(len(source)):
            if current_index >= len(target):
                last_chinese = save_content[-1]
                save_content.remove(last_chinese)
                last_japan = save_content[-1]
                save_content.remove(last_japan)
                j = i
                while j < len(source):
                    last_japan += source[j]
                    j += 1
                save_content.append(last_japan)
                save_content.append(last_chinese)
                break
            if i == len(source) - 1 and current_index < len(target):
                save_content.append(source[i])
                last_chinese = ''
                while current_index < len(target):
                    last_chinese += target[current_index]
                    current_index += 1
                save_content.append(last_chinese)
                break
            else:
                if 0.3 <= (len(source[i].split())) / len(target[current_index]) <= 0.9:
                    save_content.append(source[i].strip())
                    save_content.append(target[current_index])
                    current_index += 1
                elif current_index + 1 < len(target) and 0.4 <= len(source[i].split()) / \
                        (len(target[current_index]) + len(target[current_index + 1])) <= 1.4:
                    temp_sentence = target[current_index] + target[current_index + 1]
                    save_content.append(source[i])
                    save_content.append(temp_sentence)
                    current_index += 2
                else:
                    if current_index + 2 < len(target):
                        save_content.append(source[i])
                        save_content.append(target[current_index].strip() + target[current_index + 1].strip()
                                            + target[current_index + 2].strip())
                        current_index += 3
                    elif current_index + 2 == len(target):
                        save_content.append(source[i])
                        save_content.append(target[current_index].strip() + target[current_index + 1].strip())
                        current_index += 2
                    else:
                        save_content.append(source[i])
                        save_content.append(target[current_index])
                        current_index += 1
    return save_content


def pip_line(source, target, is_file=True):
    source_para = arabic_paragraph_segment(source, is_file)
    #print(source_para)
    if len(source_para) == 0:
        return []
    target_para = Globals.chinese_paragraph_segment(target, is_file)
    #print(target_para)
    if len(target_para) == 0:
        return None
    save_content = []
    for i in range(len(source_para)):
        source_sentence = arabic_sentence_segment(source_para[i])
        target_sentence = Globals.chinese_sentence_segment(target_para[i])
        if target_sentence is None:
            return None
        save_content.append(chinese_arabic(source_sentence, target_sentence))
    return save_content


def write_into_file(aligned_sentence, output_file):
    f = open(output_file, 'w', encoding='utf-8')
    for sentences in aligned_sentence:
        for line in sentences:
            #print(line)
            f.write(line.strip() + '\n')
        f.write('\n')
    f.close()


if __name__ == '__main__':
   savecontent = pip_line("source10.txt", "target10.txt")
   write_into_file(savecontent, 'output.txt')