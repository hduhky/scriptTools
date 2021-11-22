# -*-coding:utf-8-*-
import os
import shutil
from pdf2image import convert_from_path
from PIL import Image, ImageFile
from minecart.miner import Document
ImageFile.LOAD_TRUNCATED_IMAGES = True

themecolors = ['#50D0C1', '#00ddb6', '#5ED4C6']
rootpath = '/Users/smb-lsp/Desktop/Uniarch_ChangeColor/ios/'
folderpath = '/Users/smb-lsp/Desktop/Uniarch_ChangeColor_Images/ios/'
rgbcolors = []
result = []

def hex_to_rgb(hex):
    if '#' in hex:
        hex.split('#')[1]
    r = int(hex[1:3], 16)
    g = int(hex[3:5], 16)
    b = int(hex[5:7], 16)
    return {'r': r, 'g': g, 'b': b}

def color_match(color):
    if not isinstance(color, tuple):
        return False
    for rgbcolor in rgbcolors:
        if abs(color[0] - rgbcolor['r']) > 10:
            return False
        if abs(color[1] - rgbcolor['g']) > 10:
            return False
        if abs(color[2] - rgbcolor['b']) > 10:
            return False
        return True


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

def pdfColor_config(imagepath):
    images = convert_from_path(imagepath)
    for image in images:
        for x in range(0, image.width):
            for y in range(0, image.height):
                color = image.getpixel((x, y))
                if color_match(color):
                    # print('include theme color' + dirpath) 
                    result.append(imagepath)
                    return

print('hex to rgb...')
for hex in themecolors:
    rgb = hex_to_rgb(hex)
    print(hex + ':')
    print(rgb)
    rgbcolors.append(rgb)
print('hex to rgb finished')

print('start check images...')
for dirpath, dirnames, filenames in os.walk(rootpath):
    for filename in filenames:
        path = os.path.join(dirpath, filename)
        if path.endswith(('pdf')):
            print('warning! please check pdf file: ' + path)
            # pdfColor_config(path)
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
