#!/usr/bin/python3
#for updog webserver
import argparse
import requests
import os
from time import sleep

VERSION = 0.7

parser = argparse.ArgumentParser(prog=os.path.splitext(os.path.basename(__file__))[0])

parser.add_argument('-ip', '--host', type=str, required=True,
                help='Ip addres or FQDN of the server to download')
parser.add_argument('-p', '--port', type=int, default=80,
                help='Port of the server [Default=80]')
parser.add_argument('-t', '--type', type=str, default="http",
                help='Select the type of cenection http/https [Default=http]')
parser.add_argument('-uf', '--upload_folder', type=str, required=True,
                help='Path to upload the files')
parser.add_argument('-lf', '--local_folder', type=str, default="./",
                help='Path to the folder for upload')
parser.add_argument('-w', '--wait_time', type=int, default=5,
                help='Time between each download in seconds [Default=5]')
parser.add_argument('-v', '--version', action='version', version='%(prog)s v'+str(VERSION))

args = parser.parse_args()


URL = args.type+"://"+args.host+":"+str(args.port)
uploader_path = "/upload"
POST_URL = URL + uploader_path #"http://192.168.1.110:9090/upload"
UPLOAD_FOLDER = args.upload_folder
FOLDER_TO_SCAN = args.local_folder
WAITING_TIME = args.wait_time

def uploadFile(infile_name:str)->None:
    #infile_name = "my_file.txt"

    file_details = {
        "name": "file",
        "file": open(infile_name, "rb"),
        "filename": os.path.basename(infile_name),
    }

    file_metadata = {"path": UPLOAD_FOLDER, "Referer": UPLOAD_FOLDER}
    post_headers = {"Referer": UPLOAD_FOLDER}
    try:
        print("Uploading "+ file_details['filename'])
        test_response = requests.post(POST_URL, files = file_details, data = file_metadata, headers = post_headers)
        #print(test_response.text)
        if test_response.ok:
            print("Upload completed successfully!")
        else:
            print("Something went wrong!")
            print("Server code  : " + str(test_response.status_code))
            print("Server reason: " + str(test_response.reason))
            print("Server text:"+'\n'+'\n')
            print(test_response.text)
            exit()
    except ConnectionRefusedError as e:
        print("Connection refused try double check the arguments.")
        exit()


def main():
    if os.path.isfile(os.path.join(FOLDER_TO_SCAN)):
        onlyfiles = [FOLDER_TO_SCAN]
    else:
        onlyfiles = [os.path.join(FOLDER_TO_SCAN, f) for f in os.listdir(FOLDER_TO_SCAN) if os.path.isfile(os.path.join(FOLDER_TO_SCAN, f))]
    #print()
    number_of_files = len(onlyfiles)
    print(str(number_of_files) + " files to upload."+'\n')
    for f in onlyfiles:
    #    #TODO Add speed limiter
        uploadFile(f)
        print("Waiting " +str(WAITING_TIME)+ " seconds before the next file") 
        for i in range(WAITING_TIME):
            print(str(WAITING_TIME - i), end = '\r')
            sleep(1)
        print(" ")

if __name__ == "__main__":
    print("Uploader version " + str(VERSION))
    main()

