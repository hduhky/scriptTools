# -*-coding:utf-8-*-
import os
from PIL import Image
import shutil

themecolors = [{'r': 80, 'g': 208, 'b': 193}, {'r': 94, 'g': 212, 'b': 198}]
assetsPath = os.path.dirname('/Users/smb-lsp/Desktop/Uniarch_ChangeColor/ios/EZViewer/Images.xcassets/')
resourcePath = os.path.dirname('/Users/smb-lsp/Desktop/Uniarch_ChangeColor/ios/EZViewer/Resource/')
result = []

# 检测所有图片中带有主题色的图片，并保存（老版本）

def color_match(color):
    if not isinstance(color, tuple):
        return False
    for themecolor in themecolors:
        if color[0] == themecolor['r'] and color[1] == themecolor['g'] and color[2] == themecolor['b']:
            return True
    return False


def assetsColor_config(dirpath, imagepath):
    image = Image.open(imagepath)
    for x in range(0, image.width):
        for y in range(0, image.height):
            color = image.getpixel((x, y))
            if color_match(color):
                # print('include theme color' + dirpath) 
                if dirpath in result:
                    return
                result.append(dirpath)

def resourceColor_config(imagepath):
    image = Image.open(imagepath)
    for x in range(0, image.width):
        for y in range(0, image.height):
            color = image.getpixel((x, y))
            if color_match(color):
                # print('include theme color' + dirpath) 
                result.append(imagepath)
                return

print('start check assets...')
for dirpath, dirnames, filenames in os.walk(assetsPath):
    for filename in filenames:
        path = os.path.join(dirpath, filename)
        if path.endswith(('pdf', 'gif')):
            print('warning pdf or gif, please check files: ' + path)
            continue
        if path.endswith(('png', 'jpg', 'jpeg')):
            # print('start check image color' + path)
            assetsColor_config(dirpath, path)


print('check assets finish:')
print('\n'.join(result))

print('copying assets...')

folderpath = '/Users/smb-lsp/Desktop/Uniarch_ChangeColor_Images/assets/'
for path in result:
    foldername = path.split('Images.xcassets/')[1]
    dstpath = os.path.join(folderpath, foldername)
    shutil.copytree(path, dstpath)

print('copy assets finished\n')

result = []

print('start check resources...')
for dirpath, dirnames, filenames in os.walk(resourcePath):
    for filename in filenames:
        path = os.path.join(dirpath, filename)
        if path.endswith(('pdf', 'gif')):
            print('warning pdf or gif, please check files: ' + path)
            continue
        if path.endswith(('png', 'jpg', 'jpeg')):
            # print('start check image color' + path)
            resourceColor_config(path)

print('check resources finish:')
print('\n'.join(result))

print('copying resources...')

folderpath = '/Users/smb-lsp/Desktop/Uniarch_ChangeColor_Images/resources/'
for path in result:
    filename = path.split('Resource/')[1]
    dstfoldername = os.path.dirname(filename)
    dstpath = os.path.join(folderpath, dstfoldername)
    if not os.path.exists(dstpath):
        os.makedirs(dstpath)
    shutil.copy(path, dstpath)

print('copy resources finished')
