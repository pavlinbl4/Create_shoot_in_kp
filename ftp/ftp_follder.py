import ftplib
from data.get_credentials import Credentials


def create_ftp_folder(shoot_id):
    ftp_login = Credentials().ftp_login
    ftp_pass = Credentials().ftp_pass

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
    create_ftp_folder('KSP_0000000')
