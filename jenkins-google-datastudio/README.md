
### Purpose of the main.py script
The following main.py performs a concatenation of 7 network devices reports which creates a results.xlsx here.
The results.xlsx file should be combined with 7 columns of data from network devices.

### jenkins to gdrive migration
The above created results.xlsx is then transferred to a google drive using a gdrive transfer api script.
The credentials file has to be saved in a credentials.json(similarly) in the same drive.
The script will fetch the credentials and transfer the data to data studio to display the result in a previously existing dashboard.

#### Pre-requisites : 
1) Network whitelisting for jenkins, Gdrive.
2) Pre creation of datastudio fresh dashboard.
3) Permissions allowed for the gdrive to use a jenkins user with google id.
