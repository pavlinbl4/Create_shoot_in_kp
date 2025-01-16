import ftplib
import logging
from data.get_credentials import Credentials

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_ftp_folder(shoot_id):
    ftp_login = Credentials().ftp_login
    ftp_pass = Credentials().ftp_pass
    ftp_server = 'ftp.kommersant.ru'
    timeout = 10  # Увеличен таймаут для стабильности

    try:
        ftp = ftplib.FTP(ftp_server, ftp_login, ftp_pass, timeout=timeout)
        ftp.encoding = "cp1251"
        ftp.cwd("/PHOTO/INBOX/SHOOTS/Pavlenko_Evgenij_2571")

        try:
            ftp.mkd(shoot_id)
            logging.info(f"Directory '{shoot_id}' created successfully.")
        except ftplib.error_perm as e:
            logging.error(f"Error creating directory: {e}")

        # List directory contents
        logging.info('Current directory contents:')
        ftp.retrlines('LIST')

    except ftplib.all_errors as e:
        logging.error(f"FTP error: {e}")

    finally:
        try:
            ftp.quit()
            logging.info('Disconnected from FTP server.')
        except Exception as e:
            logging.error(f"Error disconnecting from FTP server: {e}")

if __name__ == '__main__':
    create_ftp_folder('KSP_0000000')
