import sys
import os
import createMetadata
import downloadMP3s
import featureExtraction

def main():
    folder = './'
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    if len(sys.argv) > 2:
        maxFiles = int(sys.argv[2])
    
    if not os.path.isdir(folder):
        print(folder + ' not a folder')
        exit(1)
    
    createMetadata.parseWebsiteForMetadata('https://freemusicarchive.org/', folder)
    downloadMP3s.downloadMP3s(folder, maxFiles=maxFiles)
    featureExtraction.featureExtraction(folder)

if __name__ == '__main__':
    main()