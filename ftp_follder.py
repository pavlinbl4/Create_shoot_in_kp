import ftplib
import os
from dotenv import load_dotenv


def create_ftp_folder(shoot_id):
    load_dotenv()

    ftp_login = os.environ.get('FTP_LOGIN')
    ftp_pass = os.environ.get('FTP_PASS')

    # noinspection PyTypeChecker
    ftp = ftplib.FTP('ftp.kommersant.ru', ftp_login, ftp_pass, timeout=1)
    ftp.encoding = "cp1251"
    ftp.cwd("/PHOTO/INBOX/SHOOTS/Pavlenko_Evgenij_2571")

    try:
        ftp.mkd(shoot_id)
        print("try")
    except ftplib.error_perm:
        print("550 Cannot create a file when that file already exists")

    finally:
        # ftp.login() # default, i.e.: user anonymous, passwd anonymous@
        '230 Guest login ok, access restrictions apply.'
        print(ftp.retrlines('LIST'))  # list directory contents

        '226 Transfer complete.'
        ftp.quit()
        '221 Goodbye.'


if __name__ == '__main__':
    create_ftp_folder('KSP_017764')
