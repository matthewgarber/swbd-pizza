import os
import subprocess

paths = ['train/', 'devtest/']

for path in paths:
    oldpath = path + 'pizza/'
    newpath = path + 'pizza_8k/'
    if not os.path.exists(path + 'pizza_8k'):
        os.mkdir(path + 'pizza_8k')
    filenames = os.listdir(oldpath)
    for filename in filenames:
        os.system(' '.join(['sox', oldpath + filename,
                            '-r', '8000', newpath + filename, 'remix', '1']))
