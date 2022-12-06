import sys
import os
import database.createMetadata
import database.downloadMP3s
import database.featureExtraction

def main():
    folder = './'
    if len(sys.argv) > 1:
        folder: str = sys.argv[1]
    if len(sys.argv) > 2:
        maxFiles: int = int(sys.argv[2])
    
    if not os.path.isdir(folder):
        print(folder + ' not a folder')
        exit(1)
    
    database.createMetadata.parse_website_for_metadata('https://freemusicarchive.org/', folder)
    database.downloadMP3s.downloadMP3s(folder, maxFiles=maxFiles)
    database.featureExtraction.featureExtraction(folder)

if __name__ == '__main__':
    main()