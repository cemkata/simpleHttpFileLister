#!/usr/bin/python3
#updog webserver clone
from bottle import Bottle, run, static_file, redirect, request, response, abort
import os
import time
import argparse
from io import BytesIO

VERSION = 3.0

blankIcon='data:image/gif;base64, R0lGODlhFAAWAKEAAP///8z//wAAAAAAACH+TlRoaXMgYXJ0IGlzIGluIHRoZSBwdWJsaWMgZG9tYWluLiBLZXZpbiBIdWdoZXMsIGtldmluaEBlaXQuY29tLCBTZXB0ZW1iZXIgMTk5NQAh+QQBAAABACwAAAAAFAAWAAACE4yPqcvtD6OctNqLs968+w+GSQEAOw=='
backIcon='data:image/gif;base64, R0lGODlhFAAWAMIAAP///8z//5mZmWZmZjMzMwAAAAAAAAAAACH+TlRoaXMgYXJ0IGlzIGluIHRoZSBwdWJsaWMgZG9tYWluLiBLZXZpbiBIdWdoZXMsIGtldmluaEBlaXQuY29tLCBTZXB0ZW1iZXIgMTk5NQAh+QQBAAABACwAAAAAFAAWAAADSxi63P4jEPJqEDNTu6LO3PVpnDdOFnaCkHQGBTcqRRxuWG0v+5LrNUZQ8QPqeMakkaZsFihOpyDajMCoOoJAGNVWkt7QVfzokc+LBAA7'
fileIcon='data:image/gif;base64, R0lGODlhEgAWAEAAACH+T1RoaXMgYXJ0IGlzIGluIHRoZSBwdWJsaWMgZG9tYWluLiBLZXZpbiBIdWdoZXMsIGtldmluaEBlaXQuY29tLCBTZXB0ZW1iZXIgMTk5NQAAIfkEAQAAAQAsAAAAABIAFgCHAAAAAAAzAABmAACZAADMAAD/ACsAACszACtmACuZACvMACv/AFUAAFUzAFVmAFWZAFXMAFX/AIAAAIAzAIBmAICZAIDMAID/AKoAAKozAKpmAKqZAKrMAKr/ANUAANUzANVmANWZANXMANX/AP8AAP8zAP9mAP+ZAP/MAP//MwAAMwAzMwBmMwCZMwDMMwD/MysAMyszMytmMyuZMyvMMyv/M1UAM1UzM1VmM1WZM1XMM1X/M4AAM4AzM4BmM4CZM4DMM4D/M6oAM6ozM6pmM6qZM6rMM6r/M9UAM9UzM9VmM9WZM9XMM9X/M/8AM/8zM/9mM/+ZM//MM///ZgAAZgAzZgBmZgCZZgDMZgD/ZisAZiszZitmZiuZZivMZiv/ZlUAZlUzZlVmZlWZZlXMZlX/ZoAAZoAzZoBmZoCZZoDMZoD/ZqoAZqozZqpmZqqZZqrMZqr/ZtUAZtUzZtVmZtWZZtXMZtX/Zv8AZv8zZv9mZv+ZZv/MZv//mQAAmQAzmQBmmQCZmQDMmQD/mSsAmSszmStmmSuZmSvMmSv/mVUAmVUzmVVmmVWZmVXMmVX/mYAAmYAzmYBmmYCZmYDMmYD/maoAmaozmapmmaqZmarMmar/mdUAmdUzmdVmmdWZmdXMmdX/mf8Amf8zmf9mmf+Zmf/Mmf//zAAAzAAzzABmzACZzADMzAD/zCsAzCszzCtmzCuZzCvMzCv/zFUAzFUzzFVmzFWZzFXMzFX/zIAAzIAzzIBmzICZzIDMzID/zKoAzKozzKpmzKqZzKrMzKr/zNUAzNUzzNVmzNWZzNXMzNX/zP8AzP8zzP9mzP+ZzP/MzP///wAA/wAz/wBm/wCZ/wDM/wD//ysA/ysz/ytm/yuZ/yvM/yv//1UA/1Uz/1Vm/1WZ/1XM/1X//4AA/4Az/4Bm/4CZ/4DM/4D//6oA/6oz/6pm/6qZ/6rM/6r//9UA/9Uz/9Vm/9WZ/9XM/9X///8A//8z//9m//+Z///M////AAAAAAAAAAAAAAAACGUAYwgcSHDgvoMHYyBciFChwoYMGT58uI9ixIoQMV5MuNDhxoMAYoQcaTEigJMoQ348mKllS5Ur97nMBDMmy5o2aZZcqdMmwp4+ZeKMCdRn0ZxDeSb9eJRoyBgzo0YVCTKl1asBAQA7'
folderIcon='data:image/gif;base64, R0lGODlhEwARAEAAACH+T1RoaXMgYXJ0IGlzIGluIHRoZSBwdWJsaWMgZG9tYWluLiBLZXZpbiBIdWdoZXMsIGtldmluaEBlaXQuY29tLCBTZXB0ZW1iZXIgMTk5NQAAIfkEAQAAAgAsAAAAABMAEQCHAAAAAAAzAABmAACZAADMAAD/ACsAACszACtmACuZACvMACv/AFUAAFUzAFVmAFWZAFXMAFX/AIAAAIAzAIBmAICZAIDMAID/AKoAAKozAKpmAKqZAKrMAKr/ANUAANUzANVmANWZANXMANX/AP8AAP8zAP9mAP+ZAP/MAP//MwAAMwAzMwBmMwCZMwDMMwD/MysAMyszMytmMyuZMyvMMyv/M1UAM1UzM1VmM1WZM1XMM1X/M4AAM4AzM4BmM4CZM4DMM4D/M6oAM6ozM6pmM6qZM6rMM6r/M9UAM9UzM9VmM9WZM9XMM9X/M/8AM/8zM/9mM/+ZM//MM///ZgAAZgAzZgBmZgCZZgDMZgD/ZisAZiszZitmZiuZZivMZiv/ZlUAZlUzZlVmZlWZZlXMZlX/ZoAAZoAzZoBmZoCZZoDMZoD/ZqoAZqozZqpmZqqZZqrMZqr/ZtUAZtUzZtVmZtWZZtXMZtX/Zv8AZv8zZv9mZv+ZZv/MZv//mQAAmQAzmQBmmQCZmQDMmQD/mSsAmSszmStmmSuZmSvMmSv/mVUAmVUzmVVmmVWZmVXMmVX/mYAAmYAzmYBmmYCZmYDMmYD/maoAmaozmapmmaqZmarMmar/mdUAmdUzmdVmmdWZmdXMmdX/mf8Amf8zmf9mmf+Zmf/Mmf//zAAAzAAzzABmzACZzADMzAD/zCsAzCszzCtmzCuZzCvMzCv/zFUAzFUzzFVmzFWZzFXMzFX/zIAAzIAzzIBmzICZzIDMzID/zKoAzKozzKpmzKqZzKrMzKr/zNUAzNUzzNVmzNWZzNXMzNX/zP8AzP8zzP9mzP+ZzP/MzP///wAA/wAz/wBm/wCZ/wDM/wD//ysA/ysz/ytm/yuZ/yvM/yv//1UA/1Uz/1Vm/1WZ/1XM/1X//4AA/4Az/4Bm/4CZ/4DM/4D//6oA/6oz/6pm/6qZ/6rM/6r//9UA/9Uz/9Vm/9WZ/9XM/9X///8A//8z//9m//+Z///M////AAAAAAAAAAAAAAAACMUA9+0DQLAgQYEIEw7UN4+hw3kAFCIEMG8etHnK5j2jl0yfwYMDJc2j96xhMnr5GOVDyTIiAH2SdknixYjXLpUkOZLkRXDkynwdO847CVRfLUkxACjLlzEjyoz6hC7llXRlSX0ln5pEyWhXUp1MR27USI9sPqQAfkI9OfYiR15UlYadm9MsvUhVy16MWpbpyo6L4rIdKdQt0alJGeYE+tRq2ZlJO0a6S3nyLmW7KscYaItXJLieecUUvUt0jM0DT6tezXpzQAA7'
favicon='data:image/ico;base64, AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAABILAAASCwAAAAAAAAAAAAD//////////////////////////////////////////////////////////////////////////////////////v///9n0//+86///vOv//7zr//+86///vOv//7zr//+86///vOv//7zr//+86///vOv//7zr//+86///zO/+/+v5//9n0v//Qsj//0TI//9EyP//RMj//0TI//9EyP//RMj//0TI//9EyP//RMj//0TI//9EyP//RMj//0bD9//R8f//Tsv//0LI//9DyP//Q8j//0PI//9DyP//Q8j//0PI//9DyP//Q8j//0PI//9DyP//Q8j//0PJ//8ztez/tOn//0bJ//9DyP//Q8j//0PI//9DyP//Q8j//0PI//9DyP//Q8j//0PI//9DyP//Q8j//0PI//9DyP//Kqjg/5Tg//9CyP//Q8j//0PI//9DyP//Q8j//0PI//9DyP//Q8j//0PI//9DyP//Q8j//0PI//9DyP//Qsf+/x+b0/9z1v//Qcj//0PI//9DyP//Q8j//0PI//9DyP//Q8j//0PI//9DyP//Q8j//0PI//9DyP//Q8j//z/D+v8Wj8j/Vc3//0LI//9DyP//Q8j//0PI//9CyP//Qsj//0LI//9CyP//Qsj//0LI//9CyP//Qsj//0PJ//87vvT/D4bA/1rO//9DxPv/PsL5/z/C+f9Jx/z/Tsr9/03K/f9Nyv3/Tcr9/03K/f9Nyv3/Tcr9/03K/f9Gxvv/LKri/wp/uP/a8vz/QKjZ/wyPzP8Sks3/g8Pd/7zd5v+53Ob/udzm/7nc5v+53Ob/udzm/7nc5v+73Ob/WbHX/wWGxf8DgsD/+fz+/2K54/8Mk9X/A47S/5LG3P/Dx8P/rK6q/62vqv+tsKv/v8XC/7Czr/+tsKv/ytLQ/2q42/8Sl9f/KqHa///////u9/z/uuDz/1W04v+m0OD/xs7M/7a9uv+3vbr/t726/7zEwv+4vrz/t767/8rV1P/V6O7/1ez4/+Py+v/////////////////5/P7/3+nq/77GxP+tsa3/rbKu/62yrv+tsa7/rbKu/66zr//H0tH/7fLy/////////////////////////////v///+Hq6v/T4OD/1OHh/9Th4f/U4eH/1OHh/9Th4f/U4eH/0+Dg/+zy8v/////////////////////////////////0+Pj/7/T0/+/09P/v9PT/7/T0/+/09P/v9PT/7/T0/+/09P/4+vr/////////////////////////////////////////////////////////////////////////////////////////////////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=='
header = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html><head><link rel="icon" href="'''+favicon+'''" type="image/x-icon"/><meta http-equiv="content-type" content="text/html; charset=UTF-8">  <title>Index of {path}</title> </head> <body><h1>Index of {path}</h1>
<form action="/upload" method="post" enctype="multipart/form-data"><h2><input type="hidden" name="path" value = '{path}'/><input type="hidden" name="Referer" value = '{path}'/>
Select a file: <input type="file" name="file" /><br><input type="submit" value="Start upload" /></h2></form><div id="tools"><a href="./?getDownloadTool=1">getDownloadTool</a>
<a href="./?getUploadTool=1">getUploadTool</a></div></br><table>   <tbody><tr><th valign="top"><img src="'''+blankIcon+'''" alt="[ICO]"></th><th>Name</th><th>Last modified</th><th>Size</th></tr>   <tr><th colspan="4"><hr></th></tr>\n'''
header_no_upload = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html><head><link rel="icon" href="'''+favicon+'''" type="image/x-icon"/><meta http-equiv="content-type" content="text/html; charset=UTF-8">  <title>Index of {path}</title> </head> <body><h1>Index of {path}</h1>
<div id="tools">
<a href="./?getUploadTool=1">getUploadTool</a></div></br><table>   <tbody><tr><th valign="top"><img src="'''+blankIcon+'''" alt="[ICO]"></th><th>Name</th><th>Last modified</th><th>Size</th></tr>   <tr><th colspan="4"><hr></th></tr>\n'''
footer = '''\n<tr><th colspan="4"><hr></th></tr></tbody></table><address>{name} at {ip} Port {port}</address></body></html>'''
parentfolder = '''<tr><td valign="top"><img src="'''+backIcon+'''" alt="[PARENTDIR]"></td><td><a href="..">Parent Directory</a></td><td>&nbsp;</td><td align="right">  - </td></tr>\n'''


