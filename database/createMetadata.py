from genericpath import isdir
from importlib.metadata import metadata
import json
import requests
from freeMusicArchiveClass import FreeMusicArchive
import sys
import os

numSongsPerGenre = 1

GENRES = [  'INTERNATIONAL',
            'BLUES',
            'JAZZ',
            'NOVELTY',
            'HISTORIC',
            'COUNTRY',
            'POP',
            'ROCK',
            'SOUL-RNB',
            'SPOKEN',
            'EXPERIMENTAL',
            'FOLK',
            'INSTRUMENTAL',
            'CLASSICAL',
            'ELECTRONIC',
            'HIP-HOP'
            ]

def storeDataTrackInfo(genre, dataTrackJson):
    j = json.loads(dataTrackJson)
    id = j["data-track-info"]["id"]
    handle = j["data-track-info"]["handle"]
    url = j["data-track-info"]["url"]
    title = j["data-track-info"]["title"]
    artistName = j["data-track-info"]["artistName"]
    artistUrl = j["data-track-info"]["artistUrl"]
    albumTitle = j["data-track-info"]["albumTitle"]
    playbackUrl = j["data-track-info"]["playbackUrl"]
    downloadUrl = j["data-track-info"]["downloadUrl"]
    fileName = j["data-track-info"]["fileName"]
    fileUrl = j["data-track-info"]["fileUrl"]

    c = FreeMusicArchive(genre, id, handle, url, title, artistName, artistUrl, albumTitle, playbackUrl, downloadUrl, fileName, fileUrl)

    return json.dumps(c.__dict__)


def getDataTrackInfo(genre, html):
    ret = False
    lines = html.splitlines()
    j = ''
    for line in lines:
        if 'data-track-info' in line:
            ret = True
            # print(line)

            startIdx = line.find('data-track-info') + len('data-track-info') + 2
            endIdx = line.rfind("}") + 1
            info = line[startIdx:endIdx].replace('\\', '')
            dataTrackJson = '{"data-track-info": %s}' % info
            j += '\t\t' + storeDataTrackInfo(genre, dataTrackJson) + ',\n'

    return ret, j

def genreHtmlPagesToJson(genre, url, f):
    pageCounter = 1
    fullJson = ''
    while 1:
        print('page: %d' % pageCounter)
        response = requests.get(url+str(pageCounter))
        if response.ok:
            contents = response.text
            foundSongs, j = getDataTrackInfo(genre, contents)
            if foundSongs:
                pageCounter += 1
                fullJson += j
            else:
                break
        else:
            break
    f.write(fullJson[:-2])
    return

def parseWebsiteForMetadata(url, folder):
    folder += '/data/'
    if not os.path.isdir(folder):
        os.mkdir(folder)

    f = open(folder + 'mp3Metadata.json', 'w')
    f.write('{ "songMetadata": \n\t[\n')
    metaDataJson = ''
    for genre in GENRES:
        print(genre)
        genreUrl = url + 'genre/' + genre.title() + '?sort=date&d=0&pageSize=200&page='

        # fix novelty
        if 'Novelty' in genreUrl:
            genreUrl = genreUrl.replace('Novelty', 'novelty')
        if 'Historic' in genreUrl:
            genreUrl = genreUrl.replace('Historic', 'Old-Time__Historic')
        if 'Soul-Rnb' in genreUrl:
            genreUrl = genreUrl.replace('Soul-Rnb', 'Soul-RB')
        if not genre == GENRES[0]:
            f.write(',\n')
        genreHtmlPagesToJson(genre, genreUrl, f)

    f.write('\n\t]\n}')
    f.close()

def main():
    folder = './'
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    if not os.path.isdir(folder):
        print(folder + ' not a folder')
        exit(1)

    parseWebsiteForMetadata('https://freemusicarchive.org/', folder)
    return

if __name__ == '__main__':
    main()