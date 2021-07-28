from ftplib import FTP
from getpass import getpass
from PIL import Image
import pytesseract
import os
from sys import platform


class ServerFTP:
    def __init__(self, host='127.0.0.1', user='robert', passwd='shainny35993599', acct=''):
        self.host = host
        self.user = user
        self.password = passwd
        self.acct = acct
        self.server = FTP(self.host, self.user, self.password, self.acct)
        self.path_default = f"{os.getcwd()}{ os.sep}images"
        if not os.path.isdir(self.path_default):
            os.mkdir(self.path_default)

    def login(self):
        self.server.login(self.user, self.password, self.acct)
        print('Login exitoso')

    def download(self, fullpath: str):
        p = f"temp/{fullpath.split(os.sep)[-1]}"  
        f = open(p, 'wb')
        with f as fp:
            self.server.retrbinary(f'RETR {fullpath}', fp.write)
        return self.handle_dirs(self.process_image(p), p)
    
    def process_image(self, file):
        custom_config = r'--oem 3 --psm 6 outputbase digits'
        return pytesseract.image_to_string(Image.open(file), config=custom_config).split('\n')[0]


    def handle_dirs(self, namedir, pathimage):
        basedir = f"{self.path_default}{os.sep}{namedir}"
        if not os.path.isdir(basedir):
            os.mkdir(basedir) 
        if platform == 'win32':
            os.system(f'copy {pathimage} {basedir}')            
        if platform == 'linux' or platform == 'linux2':
            os.system(f'cp {pathimage} {basedir}')
        self.rename_all_file(basedir)

        return basedir
    
    def rename_all_file(self, path):
        new_name = os.path.basename(path)
        os.chdir(path)
        for f in os.listdir(path):
            os.rename(f, f"{new_name}.{f.split('.')[-1]}")


print('*-----Bienvenido-----*')

host, user, passwd = input('host: '), input('user: '), getpass('password: ')
session = ServerFTP(host, user, passwd)
session.login()

file_to_download = input('Ruda la imagen dentro del servidor: ')
path = session.download(file_to_download)
print('Imagen procesada exitosamente...')
print(f'Leyendo directorio: {os.path.basename(path)}')
for i in os.listdir(path):
    print(i)