downloader_py = """{{!downloader_source}}"""
# Something replaces the end of the \r or \n line when building the final file.
# This will /r and /n with _r and _n
downloader_py = downloader_py.replace("'_r'","'\\r'").replace("'_n'","'\\n'")

uploader_py = """{{!uploader_source}}"""
# Something replaces the end of the \r or \n line when building the final file.
# This will /r and /n with _r and _n
uploader_py = uploader_py.replace("'_r'","'\\r'").replace("'_n'","'\\n'")

app = Bottle()

@app.route('/upload', method='POST')
def do_upload():
   if not noUpload:
      abort(404, "Not Found.")
   path = request.forms.get('path')
   upload = request.files.get('file')
   #filename = request.forms.get('filename') #Not needed?
   referer = request.forms.get('Referer') or request.headers["Referer"]
   if path.startswith('/'):
      path = path.replace("/","", 1)
   if path.startswith('../'):
       redirect('/' + path)
   save_path = os.path.join(rootFolder, path)
   # Check if folder exist
   # If the path is not there
   # redirect to home
   if not os.path.isdir(save_path):
      abort(500, "Sorry, upload folder do not exist.")
      #redirect('./')

   i = 1
   # - Added support for overwriting
   file_name = upload.filename
   overWriteFlag = True
   while overWriteFlag:
       if os.path.isfile(os.path.join(save_path, file_name)):
          file_name = upload.filename + "_" + str(i)
          i = i + 1
       else:
          upload.filename = file_name
          overWriteFlag = False
   # Assuming all is good, process and save out the file
   upload.save(save_path) # appends upload.filename automatically
   try:
      redirect('./' + referer)
   except TypeError as e:
      #print("Fallback")
      redirect('./')
   

