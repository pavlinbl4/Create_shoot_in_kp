import ftplib
import os
from dotenv import load_dotenv


class FTPClient:
    HOST = 'ftp.kommersant.ru'
    FTP_DIR = "/PHOTO/INBOX/SHOOTS/Pavlenko_Evgenij_2571"

    def __init__(self, shoot_id):
        load_dotenv()
        self.ftp_login = os.environ.get('FTP_LOGIN')
        self.ftp_pass = os.environ.get('FTP_PASS')
        self.shoot_id = shoot_id
        self.ftp = ftplib.FTP(self.HOST, self.ftp_login, self.ftp_pass, timeout=1)

    def connect(self):

        self.ftp.encoding = "cp1251"
        self.ftp.cwd(self.FTP_DIR)

    def make_dir(self):
        try:
            self.connect()
            self.ftp.mkd(self.shoot_id)
            print("Directory created")
        except ftplib.error_perm:
            print("Directory already exists")
        finally:
            self.list_dir()

    def list_dir(self):
        print(self.ftp.retrlines('LIST'))
        self.ftp_close()

    def ftp_close(self):
        self.ftp.quit()


if __name__ == '__main__':
    FTPClient('shoot_id').make_dir()
