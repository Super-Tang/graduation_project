f = open('D:\\corpus\\fr-zh\\MultiUN.fr-zh.fr', 'r', encoding='utf-8')
f1 = open('D:\\corpus\\fr-zh\\MultiUN.fr-zh.zh', 'r', encoding='utf-8')
f2 = open('C:\\Users\\Super-Tang\\Desktop\\de1.txt', 'w', encoding='utf-8')
f3 = open('C:\\Users\\Super-Tang\\Desktop\\zh1.txt', 'w', encoding='utf-8')
count = 0
for line in f:
    line1 = f1.readline()
    print(line, line1)
    if 10 < len(line.strip().split()) < 20 and ' ' not in line1 and len(line1) > 10:
        f2.write(line)
        f3.write(line1)
        count += 1
    if count == 50:
        break
f.close()
f1.close()
f2.close()
f3.close()
