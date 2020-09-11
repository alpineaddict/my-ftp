#!/usr/bin/env python

# Reset Running and Connecting variables to ensure program loop
# Import libraries
Running = True
Connecting = True
import ftplib
from ftplib import FTP


# Connect to FTP server
def FTP_Connect(ftpserv,username,password):
    global Running
    global Connecting
    global ftp

    while Connecting:
        # Attempt connection and report result
        try: 
            ftp = FTP(ftpserv)
            login = ftp.login(username,password)
            print("Status: " + login)
            if 'success' in login:
                Connecting = False
            else:
                retry = input("Connection failed. Try again? Y or N: ".lower())
                while True: 
                    if 'y' in retry: 
                        continue
                    elif 'n' in retry: 
                        ("Terminating program. Goodbye")
                        Running = False
                        Connecting = False
                        break
                    else: 
                        print("Please choose Y or N!")
                        continue

        # Raise ERROR exceptions and return to top of loop                
        except ftplib.ERROR_perm:
            print("Incorrect username! Must use 'anonymous'.")
            continue
        except ftplib.all_ERRORs as e:
            ERRORcode_string = str(e)
            print(ERRORcode_string)
            continue


# Upload testing
def upload_test():
    ftpserv = 'speedtest.tele2.net'
    username = 'anonymous'
    password = 'a'
    test_file_path = '/home/ross/Desktop/text.txt'
    test_ftp_path  = 'upload'
    test_new_file_name = 'yes.txt'

    FTP_Connect(ftpserv,username,password)

    # Change directory to FTP path
    print("Current directory: " + ftp.pwd())
    ftp.cwd('/')
    ftp.cwd(test_ftp_path)
    print("Directory changed: {}".format(ftp.pwd()))
    
    # Attempt file upload
    print("\nAttempting file upload...\n")
    with open(test_file_path,'rb') as fh:
        upload = ftp.storbinary('STOR ' + test_new_file_name, fh)
        print(upload)
    # ftp.storlines('STOR ' + test_new_file_name, fh)


# Download testing
def download_test():
    ftpserv = 'speedtest.tele2.net'
    username = 'anonymous'
    password = 'a'
    dl_file_name = '100KB.zip'
    local_file_path = '/home/ross/Desktop/'
    new_file_name = '100KB-crazy2.zip'
    new_file_name = local_file_path + new_file_name

    FTP_Connect(ftpserv,username,password)

    # Download file to desktop
    print("\nAttempting file download...\n")
    print("Attempting to download {} as {}.".format(dl_file_name,new_file_name))
    with open(new_file_name,'wb') as fh:
        download = ftp.retrbinary('RETR ' + dl_file_name, fh.write)
        print(download)    


# Upload func
def Upload():
    '''
    Receive input from user for local file path, remote FTP path and desired filename.
    User can choose to upload additional files.
    '''
    Uploading = True
    
    while Uploading: 
        # Print out requirements
        print("=========== UPLOAD ===========")
        print("Please specify FTP remote target path, source file path " +
              "and target name.")
        print("\nFTP REQUIREMENTS:")
        print(" - Files must be uploaded to 'upload' folder.")
        print(" - New folders cannot be created.\n")

        # Prompt for local file path, FTP path and new filename 
        local_file_path = input("File path (Local): ")    
        ftp_path  = input("FTP  path (Remote): ")
        new_file_name = input("New file name (Ex: lines.txt): ")

        # Change directory to FTP path
        print("Current directory: " + ftp.pwd())
        ftp.cwd('/')
        ftp.cwd(ftp_path)
        print("Directory changed: {}".format(ftp.pwd()))
        
        # Attempt file upload
        try: 
            print("\nAttempting file upload...\n")
            with open(local_file_path,'rb') as fh:
                upload = ftp.storbinary('STOR ' + new_file_name, fh)
                #fh = open(local_file_path,'r')   # had to switch to binary??
                #upload = ftp.storlines('STOR ' + new_file_name, fh)
                if 'Transfer complete' in upload:
                    print("File uploaded successfully!")
                    print(upload)
                else: 
                    print("Sorry, upload failed.")
                    print(upload)
        except FileNotFoundError:
            print("\nERROR! Path not found or is invalid. Please " +
                  "correct your file path and try again.")                    
        except ftplib.all_ERRORs as e:
            ERRORcode_string = str(e)
            print(ERRORcode_string)
            
        # Prompt for another upload or exit 
        while True: 
            retry = input("\n\nWould you like to upload another file? \nY or N: ").lower()
            if 'y' in retry: 
                break
            elif 'n' in retry:
                print("\nExiting upload module.")
                Uploading = False
                break
            else: 
                print("Please choose Y or N!")
                continue
        continue


