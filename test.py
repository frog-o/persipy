from persipy import mount_opfs, show_tree

show_tree()

await mount_opfs()

show_tree()

with open('/opfs/test.txt', 'w') as f:
    f.write('test')

show_tree()

with open('/opfs/test.txt', 'r') as f:
    text = f.read()
    print('content:', text)

