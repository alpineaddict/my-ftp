#!/usr/bin/env python

'''
Small FTP program used for testing to upload and download files.
Specifically designed to work with speedtest.tele2.net.
'''

import ftplib
import os
import sys
import constant

# TODO: add retry option for upload/download for more files
# TODO: finish up menu loop option

def userWelcome():
    '''
    Welcome user and present FTP information.
    '''

    print("=" * 11 + " My_FTP " + "=" * 11)
    print("      Welcome to My_FTP.")
    print("My_FTP is an FTP program that can be used to \n"
            "upload and download files from a test FTP server.")
    print("My_FTP cannot delete any files from test FTP server.")
    print("=" * 10 + " CONSTANTS " + "=" * 10)
    print("Username: anonymous")
    print("Passowrd: a")
    print("FTP Server: speedtest.tele2.net")
    print("=" * 30)

def itemMenu():
    '''
    Prompt user with an item menu and issue class functions accordingly.
    Promp user for choice to re-run through file upload/download again. 
    '''
    pass

class MyFTP():
    '''
    Build out an FTP object to interact with FTP server at speedtest.tele2.net
    MyFTP object can upload local files and/or download files locally.
    '''

    def __init__(self, FTP_SERVER, USERNAME, PASSWORD):
        self.FTP_SERVER = FTP_SERVER
        self.USERNAME   = USERNAME
        self.PASSWORD   = PASSWORD

        try:
            print("Attempting to connect to FTP server...")
            self.ftp_object = ftplib.FTP(FTP_SERVER)
            self.login = self.ftp_object.login(self.USERNAME, self.PASSWORD)
            print("Status: " + self.login)
        except ftplib.all_errors as e:
            error_code_string = str(e)
            print(error_code_string)
            print("Terminating program. Goodbye!")
            sys.exit()

    def directoryExistCheck(self, local_file_path):
        '''
        Check to see whether or not directory exists. Return bool val
        for condition. Will be used to determine whether or not to proceed
        to file upload or download.
        '''
        self.local_file_path = local_file_path
        if os.path.exists(self.local_file_path):
            return True

    def uploadPrompt(self):
        '''
        Prompt user for information needed for FTP file upload.
        '''

        print("=" * 11 + " UPLOAD " + "=" * 11)
        print("FTP REQUIREMENTS:")
        print(" - Files will be uploaded to /upload/ directory.")
        print(" - New folders cannot be created.")
        self.ftp_object.cwd("/upload")
        self.local_file_path = input("Full file path (Local): ")
        self.new_file_name = input("New file name (Ex: lines.txt): ")

    def uploadFile(self):
        '''
        Attempt to upload file to FTP.
        '''
        if self.directoryExistCheck(self.local_file_path):
            try:
                print("Attempting file upload...")
                with open(self.local_file_path,'rb') as fh:
                    self.file_upload = self.ftp_object.storbinary(
                        "STOR " + self.new_file_name, fh)
                    if "Transfer complete" in self.file_upload:
                        print("File uploaded successfully!")
                        print("Status: " + self.file_upload)
                    else:
                        print("Sorry, upload failed. Try again.")
                        print(self.file_upload)
            except ftplib.all_errors as e:
                error_code_string = str(e)
                print(error_code_string)
        else:
            print("ERROR! Path does not exist locally.")

    def downloadPrompt(self):
        '''
        Prompt user for information needed for FTP file download.
        '''

        print("=" * 10 + " DOWNLOAD " + "=" * 10)
        self.ftp_object.cwd('/')
        print("Please specify file to download, local target directory and new"
            " filename.")
        print("Current directory: /")
        print("Please review contents of root directory for file to download.")
        self.ftp_object.retrlines("LIST")
        self.download_file_name = input("File name to download: ")
        self.local_file_path = input("Target local directory: ")
        if self.local_file_path[-1] != "/":
            self.local_file_path += "/"
        self.new_file_name = input("New file name (Ex: newLines.txt): ")
        self.new_file_name = self.local_file_path + self.new_file_name

    def downloadFile(self):
        '''
        Attempt to download file from FTP to local repository.
        '''
        if self.directoryExistCheck(self.local_file_path):
            try:
                print("Attempting file download...")
                with open(self.new_file_name,"wb") as fh:
                    self.file_download = self.ftp_object.retrbinary(
                        "RETR " + self.download_file_name, fh.write)
                    if "Transfer complete" in self.file_download:
                        print("Download successful!")
                        print("Status: " + self.file_download)
                    else:
                        print("Sorry, download failed. Try again.")
                        print(self.file_download)
            except ftplib.all_errors as e:
                error_code_string = str(e)
                print(error_code_string)
        else:
            print("ERROR! Path does not exist locally.")

if __name__ == "__main__":
    userWelcome()
    my_ftp_connection = MyFTP(
        constant.FTP_SERVER,
        constant.USERNAME,
        constant.PASSWORD)
    my_ftp_connection.uploadPrompt()
    my_ftp_connection.uploadFile()
    my_ftp_connection.downloadPrompt()
    my_ftp_connection.downloadFile()
