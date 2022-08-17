#!/usr/bin/python3
from bottle import SimpleTemplate
import argparse
import os.path

version = 0.3

parser = argparse.ArgumentParser(prog=os.path.splitext(os.path.basename(__file__))[0])

parser.add_argument('-src', '--source_folder', type=str, default="./",
                help='Source folder, where the py file are stored. Default is curent folder.')
parser.add_argument('-build', '--release_folder', type=str, default="./",
                help='Target for the final build. Default is curent folder.')
parser.add_argument('-v', '--version', action='version', version='%(prog)s v'+str(version))

args = parser.parse_args()

source_folder = args.source_folder
release_folder = args.release_folder

print("Builder version " + str(version))

with open(os.path.join(source_folder, "server.py"), encoding = 'utf-8') as f:
   server_src = f.read()

with open(os.path.join(source_folder, "downloader.py"), encoding = 'utf-8') as f:
   downloader_src = f.read()

# Something replaces the end of the \r or \n line when building the final file.
# This will /r and /n with _r and _n
downloader_src = downloader_src.replace("'\\r'", "'_r'")
downloader_src = downloader_src.replace("'\\n'", "'_n'")

with open(os.path.join(source_folder, "uploader.py"), encoding = 'utf-8') as f:
   uploader_src = f.read()
uploader_src = uploader_src.replace("'\\r'", "'_r'")
uploader_src = uploader_src.replace("'\\n'", "'_n'")

server_tpl = SimpleTemplate(server_src)
server_final_src = server_tpl.render(downloader_source=downloader_src, uploader_source = uploader_src)

with open(os.path.join(release_folder, "simpleHttpFileLister.py"), 'w', encoding = 'utf-8') as f:
   f.write(server_final_src)

print("Done!")
print('The final script is' + os.path.join(release_folder, "simpleHttpFileLister.py"))