@app.route('/')
@app.route('/<filepath:path>')
def index(filepath = '/'):
   getDownloadTool = request.query.getDownloadTool or None
   getUploadTool = request.query.getUploadTool or None
   if getDownloadTool:

      _buffer = BytesIO(downloader_py.encode('utf-8'))
      _buffer.seek(0) # this may not be needed
      bytes = _buffer.read()
      response.set_header('Content-type', 'text/x-python')
      response.set_header('Content-disposition', 'attachment ; filename = "downloader.py"')
      return bytes
   if getUploadTool:
      _buffer = BytesIO(uploader_py.encode('utf-8'))
      _buffer.seek(0) # this may not be needed
      bytes = _buffer.read()
      response.set_header('Content-type', 'text/x-python')
      response.set_header('Content-disposition', 'attachment ; filename = "uploader.py"')
      return bytes

   if filepath == 'favicon.ico':
      return favicon
   if os.path.isfile(filepath):
      return static_file(filepath, root=rootFolder)
   else:
       page=header.format(path=filepath)
       if filepath.startswith('../') or filepath == '/':
          filepath = ""
          listed_folder = rootFolder
       else:
          page = page + parentfolder
          listed_folder = os.path.join(rootFolder, filepath)
       try:
          for fn in os.listdir(listed_folder):
             fileName = os.path.join(rootFolder, filepath, fn)
             date = time.strftime('%Y-%M-%d %H:%M', time.localtime(os.path.getmtime(fileName)))
             if os.path.isdir(fileName):
                page = page + '<tr><td valign="top"><img src="'+folderIcon+'" alt="[FILE]"></td><td>\n<a href="'+ fn +'/">'+fn+'</a>\n</td>\n<td align="right">'+date+'  </td><td align="right"> - </td></tr>'
             else:
                size = bytesConvert(os.path.getsize(fileName))
                page = page + '<tr><td valign="top"><img src="'+fileIcon+'" alt="[FILE]"></td><td> <!-- Name -->\n<a href="'+ fn+'">'+fn+'</a>\n</td><td align="right">'+date+'  </td><td align="right">'+size+' </td></tr>\n'
       except FileNotFoundError as e:
          abort(404, "Not Found.")

       page = page + footer.format(port = port, ip = host, name = serverName)
       return page

