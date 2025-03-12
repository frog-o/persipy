from persipy import mount_opfs, show_tree

await mount_opfs()

show_tree()

with open('/opfs/folder/test2.txt', 'w') as f:
    f.write('test')


show_tree()

with open('/opfs/folder/test.txt', 'r') as f:
    text = f.read()
    print(text)


show_tree('/opfs/folder')