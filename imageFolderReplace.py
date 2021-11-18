# -*-coding:utf-8-*-
import os
import shutil

srcPath = os.path.dirname('/Users/smb-lsp/Desktop/Uniarch_ChangeColor_Images/')
assetsDstPathHead = os.path.dirname('/Users/smb-lsp/Desktop/Uniarch_ChangeColor/ios/EZViewer/Images.xcassets/')
resourcesDstPathHead = os.path.dirname('/Users/smb-lsp/Desktop/Uniarch_ChangeColor/ios/EZViewer/Resource/')

print('start copy assets...')
rootPath = os.path.join(srcPath, 'assets/')
for dirpath, dirnames, filenames in os.walk(rootPath):
    if dirpath.endswith('imageset'):
        dirpathend = dirpath.split(rootPath)[1]
        foldername = os.path.dirname(dirpathend)
        dstPath = os.path.join(assetsDstPathHead, foldername)
        os.system('cp -rf ' + dirpath + ' ' + dstPath)
print('copy assets finished\n')

print('start copy resources...')
rootPath = os.path.join(srcPath, 'resources/')
for dirpath, dirnames, filenames in os.walk(rootPath):
    for filename in filenames:
        if filename.endswith(('png', 'jpg', 'jpeg')):
            dirpathend = dirpath.split(rootPath)[1]
            dstPath = os.path.join(resourcesDstPathHead, dirpathend, filename)
            path = os.path.join(dirpath, filename)
            shutil.copy(path, dstPath)
print('copy resources finished')





