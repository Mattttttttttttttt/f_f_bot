from glob import glob

path = 'D:\Desktop\Программы Питон\поиск файлов бот\data_backup'
paths = glob(path + '\*')
names =[]
print(paths)
for i in range(len(paths)):
    j = 1
    names_2 = []
    while True:
        names_2.append(paths[i][len(paths[i])-j])
        costyl = '\ '
        if paths[i][len(paths[i])-j] == costyl[0]: break
        j = j + 1
    names_2 = names_2[0:len(names_2) - 1]
    names.append(' ')
    for j in range(len(names_2)):
        names[i] = names[i] + names_2[len(names_2) - 1 - j]
    names[i] = names[i][1:len(names[i])]
print(names)

base_path = 'D:\Desktop\Программы Питон\поиск файлов бот\data' + '\\name'
print(base_path)
