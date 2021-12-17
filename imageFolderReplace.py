# -*-coding:utf-8-*-
import os
import shutil

# 用于两个目录相同的文件夹内容替换

srcPath = '/Users/smb-lsp/Desktop/Uniarch_ChangeColor_Images/ios/'
dstPath = '/Users/smb-lsp/Desktop/Uniarch_ChangeColor/ios/'

print('start copy images...')
for dirpath, dirnames, filenames in os.walk(srcPath):
    for filename in filenames:
        if filename.endswith(('png', 'jpg', 'jpeg', 'gif')):
            fileSrcPath = os.path.join(dirpath, filename)
            dirpathend = dirpath.split(srcPath)[1]
            fileDstPath = os.path.join(dstPath, dirpathend, filename)
            shutil.copy(fileSrcPath, fileDstPath)
print('copy images finished')