def bytesConvert(inBytes):
    if inBytes < 0:
        return '-'
    step = 1024.
    precision = 1
    units = ['bytes','KB','MB','GB','TB']
    for i in range(len(units)):
        if (inBytes / step) >= 1:
            inBytes /= step
            inBytes = round(inBytes, precision)
        else:
            return str(inBytes) + ' ' + units[i]

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

def main():
    global serverRoot
    global serverName
    global rootFolder
    global port
    global host
    global noUpload
 
    if os.path.isfile('config.ini'):
        import configparser
        config = configparser.ConfigParser()
        config.read('config.ini')
        port = config['DEFAULT']['Port']
        host = config['DEFAULT']['ip']
        serverRoot = config['DEFAULT']['serverRoot']
        serverName = config['DEFAULT']['serverName']
        noUpload = config['DEFAULT']['noUpload']
        if noUpload.lower() == "false":
           noUpload = False
        else:
           noUpload = True
    else:
        parser = argparse.ArgumentParser(prog=os.path.splitext(os.path.basename(__file__))[0])
        cwd = os.getcwd()
        parser.add_argument('-d', '--directory', metavar='DIRECTORY', type=read_write_directory, default=cwd,
                        help='Root directory\n'
                             '[Default=.]')
        parser.add_argument('-ip', '--host', type=str, default='0.0.0.0',
                        help='Ip to serve [Default=0.0.0.0]')
        parser.add_argument('-p', '--port', type=int, default=8080,
                        help='Port to serve [Default=8080]')
        parser.add_argument('-n', '--servername', type=str, default='My server',
                        help='Name of the server [Default=My serve]')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s v'+str(VERSION))

        parser.add_argument('--no_upload', default=False, action='store_true',
                        help='Disable the upload of files. Enabled bt deafult.')
        args = parser.parse_args()

        port = args.port
        host = args.host
        serverRoot = args.directory
        serverName = args.servername
        noUpload = not args.no_upload

    if not noUpload:
       #Changing the header to remoce the upload form
       global header
       global header_no_upload
       header = header_no_upload
       
    os.chdir(serverRoot)
    rootFolder = os.getcwd()
    print("Uploader version " + str(VERSION))
    print("\nWARNING: This is a development server. Do not use it in a production deployment.")
    run(app, host = host, port = port)


if __name__ == '__main__':
    main()

