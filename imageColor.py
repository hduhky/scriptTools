# -*-coding:utf-8-*-
import os
from PIL import Image
import shutil

themecolors = [{'r': 80, 'g': 208, 'b': 193}, {'r': 94, 'g': 212, 'b': 198}]
rootPath = os.path.dirname('/Users/smb-lsp/Desktop/Uniarch_ChangeColor/ios/EZViewer/Images.xcassets/')
result = []

def imagecolor_config(dirpath, imagepath):
    image = Image.open(imagepath)
    for x in range(0, image.width):
        for y in range(0, image.height):
            color = image.getpixel((x, y))
            if color_match(color):
                # print('include theme color' + dirpath) 
                if dirpath in result:
                    return
                result.append(dirpath)

def color_match(color):
    for themecolor in themecolors:
        if color[0] == themecolor['r'] and color[1] == themecolor['g'] and color[2] == themecolor['b']:
            return True
    return False

for dirpath, dirnames, filenames in os.walk(rootPath):
    for filename in filenames:
        path = os.path.join(dirpath, filename)
        if path.endswith(('pdf', 'gif')):
            print('warning pdf or gif, please check files: ' + dirpath)
            continue
        if path.endswith(('png', 'jpg', 'jpeg')):
            # print('start check image color' + path)
            imagecolor_config(dirpath, path)

print('check finish:')
print('\n'.join(result))

print('copying')

folderpath = '/Users/smb-lsp/Desktop/Uniarch_ChangeColor_Images'
for path in result:
    foldername = path.split('Images.xcassets/')[1]
    dstpath = os.path.join(folderpath, foldername)
    shutil.copytree(path, dstpath)

print('copy finished')
