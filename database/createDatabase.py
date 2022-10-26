import json
import requests
from freeMusicArchiveClass import FreeMusicArchive
import sys
import os

numSongsPerGenre = 1

genres = [  'INTERNATIONAL',
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

def storeDataTrackInfo(dataTrackJson):
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

    c = FreeMusicArchive(id, handle, url, title, artistName, artistUrl, albumTitle, playbackUrl, downloadUrl, fileName, fileUrl)

    print(json.dumps(c.__dict__))


def getDataTrackInfo(html):
    ret = False
    lines = html.splitlines()
    for line in lines:
        if 'data-track-info' in line:
            ret = True
            # print(line)

            startIdx = line.find('data-track-info') + len('data-track-info') + 2
            endIdx = line.rfind("}") + 1
            info = line[startIdx:endIdx].replace('\\', '')
            dataTrackJson = '{"data-track-info": %s}' % info
            storeDataTrackInfo(dataTrackJson)

    return ret

def getGenreHtmlPages(url):
    pageCounter = 1
    while 1:
        print(pageCounter)
        response = requests.get(url+str(pageCounter))
        if response.ok:
            contents = response.text
            if getDataTrackInfo(contents):
                pageCounter += 1
            else:
                break
        else:
            break

def parseWebsiteToClasses(url):
    for genre in genres:
        print(genre)
        genreUrl = url + 'genre/' + genre.title() + '?sort=date&d=0&pageSize=200&page='

        # fix novelty
        if 'Novelty' in genreUrl:
            genreUrl = genreUrl.replace('Novelty', 'novelty')
        if 'Historic' in genreUrl:
            genreUrl = genreUrl.replace('Historic', 'Old-Time__Historic')
        if 'Soul-Rnb' in genreUrl:
            genreUrl = genreUrl.replace('Soul-Rnb', 'Soul-RB')
        getGenreHtmlPages(genreUrl)



def main():
    parseWebsiteToClasses('https://freemusicarchive.org/')


    return

if __name__ == '__main__':
    main()