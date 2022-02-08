import imaplib
from core.imbox.imap import ImapTransport
from core.imbox.messages import Messages
from core.imbox.vendors import GmailMessages, QQmailMessages, hostname_vendorname_dict, name_authentication_string_dict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import configparser
import os

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
conf = configparser.ConfigParser()
conf.read(os.path.join(base_dir, 'config.conf'))

attachment_path = conf.get("mailbox", "attachment_path")
illustrate_path = conf.get("mailbox", "illustrate_path")

class Imbox:

    authentication_error_message = None

    def __init__(self, hostname, username=None, password=None, ssl=True,
                 port=None, ssl_context=None, policy=None, starttls=False,
                 vendor=None):

        self.server = ImapTransport(hostname, ssl=ssl, port=port,
                                    ssl_context=ssl_context, starttls=starttls)

        self.hostname = hostname
        self.username = username
        self.password = password
        self.parser_policy = policy
        self.vendor = vendor or hostname_vendorname_dict.get(self.hostname)

        if self.vendor is not None:
            self.authentication_error_message = name_authentication_string_dict.get(
                self.vendor)

        try:
            self.connection = self.server.connect(username, password)
        except imaplib.IMAP4.error as e:
            if self.authentication_error_message is None:
                raise
            raise imaplib.IMAP4.error(
                self.authentication_error_message + '\n' + str(e))

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.logout()

    def logout(self):
        self.connection.close()
        self.connection.logout()

    def list(self):
        return self.connection.list()

    def check_success(self, response):
        if 'OK' in str(response):
            return True
        else:
            return False

    def is_contain_chinese(self, check_str):
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def mark_seen(self, folder, uids):
        if uids=='' or uids==None:
            return
        self.select(folder)
        r1 = self.connection.uid('STORE', (uids), '-FLAGS', '(\\UNSEEN)')
        r2 = self.connection.uid('STORE', (uids), '+FLAGS', '(\\SEEN)')
        return self.check_success(r1) & self.check_success(r2)

    def mark_unseen(self, folder, uids):
        if uids=='' or uids==None:
            return
        self.select(folder)
        r1 = self.connection.uid('STORE', (uids), '-FLAGS', '(\\SEEN)')
        r2 = self.connection.uid('STORE', (uids), '+FLAGS', '(\\UNSEEN)')
        return self.check_success(r1) & self.check_success(r2)

    def mark_flag(self, folder, uids):
        if uids=='' or uids==None:
            return
        self.select(folder)
        r1 = self.connection.uid('STORE', (uids), '-FLAGS', '(\\UNFLAGGED)')
        r2 = self.connection.uid('STORE', (uids), '+FLAGS', '(\\FLAGGED)')
        return self.check_success(r1) & self.check_success(r2)

    def mark_unflag(self, folder, uids):
        if uids=='' or uids==None:
            return
        self.select(folder)
        r1 = self.connection.uid('STORE', (uids), '-FLAGS', '(\\FLAGGED)')
        r2 = self.connection.uid('STORE', (uids), '+FLAGS', '(\\UNFLAGGED)')
        return self.check_success(r1) & self.check_success(r2)

    def copy(self, origin_folder, uids, target_folder):
        if uids=='' or uids==None:
            return
        self.select(origin_folder)
        r = self.connection.uid('COPY', (uids), self.get_folder(target_folder))
        return self.check_success(r)

    def move(self, source_folder, uids, target_folder):
        if uids=='' or uids==None:
            return
        if self.copy(source_folder, uids, target_folder):
            return self.permanently_delete(source_folder, uids)

    def delete(self, origin_folder, uids):
        if uids=='' or uids==None:
            return
        if self.copy(origin_folder, (uids), 'deleted'):
            return self.permanently_delete(origin_folder, (uids))

    def permanently_delete(self, folder, uids):
        if uids=='' or uids==None:
            return
        self.select(folder)
        r1 = self.connection.uid('STORE', (uids), '+FLAGS', '(\\Deleted)')
        r2 = self.connection.expunge()
        return self.check_success(r1) & self.check_success(r2)

    def draft(self, receivers, mail_subject, mail_content, cc=None, bcc=None, attachment_names=None, illustrate_names=None):
        receivers = str(receivers).split(',')

        attachment_name_list = []
        if attachment_names != None:
            attachment_name_list = str(attachment_names).split(',')
        illustrate_name_list = []
        if illustrate_names != None:
            illustrate_name_list = str(illustrate_names).split(',')

        if len(attachment_name_list)==0 and len(illustrate_name_list)==0:
            message = MIMEText(mail_content, 'html', 'utf-8')
            message['From'] = self.username
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

            r = self.connection.append(self.get_folder('drafts'), None, None, message.as_string().encode('utf-8'))
            return self.check_success(r)

        if len(attachment_name_list) != 0 and len(illustrate_name_list) == 0:
            # 创建一个带附件的实例
            message = MIMEMultipart()
            message['From'] = self.username
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

            r = self.connection.append(self.get_folder('drafts'), None, None, message.as_string().encode('utf-8'))
            return self.check_success(r)

        if len(attachment_name_list) == 0 and len(illustrate_name_list) != 0:
            # 创建一个带插图的实例
            msg_root = MIMEMultipart('related')
            msg_root['From'] = self.username
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
                    raise ValueError("Illustration's name can not be chinese!")

            r = self.connection.append(self.get_folder('drafts'), None, None, msg_root.as_string().encode('utf-8'))
            return self.check_success(r)

        if len(attachment_name_list) != 0 and len(illustrate_name_list) != 0:
            # 创建一个带附件的实例
            msg_root = MIMEMultipart('related')
            # msg_root['From'] = formataddr([sender, sender], charset='utf-8')
            # msg_root['To'] = formataddr([receiver, receiver], charset='utf-8')
            msg_root['From'] = self.username
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
                    raise ValueError("Illustration's name can not be chinese!")

            r = self.connection.append(self.get_folder('drafts'), None, None, msg_root.as_string().encode('utf-8'))
            return self.check_success(r)
        return False

    def messages(self, **kwargs):
        folder = kwargs.get('folder', False)

        messages_class = Messages
        if self.vendor == 'gmail':
            messages_class = GmailMessages
        if self.vendor == 'qq':
            messages_class = QQmailMessages

        if folder:
            self.connection.select(messages_class.FOLDER_LOOKUP.get((folder.lower())) or folder)
            del kwargs['folder']
        else:
            self.connection.select('INBOX')
        return messages_class(connection=self.connection, parser_policy=self.parser_policy, **kwargs)

    def folders(self):
        return self.connection.list()

    def get_folder(self, folder):
        messages_class = Messages
        if self.vendor == 'gmail':
            messages_class = GmailMessages
        if self.vendor == 'qq':
            messages_class = QQmailMessages
        if folder:
            return messages_class.FOLDER_LOOKUP.get((folder.lower())) or folder

    def select(self, folder):
        if folder:
            self.connection.select(self.get_folder(folder))