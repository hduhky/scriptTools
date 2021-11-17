# -*-coding:utf-8-*-
import os
import json

rootPath = os.path.dirname('/Users/smb-lsp/Desktop/Uniarch_ChangeColor/ios/EZViewer/Images.xcassets')

def jsonfile_config(dirpath, jsonpath, imagenames):
    jsonfile = open(jsonpath, 'r')
    jsonstring = jsonfile.read()
    jsonfile.close()
    dict = json.loads(jsonstring)
    if 'images' not in dict:
        return
    images = dict['images']
    if len(images) != 3:
        print('please check files' + dirpath)
        return
    shouldupdate = False
    for imagename in imagenames:
        path = os.path.join(dirpath, imagename)
        if path.endswith(('png', 'jpg', 'jpeg')):
            if '2x' in imagename:
                originimagename = images[1]['filename']
                if imagename != originimagename:
                    images[1]['filename'] = imagename
                    shouldupdate = True
            if '3x' in imagename:
                originimagename = images[2]['filename']
                if imagename != originimagename:
                    images[2]['filename'] = imagename
                    shouldupdate = True
    if shouldupdate:
        jsonstring = json.dumps(dict, indent=2, separators=(',', ' : '))
        jsonfile = open(jsonpath, 'w')
        jsonfile.write(jsonstring)
        jsonfile.close()


for dirpath, dirnames, filenames in os.walk(rootPath):
    for filename in filenames:
        path = os.path.join(dirpath, filename)
        if path.endswith('json'):
            filenames.remove(filename)
            if len(filenames) > 0:
                jsonfile_config(dirpath, path, filenames)






