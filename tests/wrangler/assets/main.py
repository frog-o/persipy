from src import opfs



path = '/test/text.txt'
path2 = '/test/text2.txt'


await opfs.init()


with opfs(path, ) as file:
    print(await file.write('asd'))
    print(await file.get_text())
    print(await file.write('asdddd'))
    print(await file.get_bytes())
    print(await file.read())
    #print(await file.write('asdddd'*100))


