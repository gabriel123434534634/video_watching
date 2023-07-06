from json import dump, load
from json.decoder import JSONDecodeError
import re, random
import time as time2
time2.localtime2 = time2.localtime
import email
import smtplib
class time:
    class localtime:
        def __init__(self):    
            self.tm_year = time2.localtime2().tm_year
            self.tm_mon = time2.localtime2().tm_mon
            self.tm_mday = time2.localtime2().tm_mday
            self.tm_hour = time2.localtime2().tm_hour
            self.tm_min = time2.localtime2().tm_min
            self.tm_sec = time2.localtime2().tm_sec
            self.tm_wday = time2.localtime2().tm_wday
            self.tm_yday = time2.localtime2().tm_yday
            self.tm_ysec = (86400*self.tm_yday)+(60*60*self.tm_hour)+(60*self.tm_min)+self.tm_sec
    class convert:
        def organize_ysec(organize):
            ysec = organize[0]
            year = organize[1]
            if ysec > 31536000:
                year = (ysec//31536000)+year
                ysec = ysec%31536000
                return [ysec, year]
            else:
                return [ysec, year]
        def organize_to_string(organize, shorting=False):
            ysec = organize[0]
            meses = [
                31, 28,31,30,31,30,31,30,31,30,31,30
            ]
            mês = 0
            ysec2 = ysec
            for i in range(0, len(meses)):
                temp = 60*60*24*meses[i]
                if ysec2 - temp <= 0:
                    mês = i
                    if mês < 0:
                        mês = 0
                    break
                else:
                    ysec2 -= temp
            mday = ysec//86400
            yday = mday
            temp = 0
            for i in range(0, mês):
                temp += meses[i]
            mday -= temp
            hora = ((ysec-(60*60*24*yday))//60)//60
            minuto = (ysec-((60*60*24*yday+(60*60*hora))))//60
            if shorting == True:
                mês -= 1
            # if mday == 0:
            #     mês -= 1
            #     mday = meses[mês]
            segundos = ysec-((86400*yday)+(3600*hora)+(60*minuto))
            return {"segundo":segundos, "minuto": minuto, "hora":hora, "dia":mday, "mês":mês+1, "ano":organize[1]}
def convert(number, limit=None):
    if type(number) == int:
        if "-" in str(number):
            add = "-"
        elif "+" in str(number):
            add = "+"
        else:
            add = ""
        number = str(number)
        number = number.replace("+", "")
        number = number.replace("-", "")
        number = number.split(sep=".")
        number[0] = number[0][::-1]
        number[0] = re.sub("([0-9][0-9][0-9])", "\\1,", number[0])[::-1]
        if number[0][0] == ",":
            number[0] = number[0][1:]
        return add+number[0]
    if type(number) == float:
        if limit != None:
            number = float(eval("""f"{number:.?!f}" """.replace("?!", str(limit))))
        if "-" in str(number):
            add = "-"
        elif "+" in str(number):
            add = "+"
        else:
            add = ""
        number = str(number)
        number = number.replace("+", "")
        number = number.replace("-", "")
        number = number.split(sep=".")
        number[0] = number[0][::-1]
        number[0] = re.sub("([0-9][0-9][0-9])", "\\1,", number[0])[::-1]
        if number[0][0] == ",":
            number[0] = number[0][1:]
        return add+number[0]+"."+number[1]
    if type(number) ==  str:
        number = str(number).replace(",", "")
        if "." in number:
            return float(number)
        else:
            return int(number)
def generate_ascii_code(amount=random.randint(50, 100)):
    a = "a s d f g h j k l  z x c v b n m".split()
    b = ""
    for i in range(0, amount-1):
        b += random.choice(a)
    return b
class json_firebase:
    def __init__(self, file_credentials, db_id, filename, backup=[False, "root"]):
        self.file_credentials = file_credentials
        self.db_id = db_id
        self.filename = filename
        import firebase_admin
        from firebase_admin import storage
        from firebase_admin import credentials 
        import os
        self.backup = backup
        self.cred = credentials.Certificate(file_credentials)
        try:
            app = firebase_admin.get_app()
        except:
            cred = credentials.Certificate(self.file_credentials)
            firebase_admin.initialize_app(self.cred, {
                "storageBucket": self.db_id
            })
        bd = storage.bucket().blob(filename).download_as_bytes()
        file = "oycbt7rygkjhbaieuycfefiaudsgfiuydnkfjhzboudfygao87ertoq83yufgahdkcnkdyvgeuft97qegfydasvkchadiuvatweouf.json"
        open(file, "wb").write(bd)
        try:
            self.data = load(open(file, encoding="utf-8"))
        except JsonDecodeError:
            os.remove(file)
            raise JsonDecodeError(f"invalid file to interpret: {filename}")
        os.remove(file)
    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
    def keys(self):
        return self.data.keys()
    def __delitem__(self, key):
        del self.data[key]
    def __str__(self):
        return str(self.data)
    def up(self):
        import firebase_admin
        from firebase_admin import storage
        from firebase_admin import credentials 
        import os
        if self.backup[0] == True:
            file_backup = self.backup[1]+generate_ascii_code(amount=1000)+".json"
            try:
                app = firebase_admin.get_app()
            except:
                cred = credentials.Certificate(self.file_credentials)
                firebase_admin.initialize_app(self.cred, {
                    "storageBucket": self.db_id
                })
            bd = storage.bucket().blob(self.filename).download_as_bytes()
            file = "oycbt7rygkjhbaieuycfefiaudsgfiuydnkfjhzboudfygao87ertoq83yufgahdkcnkdyvgeuft97qegfydasvkchadiuvatweouf.json"
            open(file, "wb").write(bd)
            try:
                data_backup = load(open(file, encoding="utf-8"))
                dump(data_backup, open(file, "w", encoding="utf-8"), ensure_ascii=False)
                from datetime import datetime
                storage.bucket().blob(self.backup[1]+str(datetime.now()).replace(":", ".")).upload_from_filename(file)
            except Exception as error:
                os.remove(file)
                print(error)
            os.remove(file)

        file = "oycbt7rygkjhbaieuycfefiaudsgfiuydnkfjhzboudfygao87ertoq83yufgahdkcnkdyvgeuft97qegfydasvkchadiuvatweouf.json"
        dump(self.data, open(file, "w", encoding="utf-8"), ensure_ascii=False)
        storage.bucket().blob(self.filename).upload_from_filename(file)
        os.remove(file)
        
class json:
    def __init__(self, file, backup=[False, "Backup"], versionUP=1):
        self.version = None
        self.versionUP = versionUP
        self.data = load(open(file, "r", encoding="utf-8"))
        self.file = file
        self.backup = backup
    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
        
    def up(self):
        backup = self.backup
        if backup == True:
            backup = [True, str(self.file[0:len(self.file)-5])+"_backup"]
        if backup[0] == True:
            try:
                self.version = load(open("%s/version.json"%(str(self.file[0:len(self.file)-5])+"_backup"), "r", encoding="utf-8"))["version"]
            except FileNotFoundError:
                self.version = -1*self.versionUP+1
            try:
                dump({"version":self.version+self.versionUP}, open("%s/version.json"%(backup[1]), "w", encoding="utf-8"))
                self.version += self.versionUP
                dump(self.data, open("%s/%s_%s.json"%(backup[1],self.file,float(self.version)), "w",encoding="utf-8"), ensure_ascii=False)
            except FileNotFoundError:
                from os import system
                self.version += self.versionUP
                system("mkdir %s"%(backup[1]))
                dump(self.data, open("%s/%s_%s.json"%(backup[1],self.file,float(self.version)), "w",encoding="utf-8"), ensure_ascii=False)
                dump({"version":self.version}, open("%s/version.json"%(backup[1]), "w", encoding="utf-8"))
        dump(self.data, open(self.file, "w", encoding="utf-8"), ensure_ascii=False, indent=4)
        del backup
    def keys(self):
        return self.data.keys()
    def __delitem__(self, key):
        del self.data[key]
    def __str__(self):
        return str(self.data)
class sprite:
    def __init__(self, screen,delay=[None, 0]):
        import pygame
        self.delay = delay
        self.screen = screen
        self.images = []
        self.position = [0,0]
        self.frame = 0
    def update(self):
        if self.delay[0] != None:
            if self.frame >= len(self.images)-1:
                self.frame = 0
            self.frame += 1
        self.screen.blit(self.images[self.frame], self.position)
class spriteGroup:
    def __init__(self, sprites):
        self.sprites = sprites
    def draw(self):
        for i in self.sprites:
            i.update()

class gmail():
    def __init__(self, gmail, password, css_files=[], image_files=[], smtp_server="smtp.gmail.com", smtp_port=587, profile_picture_url=""):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.msg = email.message.Message()
        self.msg['From'] = gmail
        self.password = password
        self.msg.add_header('Content-Type', 'text/html')
        self.profile_picture_url = profile_picture_url
        if self.profile_picture_url != "":
            self.msg.add_header('X-Image-Url', self.profile_picture_url)
        if len(css_files) != 0:
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            for i in css_files:
                f = open(i, "rb")
                # set attachment mime and file name, the image type is png
                mime = MIMEBase('stylesheet', 'css', filename=i)
                # add required header data:
                mime.add_header('Content-Disposition', 'attachment', filename=i)
                mime.add_header('X-Attachment-Id', '0')
                mime.add_header('Content-ID', '<0>')
                # read attachment file content into the MIMEBase object
                mime.set_payload(f.read())
                # encode with base64
                encoders.encode_base64(mime)
                # add MIMEBase object to MIMEMultipart object
                msg.attach(mime)
        if len(image_files) != 0:
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            for i in image_files:
                f = open(i, "rb")
                # set attachment mime and file name, the image type is png
                mime = MIMEBase('image', 'png', filename=i)
                # add required header data:
                mime.add_header('Content-Disposition', 'attachment', filename=i)
                mime.add_header('X-Attachment-Id', '0')
                mime.add_header('Content-ID', '<0>')
                # read attachment file content into the MIMEBase object
                mime.set_payload(f.read())
                # encode with base64
                encoders.encode_base64(mime)
                # add MIMEBase object to MIMEMultipart object
                msg.attach(mime)
    def send_email(self, Subject, Reciver, Body):
        self.msg.set_payload(Body )
        self.msg['Subject'] = Subject
        self.msg['To'] = Reciver
        self.msg.add_header('Content-Type', 'text/html')
        s = smtplib.SMTP(f'{self.smtp_server}: {self.smtp_port}')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(self.msg['From'], self.password)
        s.sendmail(self.msg['From'], [self.msg['To']], self.msg.as_string().encode('utf-8'))
        print('Email enviado')
def enviar_email(): 
    corpo_email = "<p>Testando, olá</p>"

    msg = email.message.Message()
    msg['Subject'] = 'testando'
    msg['From'] = 'republica.democratica.de.sigma@gmail.com'
    msg['To'] = 'fiuzagabri@gmail.com'
    password = '$Nucalaca23?$'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')
def upload_file_to_firebase(file_name, file_credentials, db_id, new_file_name=None):
    if new_file_name == None:
        new_file_name = file_name
    import firebase_admin
    from firebase_admin import storage
    from firebase_admin import credentials 
    import os
    cred = credentials.Certificate(file_credentials)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {
            "storageBucket": db_id
        })
     
    storage.bucket().blob(new_file_name).upload_from_filename(file_name)
    
def download_file_from_firebase(file_name, file_credentials, db_id, new_file_name=None):
    if new_file_name == None:
        new_file_name = file_name
    import firebase_admin
    from firebase_admin import storage
    from firebase_admin import credentials 
    import os
    cred = credentials.Certificate(file_credentials)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {
            "storageBucket": db_id
        })
     
    bd = storage.bucket().blob(file_name).download_as_bytes()
    open(new_file_name, "wb").write(bd)
def delete_file_from_firebase(file_name, file_credentials, db_id):
    import firebase_admin
    from firebase_admin import storage
    from firebase_admin import credentials 
    import os
    cred = credentials.Certificate(file_credentials)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {
            "storageBucket": db_id
        })
     
    bd = storage.bucket().blob(file_name).delete()

