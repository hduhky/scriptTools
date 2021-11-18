# -*-coding:utf-8-*-
import os

srcPath = '/Users/smb-lsp/Desktop/Uniarch_ChangeColor_Images/'
dstPathHead = '/Users/smb-lsp/Desktop/Uniarch_ChangeColor/ios/EZViewer/Images.xcassets/'

for dirpath, dirnames, filenames in os.walk(srcPath):
    if dirpath.endswith('imageset'):
        dirpathend = dirpath.split(srcPath)[1]
        foldername = os.path.dirname(dirpathend)
        dstPath = dstPathHead + foldername
        os.system('cp -rf ' + dirpath + ' ' + dstPath)






