import csv
import json
import pymssql
import os
import datetime
import pysftp
# The multiple prints are for redirecting it to a log file when executed in cron.
class Config():
    def get_config():
        try:
            current_directory = os.getcwd()
            with open(f'{current_directory}/config.json', 'r') as config:
                config = json.load(config)
            return config
        except Exception as e:
            print(str(date) + " - " + "Error loading config")
            print("Exception: " + str(e));

class SQL():
    def get_sql_data():
        try:
            print(str(date) + " - " + "Connecting to database")
            with pymssql.connect(host=f'{config["DATABASE"]["HOST"]}', user=f'{config["DATABASE"]["USERNAME"]}', database=f'{config["DATABASE"]["NAME"]}', password=f'{config["DATABASE"]["PASSWORD"]}') as conn:
                cursor = conn.cursor(as_dict=True)
            return cursor
                
        except Exception as e:
            print(str(date) + " - " + "Error getting SQL data from database")
            print("Exception: " + str(e));
            
    def create_csv_file(cursor):
        try:
            print(str(date) + " - " + "Getting SQL data from database")
            cursor.execute(f'SELECT * FROM [{config["DATABASE"]["NAME"]}].[dbo].[{config["DATABASE"]["VIEW_NAME"]}]')
            with open(f'{config["GENERAL"]["EXPORT_DIRECTORY"] +  config["GENERAL"]["FILE_NAME"] + str(formated_date) + config["GENERAL"]["FILE_EXT"]}', 'w', newline='') as roster_file:
                columns = [column[0] for column in cursor.description]
                data = cursor.fetchall()
                writer = csv.DictWriter(roster_file, fieldnames=columns, delimiter=f'{config["GENERAL"]["DELIMITER"]}')
                for row in data:
                    writer.writerow(row)
            print(str(date) + " - " + f"CSV File created")
        
        except Exception as e:
            print(str(date) + " - " + "Error getting SQL data from database")
            print("Exception: " + str(e));
            
class SFTP():
    def make_sftp_connection(hostname, username, password, filename):
        print(str(date) + " - " + "SFTP connection made")
        with pysftp.Connection(hostname, username=username, password=password) as sftp:
            return sftp
    
    def upload_files(sftp, filename):
        print(str(date) + " - " + "Change directory to root /")
        sftp.cd('/')
        print(str(date) + " - " + "Uploading file to SFTP server")
        sftp.put(filename)
        print(str(date) + " - " + "Done uploading file to SFTP server")

    
    def deleteLocalUploadedFiles(file):
        print(str(date) + " - " + "Deleting local file")
        os.remove(file)
            
if __name__ == '__main__':
    config = Config()
    config = config.getConfig()
    date = datetime.datetime.now()
    formated_date = date.strftime(config["GENERAL"]["DATE_FORMAT"])
    file_name = config["GENERAL"]["EXPORT_DIRECTORY"] +  config["GENERAL"]["FILE_NAME"] + str(formated_date) + config["GENERAL"]["FILE_EXT"]
    sql = SQL()
    data = sql.get_sql_data()
    csv_file = sql.create_csv_file(data)
    if config["SFTP"]["ENABLED"] == True:
        sftp_hostname = config["SFTP"]["HOST"]
        sftp_username = config["SFTP"]["USERNAME"]
        sftp_password = config["SFTP"]["PASSWORD"]
        SFTP.makeSftpConnectionAndUploadFiles(sftp_hostname, sftp_username, sftp_password, file_name)
        SFTP.deleteLocalUploadedFiles(file_name)