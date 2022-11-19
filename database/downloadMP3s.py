import shutil
import sys
import os
import json
import requests
from createMetadata import GENRES

def readMetadataJson(jsonFilename):
    f = open(jsonFilename, 'r')
    metaJson = json.load(f)

    return metaJson

def removeDuplicates(metaJson):
    print(len(metaJson['songMetadata']))
    downloadUrlList = []
    duplicateUrlList = []
    genreList = []
    for i, m in enumerate(metaJson['songMetadata']):
        print('%d/%d' % (i+1,len(metaJson['songMetadata'])))
        if m['downloadUrl'] not in downloadUrlList:
            downloadUrlList.append(m['downloadUrl'])
        else:
            duplicateUrlList.append(m['downloadUrl'])

    cleanJson = {'songMetadata': []}
    for i, m in enumerate(metaJson['songMetadata']):
        if m['downloadUrl'] not in duplicateUrlList:
            cleanJson['songMetadata'].append(m)
    print(len(cleanJson['songMetadata']))
    return cleanJson

def removeGenreDirs(folder = './'):
    folder += '/data/'
    for genre in GENRES:
        if os.path.isdir(folder+genre):
            shutil.rmtree(folder+genre)
    
def makeGenreDirs(folder = './'):
    folder += '/data/'
    for genre in GENRES:
        if not os.path.isdir(folder+genre):
            os.mkdir(folder+genre)


def downloadMp3Files(metaJson, folder='./'):
    # print(len(metaJson['songMetadata']))
    for i, m in enumerate(metaJson['songMetadata']):
        print("%d/%d" % (i+1,len(metaJson['songMetadata'])))
        if m['fileName'] == '' or m['fileName'] == None or m['downloadUrl'] == None or m['downloadUrl'] == '':
            print('Insufficient data, did not download')
            continue
        filename = folder + '/data/' + m['genre'] + '/' + m['fileName']
        if os.path.isfile(filename):
            continue

        try:
            response = requests.get(m['downloadUrl'])
            if response.ok:
                open(filename, 'wb').write(response.content)
            else:
                print(filename + ' did not download')
        except:
            print("Error in downloading")
        

def downloadMP3s(folder, remove=False):
    metaJson = readMetadataJson(folder + '/data/mp3Metadata.json')
    metaJson = removeDuplicates(metaJson)
    if remove:
        removeGenreDirs(folder)
    makeGenreDirs(folder)
    downloadMp3Files(metaJson, folder)

def main():
    folder = './'
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    if not os.path.isdir(folder):
        print(folder + ' not a folder')
        exit(1)

    downloadMP3s(folder, False)

if __name__ == '__main__':
    main()
