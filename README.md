# Simple http server
All scripts are wirent in pure python no other frameworks execpt [bottle framework](https://github.com/bottlepy/bottle).
You do not need to install the framework, only download the bottle.py file and put it in the same folder.
If multi-threading is needed to serve several users at once, a support for paste http server is added [Paste](https://github.com/pasteorg/paste).
  
- server.py
- uploader.py
- downloader.py
- builder.py

***server.py***
This list the files all in one file. You can disable the upload.
The server can be configured with ini file. Check config.ini for sample config.  
Or using comand line arguments.  
  
<pre>
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Root directory [Default=.]
  -ip HOST, --host HOST
                        Ip to serve [Default=0.0.0.0]
  -p PORT, --port PORT  Port to serve [Default=8080]
  -n SERVERNAME, --servername SERVERNAME
                        Name of the server [Default=My serve]
  -v, --version         show program's version number and exit
  --no_upload           Disable the upload of files. Enabled bt deafult.
</pre>
***uploader.py***
This script uploads the folder/file to the webserver.  
In the jeader above the table with the content, there are 2 links for the downloader and uploader  
  
<pre>
  -h, --help            show this help message and exit
  -ip HOST, --host HOST
                        Ip addres or FQDN of the server to download
  -p PORT, --port PORT  Port of the server [Default=80]
  -t TYPE, --type TYPE  Select the type of cenection http/https [Default=http]
  -uf UPLOAD_FOLDER, --upload_folder UPLOAD_FOLDER
                        Path to upload the files
  -lf LOCAL_FOLDER, --local_folder LOCAL_FOLDER
                        Path to the folder for upload
  -w WAIT_TIME, --wait_time WAIT_TIME
                        Time between each download in seconds [Default=5]
  -v, --version         show program's version number and exit
</pre>
***downloader.py***
This will download the content of given folder.  
  
<pre>
  -h, --help            show this help message and exit
  -ip HOST, --host HOST
                        Ip addres or FQDN of the server to download
  -p PORT, --port PORT  Port of the server [Default=80]
  -f FOLDER, --folder FOLDER
                        Path to save the content [Default=current folder]
  -w WAIT_TIME, --wait_time WAIT_TIME
                        Time between each download in seconds [Default=5]
  -v, --version         show program's version number and exit
  -o, --old_load_bar
</pre>
***builder.py***
This will combine all the scripts to one file simpleHttpFileLister.py.  
  
<pre>
  -h, --help            show this help message and exit
  -src SOURCE_FOLDER, --source_folder SOURCE_FOLDER
                        Source folder, where the py file are stored. Default
                        is curent folder.
  -build RELEASE_FOLDER, --release_folder RELEASE_FOLDER
                        Target for the final build. Default is curent folder.
  -v, --version         show program's version number and exit
</pre>
Due to bug in the I replace all \r and \n with _r and _n. If I don't replace the special charecters.  
This leads to replacing the chars back in the simpleHttpFileLister.py.   
In the saved file some lines are missaligned. We have the following code:  
```
            print(str(WAITING_TIME - i), end = '
')
```
Instead it should be:
```
            print(str(WAITING_TIME - i), end = '\r')
```

***Versions***  
*builder v0.3*  
*downloader v0.6*  
*uploader v0.7*  
*server v3.1*  



