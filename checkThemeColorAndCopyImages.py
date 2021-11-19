# -*-coding:utf-8-*-
import os
from PIL import Image, ImageFile
import shutil
ImageFile.LOAD_TRUNCATED_IMAGES = True

themecolors = [{'r': 0, 'g': 221, 'b': 182}]
rootpath = '/Users/smb-lsp/Desktop/Uniarch_ChangeColor/ios/'
folderpath = '/Users/smb-lsp/Desktop/Uniarch_ChangeColor_Images/ios/'
result = []

def color_match(color):
    if not isinstance(color, tuple):
        return False
    for themecolor in themecolors:
        if color[0] == themecolor['r'] and color[1] == themecolor['g'] and color[2] == themecolor['b']:
            return True
    return False

def imageColor_config(imagepath):
    image = Image.open(imagepath)
    if imagepath.endswith(('gif')):
        image = image.convert('RGB')
    for x in range(0, image.width):
        for y in range(0, image.height):
            color = image.getpixel((x, y))
            if color_match(color):
                # print('include theme color' + dirpath) 
                result.append(imagepath)
                return

print('start check images...')
for dirpath, dirnames, filenames in os.walk(rootpath):
    for filename in filenames:
        path = os.path.join(dirpath, filename)
        if path.endswith(('pdf')):
            print('warning! please check pdf file: ' + path)
            continue
        if path.endswith(('png', 'jpg', 'jpeg', 'gif')):
            # print('start check image color' + path)
            imageColor_config(path)

print('check images finish:')
print('\n'.join(result))

print('copying images...')

for path in result:
    filename = path.split(rootpath)[1]
    dstfoldername = os.path.dirname(filename)
    dstpath = os.path.join(folderpath, dstfoldername)
    if not os.path.exists(dstpath):
        os.makedirs(dstpath)
    shutil.copy(path, dstpath)

print('copy images finished')
