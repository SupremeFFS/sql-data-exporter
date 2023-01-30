# sql-data-exporter

A Python program to pull SQL data from a Microsoft SQL server and export it to a CSV file. 

## How it works

sql-data-exporter pulls data from the SQL database(specified in the config.json file) and creates a file with the data in a csv format.

## How to Run Locally

Clone the repository and in the command line run: python main.py and it will pull the SQL data and create a file specified in the config.json. 

## Example config, anything after the # are comments
```json
{
    "DATABASE": {
        "USERNAME": "username",                         #SQL Username
        "PASSWORD": "password",                         #SQL Password
        "HOST": "host_ip",                              #SQL Server IP
        "NAME": "datbase_name",                         #SQL Database Name
        "VIEW_NAME": "table_name",                      #SQL View Name or Table Name
    },
    "GENERAL": {
        "EXPORT_DIRECTORY": "/export/directory/",       #Directory to export the file to and it MUST end in a forward slash
        "FILE_EXT": ".csv",                             #Can be .csv or .txt
        "DELIMITER":",",                                #Column delimiter
        "DATE_FORMAT": "%m-%d-%Y-%H%M%S",               #Date format
        "FILE_NAME": "new_file_name"                    #Filename of the file to export
    },
    "SFTP": {
        "ENABLED": false,                               #Whether or not to enable SFTP upload
        "HOST": "",                                     #SFTP host IP or DNS address to connect to
        "USERNAME": "",                                 #SFTP username                              
        "PASSWORD": "",                                 #SFTP password
        "UPLOAD_DIRECTORY": ""                          #SFTP upload directory
    }
}
```