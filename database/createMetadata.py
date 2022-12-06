import json
import requests
from database.freeMusicArchiveClass import FreeMusicArchive
import sys
import os

numSongsPerGenre = 1

GENRES: List[str] = [
    'JAZZ',
    'COUNTRY',
    'POP',
    'ROCK',
    'SOUL-RNB',
    'CLASSICAL',
    'HIP-HOP'
]


def store_data_track_info(genre, data_track_json) -> str:
    j = json.loads(data_track_json)
    
    id = j["data-track-info"]["id"]
    handle = j["data-track-info"]["handle"]
    url = j["data-track-info"]["url"]
    title = j["data-track-info"]["title"]
    artist_name = j["data-track-info"]["artistName"]
    artist_url = j["data-track-info"]["artistUrl"]
    album_title = j["data-track-info"]["albumTitle"]
    play_back_url = j["data-track-info"]["playbackUrl"]
    download_url = j["data-track-info"]["downloadUrl"]
    file_name = j["data-track-info"]["fileName"]
    file_url = j["data-track-info"]["fileUrl"]

    c = FreeMusicArchive(genre, id, handle, url, title, artist_name,
                         artist_url, album_title, play_back_url, download_url, file_name, file_url)

    return json.dumps(c.__dict__)


def get_data_track_info(genre, html):
    ret: bool = False
    lines: List[str] = html.splitlines()
    j: str = ''
    for line in lines:
        if 'data-track-info' in line:
            ret: bool = True
            # print(line)

            start_idx = line.find('data-track-info') + \
                len('data-track-info') + 2
            end_index = line.rfind("}") + 1
            info = line[start_idx:end_index].replace('\\', '')
            data_track_json = '{"data-track-info": %s}' % info
            j += '\t\t' + store_data_track_info(genre, data_track_json) + ',\n'

    return ret, j


def genre_html_pages_to_json(genre, url, f) -> None:
    page_counter: int = 1
    full_json: str = ''
    while 1:
        print('page: %d' % page_counter)
        response = requests.get(url+str(page_counter))
        if response.ok:
            contents = response.text
            found_songs, j = get_data_track_info(genre, contents)
            if found_songs:
                page_counter += 1
                full_json += j
            else:
                break
        else:
            break
    f.write(full_json[:-2])


def parse_website_for_metadata(url, folder) -> None:
    folder += '/data/'
    if not os.path.isdir(folder):
        os.mkdir(folder)

    f = open(folder + 'mp3Metadata.json', 'w')
    f.write('{ "songMetadata": \n\t[\n')

    for genre in GENRES:
        print(genre)
        genre_url: str = url + 'genre/' + \
            genre.title() + '?sort=date&d=0&pageSize=200&page='

        # fix novelty
        if 'Novelty' in genre_url:
            genre_url: str = genre_url.replace('Novelty', 'novelty')
        if 'Historic' in genre_url:
            genre_url = genre_url.replace('Historic', 'Old-Time__Historic')
        if 'Soul-Rnb' in genre_url:
            genre_url = genre_url.replace('Soul-Rnb', 'Soul-RB')
        if genre != GENRES[0]:
            f.write(',\n')
        genre_html_pages_to_json(genre, genre_url, f)

    f.write('\n\t]\n}')
    f.close()


def main() -> None:
    folder: str = './'
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    if not os.path.isdir(folder):
        print(folder + ' not a folder')
        exit(1)

    parse_website_for_metadata('https://freemusicarchive.org/', folder)


if __name__ == '__main__':
    main()
