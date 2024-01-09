from glob import glob as glob
import PyPDF2

base_path = "D:\Desktop\Программы Питон\поиск файлов бот\data"
paths = glob(base_path + '/*.pdf*')
pdf_list = []
for f in paths:
    pdf_list.append(PyPDF2.PdfReader(f, 'rb'))
print(pdf_list[1])
print(paths[1][49:len(paths[1])-4])
"""base_path = "D:\Desktop\Программы Питон\поиск файлов бот\data"
t = glob(base_path + '/*.pdf*')
i = 0
print(t[1][49:len(t[1])])
if 'билет'.upper() in t[1]: print(1)"""