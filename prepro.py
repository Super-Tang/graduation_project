zh_file = open('D:\\corpus\\en-zh\\MultiUN.en-zh.zh', 'r', encoding='utf-8')
en_file = open('D:\\corpus\\en-zh\\MultiUN.en-zh.en','r', encoding='utf-8')
train_zh = open("D:\\corpus\\en-zh\\train.zh", 'w', encoding='utf-8')
train_en = open("D:\\corpus\\en-zh\\train.en", 'w', encoding='utf-8')
test_zh = open("D:\\corpus\\en-zh\\test.zh", 'w', encoding='utf-8')
test_en = open("D:\\corpus\\en-zh\\test.en", 'w', encoding='utf-8')
count = 0
while count < 5000000:
    line1 = zh_file.readline()
    line2 = en_file.readline()
    train_zh.write(line1)
    train_en.write(line2)
    count += 1
while count < 5001000:
    line1 = zh_file.readline()
    line2 = en_file.readline()
    test_zh.write(line1)
    test_en.write(line2)
    count += 1
zh_file.close()
en_file.close()
train_en.close()
train_zh.close()
test_en.close()
test_zh.close()