#!/usr/bin/python3
#for updog webserver
import argparse
import urllib.request
from urllib.parse import quote
import os.path
from time import sleep
import shutil

VERSION = 0.6

parser = argparse.ArgumentParser(prog=os.path.splitext(os.path.basename(__file__))[0])

parser.add_argument('-ip', '--host', type=str, required=True,
                help='Ip addres or FQDN of the server to download')
parser.add_argument('-p', '--port', type=int, default=80,
                help='Port of the server [Default=80]')
parser.add_argument('-f', '--folder', type=str, default="./",
                help='Path to save the content [Default=current folder]')
parser.add_argument('-w', '--wait_time', type=int, default=5,
                help='Time between each download in seconds [Default=5]')
parser.add_argument('-v', '--version', action='version', version='%(prog)s v'+str(VERSION))
parser.add_argument('-o', '--old_load_bar', action='store_true')

args = parser.parse_args()

#URL = "http://192.168.1.110:8080"
URL = args.host+":"+str(args.port)
SAVE_FOLDER = args.folder
WAITING_TIME = args.wait_time
OLD_BAR_STYLE = args.old_load_bar

def read_write_directory(directory):
    if os.path.exists(directory):
        if os.access(directory, os.W_OK and os.R_OK):
            return directory
        else:
            print('The output is not readable and/or writable')
            exit()
    else:
        print('The specified directory does not exist')
        exit()


def getFileLinks(URL:str)->list:
    print("Getting page for the links")
    with urllib.request.urlopen(URL) as f:
        page_html = f.read().decode("utf-8").splitlines()
    result = []
    for i in range(0,len(page_html)):
        print(i, end = '\r')
        if "<td> <!-- Name -->" in page_html[i]:
            h = page_html[i+1].strip()
            h = h.replace('''<a href="''','')
            h = h.replace('''</a>''','')
            flink, fname = h.split('''">''')
            #TODO
            ##if fname.endswith(".py") or fname.endswith(".txt"):
            ##    #skip files ending with txt and py can be changed
            ##    continue
            new_url = URL +"/"+ quote(flink)
            tmp={}
            tmp['url'] = new_url
            tmp['file'] = fname
            result.append(tmp)
    print("List of links genereted.")
    return result

#normalize the size of the progress bar based on the terminal size
size = shutil.get_terminal_size(fallback=(80, 20))
length = size.columns - 20

if OLD_BAR_STYLE:
    statusDoneChar = "=" #old style
    statusLeftChar = "_" #old style
else:
    statusDoneChar = "#"
    statusLeftChar = "."

def progresbar(block_num:int, block_size:int, total_size:int)->None:
    #resize the progressbar 
    prc = int(block_num*block_size/total_size * 100)
    if prc > 100:
        prc = 100
    downLoad = int(length*prc/100)
    left = length - downLoad

    status = statusDoneChar*(downLoad) + statusLeftChar * (left) + " "
    print(status, end = '\r')

def downloadFile(fileUrl:str, filename:str)->None:
    print("Downloading: "+fileUrl)
    urllib.request.urlretrieve(fileUrl, os.path.join(SAVE_FOLDER, filename), progresbar)
    print('\n')

def main():
    try:
        files = getFileLinks(URL)
    except ConnectionRefusedError as e:
        print("Connection refused try double check the arguments.")
        exit()

    print()
    number_of_files = len(files)
    print(str(number_of_files) + " files to download."+'\n')
    for f in files:
        #TODO Add speed limiter
        downloadFile(f['url'],f['file'])
        print("Waiting " +str(WAITING_TIME)+ " seconds before the next file") 
        for i in range(WAITING_TIME):
            print(str(WAITING_TIME - i), end = '\r')
            sleep(1)
        print()

if __name__ == "__main__":
    print("Downloader version " + str(VERSION))
    main()

