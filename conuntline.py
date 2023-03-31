import os

path = '/workspace/2-4-2test1'
readfile = os.listdir(path)

print(readfile)

for filename in readfile:
    name, ext = os.path.splitext(filename)
    if ext.lower() == '.txt':
        f = open(f'{path}'+ os.sep + filename, 'r', encoding='UTF8' )
        cnt = 0

        while 1 :
            if f.readline() == '' :
                break
            cnt += 1
        print(filename)
        print("readline함수 : %d" % (cnt))
    else:
        continue