# Download func    
def Download():
    '''
    Receive input from user for FTP server address.
    Receive input from user for a file path to download from FTP server. 
    '''
    
    Downloading = True  
    
    while Downloading:
        
        # Print out requirements
        print("========== DOWNLOAD ==========")
        print("Please specify FTP server download source address, download source" +
              "path and target file path.")
        print("\nFTP REQUIREMENTS:")
        print(" - Local file path must be full path, including backslash (/) at " +
             "the end.\n   Example: /home/username/Desktop/")

        # List directory contents
        ftp.cwd('/')
        print("Current directory: " + ftp.pwd())
        print("\nPlease review contents of root directory (/) for file to download.")
        ftp.retrlines('LIST')
        print("\n")

        # Prompt for download file name, local path & new file name
        dl_file_name    = input("File name to download: ")
        local_file_path = input("Target local directory: ")
        if local_file_path[-1:] != '/':       # add '/' to filename if it isn't there
            local_file_path = local_file_path + '/'
        new_file_name   = input("New file name (Ex: lines.txt): ")
        new_file_name   = local_file_path + new_file_name

        # Attempt download
        try:
            print("\n\n===============================")
            print("Attempting download...")
            with open(new_file_name,'wb') as fh:
            #fh = open(new_file_name,'wb')
                download = ftp.retrbinary('RETR ' + dl_file_name, fh.write)
                if 'Transfer complete' in download:
                    print("Download successful!")
                    print(download)
                else: 
                    print("Sorry, download failed.")
        except FileNotFoundError:
            print("\nERROR! File not found or path is invalid. Please " +
                  "correct your file path and try again.")
        except ftplib.all_ERRORs as e:
            ERRORcode_string = str(e)
            print(ERRORcode_string)
            
        # Prompt for another download  or exit
        while True: 
            retry = input("\n\nWould you like to download another file? \nY or N: ")
            if 'y' in retry.lower():
                print("\n")
                break
            elif 'n' in retry.lower():
                print("\nExiting download module.")
                Downloading = False
                break
            else: 
                print("Please choose Y or N!")
                continue
        continue 


####################
##  Run Program  ##
##################
def main():
    '''
    Run main bit of application via FTPx.py.
    '''    
    Running = True

    while Running:
        # Welcome user, display intro
        print("=========== FTPx ============")
        print("      Welcome to FTPx.\n")
        print("FTPx is an FTP program that can be used to \n" + 
                "upload and download files from an FTP server.")

        # Prompt for FTP address
        print("\n\n========== CONNECT ==========")
        print("FTP REQUIREMENTS:")
        print(" - FTP address does not need prefix \"https://\"")
        print(" - FTP default port is 21.")
        print(" - If custom port is needed please add suffix" +
            "\n   (ex www.domainftp.org:69)")
        ftpserv = input("\nFTP Server Address: ")

        # Prompt for credentials
        print("\n\n========== LOGIN ===========")
        username = input("Please enter username: ")
        password = input("Please enter password: ")    
        print("\n\n==============================")
        print("Attempting to connect to FTP server...")

        # Attempt connection and login
        FTP_Connect(ftpserv,username,password)

        # Display option menu 
        while True:
            try: 
                print("\n\n=========== OPTIONS ===========")
                print("Choose an option")
                print("1. Upload\n2. Download\n3. Exit\n")
                option = int(input("Enter a number: "))
                print("\n")

                if option == 1:
                    Upload()            
                elif option == 2:          
                    Download()
                elif option == 3:
                    print("============ EXIT =============")
                    print("Terminating program...")
                    print("Connection status: {}".format(ftp.quit()))
                    Running = False
                    break            
                else: 
                    print("ERROR! Please choose a number option between 1 and 3!")

            except ValueError: 
                print("ERROR! Value must be an integer!\n")
                continue





if __name__ == '__main__':
    print("Constants used for testing.")
    print("ftpserv = speedtest.tele2.net\nusername = anonymous\npassword = a\nFile used" +
        " for testing: /home/ross/Desktop/text.txt\n\n")
    FTPxSub.main()