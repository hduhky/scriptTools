# -*-coding:utf-8-*-
import os
from PIL import Image, ImageFile
import shutil

themecolors = [{'r': 80, 'g': 208, 'b': 193}, {'r': 94, 'g': 212, 'b': 198}]
rootpath = os.path.dirname('/Users/smb-lsp/Desktop/Uniarch_ChangeColor/ios/')
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

ImageFile.LOAD_TRUNCATED_IMAGES = True
print('start check images...')
for dirpath, dirnames, filenames in os.walk(rootpath):
    for filename in filenames:
        path = os.path.join(dirpath, filename)
        if path.endswith(('pdf')):
            print('warning pdf or gif, please check files: ' + path)
            continue
        if path.endswith(('png', 'jpg', 'jpeg', 'gif')):
            # print('start check image color' + path)
            imageColor_config(path)

print('check images finish:')
print('\n'.join(result))

print('copying images...')

folderpath = '/Users/smb-lsp/Desktop/Uniarch_ChangeColor_Images/ios/'
for path in result:
    filename = path.split('/Users/smb-lsp/Desktop/Uniarch_ChangeColor/ios/')[1]
    dstfoldername = os.path.dirname(filename)
    dstpath = os.path.join(folderpath, dstfoldername)
    if not os.path.exists(dstpath):
        os.makedirs(dstpath)
    shutil.copy(path, dstpath)

print('copy images finished')
