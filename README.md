# Simple Backupscript for Root Servers

This script can be used on a root linux server to backup mysql databases to Google Drive. Support to backup selected folders will be added as soon as possible.

### Installation

This script requires [rclone](http://rclone.org/install/). Do the following steps to use this script.

Download and setup rclone as described on their page and setup config for drive: http://rclone.org/drive/. You'll need to remember the name of the remote.

Then:
```sh
$ git clone ---
```
Add backupscript.json to the same directory as backupscript.py

```sh
{
   "PATH_CONFIG":{
      "local_backup_path":"ENTER_PATH"
   },
   "DB_CREDENTIALS":{
      "username":"ENTER_USERNAME",
      "password":"ENTER_PASSWORD",
      "host":"localhost",
      "db_names":[
         "ADD_DB_NAMES_AS_LIST"
      ]
   },
   "GDRIVE_CREDENTIALS":{
      "remote_name":"ENTER_REMOTE_NAME",
      "remote_path":"ENTER_PATH"
   }
}
```


### Todos

 - Testing
 - Check whether folder already exists in Drive
 - Write Log-File
 - Backup Folders

License
----

MIT


**Free Software, Hell Yeah!**
