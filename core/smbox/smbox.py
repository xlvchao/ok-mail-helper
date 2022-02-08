import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from core.smbox.smtp import SmtpTransport
import configparser

# 获取配置
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
conf = configparser.ConfigParser()
conf.read(os.path.join(base_dir, 'config.conf'))

attachment_path = conf.get("mailbox", "attachment_path")
illustrate_path = conf.get("mailbox", "illustrate_path")

class Smbox:

    authentication_error_message = None

    def __init__(self, hostname, username=None, password=None, ssl=True,
                 port=None, ssl_context=None, starttls=False):

        self.server = SmtpTransport(hostname, port=port, ssl=ssl,
                                    ssl_context=ssl_context, starttls=starttls)

        self.username = username
        self.password = password

        try:
            self.connection = self.server.connect(username, password)
        except smtplib.SMTPResponseException as e:
            raise smtplib.SMTPResponseException(e.smtp_code, e.smtp_error)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.connection.quit()

    def is_contain_chinese(self, check_str):
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def send_mail(self, sender, receivers, mail_subject, mail_content, cc=None, bcc=None, attachment_names=None, illustrate_names=None):
        receivers = str(receivers).split(',')

        attachment_name_list = []
        if attachment_names != None:
            attachment_name_list = str(attachment_names).split(',')
        illustrate_name_list = []
        if illustrate_names != None:
            illustrate_name_list = str(illustrate_names).split(',')

        if len(attachment_name_list)==0 and len(illustrate_name_list)==0:
            message = MIMEText(mail_content, 'html', 'utf-8')
            message['From'] = sender
            message['To'] = ','.join(receivers)
            message['Subject'] = mail_subject

            if cc != None:
                cc = str(cc).split(',')
                receivers.extend(cc)
                message['Cc'] = ','.join(cc)
            if bcc != None:
                bcc = str(bcc).split(',')
                receivers.extend(bcc)
                message['Bcc'] = ','.join(bcc)

            try:
                self.connection.sendmail(sender, receivers, message.as_string())
                return True
            except smtplib.SMTPException:
                return False

        if len(attachment_name_list) != 0 and len(illustrate_name_list) == 0:
            # 创建一个带附件的实例
            message = MIMEMultipart()
            message['From'] = sender
            message['To'] = ','.join(receivers)
            message['Subject'] = mail_subject

            if cc != None:
                cc = str(cc).split(',')
                receivers.extend(cc)
                message['Cc'] = ','.join(cc)
            if bcc != None:
                bcc = str(bcc).split(',')
                receivers.extend(bcc)
                message['Bcc'] = ','.join(bcc)

            # 邮件正文内容
            message.attach(MIMEText(mail_content, 'html', 'utf-8'))

            # 构造附件
            for attach_name in attachment_name_list:
                if self.is_contain_chinese(attach_name):
                    attach = MIMEText(open(attachment_path + "/" + attach_name, 'rb').read(), 'base64', 'utf-8')
                    attach["Content-Type"] = 'application/octet-stream'
                    attach.add_header("Content-Disposition", "attachment", filename=("gbk", "", attach_name))
                    message.attach(attach)
                else:
                    attach = MIMEText(open(attachment_path + "/" + attach_name, 'rb').read(), 'base64', 'utf-8')
                    attach["Content-Type"] = 'application/octet-stream'
                    attach["Content-Disposition"] = 'attachment; filename="' + attach_name + '"'
                    message.attach(attach)

            try:
                self.connection.sendmail(sender, receivers, message.as_string())
                for attach_name in attachment_name_list:
                    my_file = attachment_path + "/" + attach_name
                    if os.path.exists(my_file):
                        os.remove(my_file)
                return True
            except smtplib.SMTPException:
                return False

        if len(attachment_name_list) == 0 and len(illustrate_name_list) != 0:
            # 创建一个带插图的实例
            msg_root = MIMEMultipart('related')
            msg_root['From'] = sender
            msg_root['To'] = ','.join(receivers)
            msg_root['Subject'] = mail_subject

            if cc != None:
                cc = str(cc).split(',')
                receivers.extend(cc)
                msg_root['Cc'] = ','.join(cc)
            if bcc != None:
                bcc = str(bcc).split(',')
                receivers.extend(bcc)
                msg_root['Bcc'] = ','.join(bcc)

            # 邮件正文内容
            msg_alternative = MIMEMultipart('alternative')
            msg_alternative.attach(MIMEText(mail_content, 'html', 'utf-8'))
            msg_root.attach(msg_alternative)

            # 构造插图
            for illustrate_name in illustrate_name_list:
                if not self.is_contain_chinese(illustrate_name):
                    fp = open(illustrate_path + "/" + illustrate_name, 'rb')
                    msg_image = MIMEImage(fp.read())
                    fp.close()
                    msg_image.add_header('Content-ID', '<' + illustrate_name + '>')
                    msg_root.attach(msg_image)
                else:
                    raise smtplib.SMTPResponseException(1, "Illustration's name can not be chinese!")

            try:
                self.connection.sendmail(sender, receivers, msg_root.as_string())
                for illustrate_name in illustrate_name_list:
                    my_file = illustrate_path + "/" + illustrate_name
                    if os.path.exists(my_file):
                        os.remove(my_file)
                return True
            except smtplib.SMTPException:
                return False

        if len(attachment_name_list) != 0 and len(illustrate_name_list) != 0:
            # 创建一个带附件的实例
            msg_root = MIMEMultipart('related')
            # msg_root['From'] = formataddr([sender, sender], charset='utf-8')
            # msg_root['To'] = formataddr([receiver, receiver], charset='utf-8')
            msg_root['From'] = sender
            msg_root['To'] = ','.join(receivers)
            msg_root['Subject'] = mail_subject

            if cc != None:
                cc = str(cc).split(',')
                receivers.extend(cc)
                msg_root['Cc'] = ','.join(cc)
            if bcc != None:
                bcc = str(bcc).split(',')
                receivers.extend(bcc)
                msg_root['Bcc'] = ','.join(bcc)

            # 邮件正文内容
            msg_alternative = MIMEMultipart('alternative')
            msg_alternative.attach(MIMEText(mail_content, 'html', 'utf-8'))
            msg_root.attach(msg_alternative)

            # 构造附件
            for attach_name in attachment_name_list:
                if self.is_contain_chinese(attach_name):
                    attach = MIMEText(open(attachment_path + "/" + attach_name, 'rb').read(), 'base64', 'utf-8')
                    attach["Content-Type"] = 'application/octet-stream'
                    attach.add_header("Content-Disposition", "attachment", filename=("gbk", "", attach_name))
                    msg_root.attach(attach)
                else:
                    attach = MIMEText(open(attachment_path + "/" + attach_name, 'rb').read(), 'base64', 'utf-8')
                    attach["Content-Type"] = 'application/octet-stream'
                    attach["Content-Disposition"] = 'attachment; filename="' + attach_name + '"'
                    msg_root.attach(attach)

            # 构造插图
            for illustrate_name in illustrate_name_list:
                if not self.is_contain_chinese(illustrate_name):
                    fp = open(illustrate_path + "/" + illustrate_name, 'rb')
                    msg_image = MIMEImage(fp.read())
                    fp.close()
                    msg_image.add_header('Content-ID', '<' + illustrate_name + '>')
                    msg_root.attach(msg_image)
                else:
                    raise smtplib.SMTPResponseException(1, "Illustration's name can not be chinese!")

            try:
                self.connection.sendmail(sender, receivers, msg_root.as_string())
                for attach_name in attachment_name_list:
                    my_file = attachment_path + "/" + attach_name
                    if os.path.exists(my_file):
                        os.remove(my_file)
                for illustrate_name in illustrate_name_list:
                    my_file = illustrate_path + "/" + illustrate_name
                    if os.path.exists(my_file):
                        os.remove(my_file)
                return True
            except smtplib.SMTPException:
                return False
        return False