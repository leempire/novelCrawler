import os

def merge(bookname):
    chapters = []
    path = os.path.join('data', bookname)
    for filename in sorted(os.listdir(path)):
        with open(os.path.join(path, filename), encoding='utf-8') as f:
            chapters.append(f.read())
    txt = '\n'.join(chapters)
    with open(os.path.join('data', bookname + '.txt'), 'w', encoding='utf-8') as f:
        f.write(txt)
