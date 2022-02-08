from core.imbox.imbox import Imbox
from core.smbox import Smbox
import configparser
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
conf = configparser.ConfigParser()
conf.read(os.path.join(base_dir, 'config.conf'))

username = conf.get("mailbox", "username")
password = conf.get("mailbox", "password")

imap_server_host = conf.get("imap", "server_host")
imap_server_port = int(conf.get("imap", "server_port"))
imap_enable_ssl = True if conf.get("imap", "enable_ssl") == "True" else False

smtp_server_host = conf.get("smtp", "server_host")
smtp_server_port = int(conf.get("smtp", "server_port"))
smtp_enable_ssl = True if conf.get("smtp", "enable_ssl") == "True" else False


def list_boxes():
    '''
    列出当前邮箱账户下有哪些邮箱目录
    :return:
    '''
    imbox = Imbox(imap_server_host,
                  port=imap_server_port,
                  username=username,
                  password=password,
                  ssl=imap_enable_ssl,
                  ssl_context=None,
                  starttls=False)
    return imbox.list()

def get_messages(folder, current_page=None, page_size=None):
    '''
    分页获取指定文件夹中的邮件（如需获取全部，current_page、page_size不设置即可）
    :param folder: 取值inbox、sent、drafts、deleted、junk
    :param current_page:取值1,2,3...
    :param page_size:
    :return: json格式数据列表
    '''
    imbox = Imbox(imap_server_host,
                  port=imap_server_port,
                  username=username,
                  password=password,
                  ssl=imap_enable_ssl,
                  ssl_context=None,
                  starttls=False)
    return imbox.messages(folder=folder, current_page=current_page, page_size=page_size).page

def get_unread_messages(folder, unread=True, current_page=None, page_size=None):
    '''
    分页获取指定文件夹中的未读邮件（如需获取全部，current_page、page_size不设置即可）
    :param folder:取值inbox、sent、drafts、deleted、junk
    :param unread:
    :param current_page:取值1,2,3...
    :param page_size:
    :return:json格式数据列表
    '''
    imbox = Imbox(imap_server_host,
                  port=imap_server_port,
                  username=username,
                  password=password,
                  ssl=imap_enable_ssl,
                  ssl_context=None,
                  starttls=False)
    return imbox.messages(folder=folder, unread=unread, current_page=current_page, page_size=page_size).page

def get_flagged_messages(folder, flagged=True, current_page=None, page_size=None):
    '''
    分页获取指定文件夹中的星标邮件（如需获取全部，current_page、page_size不设置即可）
    :param folder: 取值inbox、sent、drafts、deleted、junk
    :param flagged:
    :param current_page:取值1,2,3...
    :param page_size:
    :return:json格式数据列表
    '''
    imbox = Imbox(imap_server_host,
                  port=imap_server_port,
                  username=username,
                  password=password,
                  ssl=imap_enable_ssl,
                  ssl_context=None,
                  starttls=False)
    return imbox.messages(folder=folder, flagged=flagged, current_page=current_page, page_size=page_size).page

def get_date_before_messages(folder, date_str, current_page=None, page_size=None):
    '''
    分页获取指定文件夹中、指定日期之前的邮件（注意：date_str的格式必须是YYYY-mm-dd，如需获取全部，current_page、page_size不设置即可）
    :param folder: 取值inbox、sent、drafts、deleted、junk
    :param date_str:
    :param current_page:取值1,2,3...
    :param page_size:
    :return:json格式数据列表
    '''
    imbox = Imbox(imap_server_host,
                  port=imap_server_port,
                  username=username,
                  password=password,
                  ssl=imap_enable_ssl,
                  ssl_context=None,
                  starttls=False)
    return imbox.messages(folder=folder, date__lt=date_str, current_page=current_page, page_size=page_size).page

def get_date_after_messages(folder, date_str, current_page=None, page_size=None):
    '''
    分页获取指定文件夹中、指定日期之后的邮件（注意：date_str的格式必须是YYYY-mm-dd，如需获取全部，current_page、page_size不设置即可）
    :param folder: 取值inbox、sent、drafts、deleted、junk
    :param date_str:
    :param current_page:取值1,2,3...
    :param page_size:
    :return:json格式数据列表
    '''
    imbox = Imbox(imap_server_host,
                  port=imap_server_port,
                  username=username,
                  password=password,
                  ssl=imap_enable_ssl,
                  ssl_context=None,
                  starttls=False)
    return imbox.messages(folder=folder, date__gt=date_str, current_page=current_page, page_size=page_size).page

def mark_seen_by_uids(folder, uids):
    '''
    批量设置已读，多个uid以英文逗号分隔
    :param folder: uids的原目录，取值inbox、sent、drafts、deleted、junk
    :param uids:
    :return:Ture or False
    '''
    imbox = Imbox(imap_server_host,
                  port=imap_server_port,
                  username=username,
                  password=password,
                  ssl=imap_enable_ssl,
                  ssl_context=None,
                  starttls=False)
    return imbox.mark_seen(folder, uids)

def mark_unseen_by_uids(folder, uids):
    '''
    批量设置未读，多个uid以英文逗号分隔
    :param folder: uids的原目录，取值inbox、sent、drafts、deleted、junk
    :param uids:
    :return:Ture or False
    '''
    imbox = Imbox(imap_server_host,
                  port=imap_server_port,
                  username=username,
                  password=password,
                  ssl=imap_enable_ssl,
                  ssl_context=None,
                  starttls=False)
    return imbox.mark_unseen(folder, uids)

def mark_flag_by_uids(folder, uids):
    '''
    批量设为星标，多个uid以英文逗号分隔
    :param folder: uids的原目录，取值inbox、sent、drafts、deleted、junk
    :param uids:
    :return:Ture or False
    '''
    imbox = Imbox(imap_server_host,
                  port=imap_server_port,
                  username=username,
                  password=password,
                  ssl=imap_enable_ssl,
                  ssl_context=None,
                  starttls=False)
    return imbox.mark_flag(folder, uids)

def mark_unflag_by_uids(folder, uids):
    '''
    批量去掉星标，多个uid以英文逗号分隔
    :param folder: uids的原目录，取值inbox、sent、drafts、deleted、junk
    :param uids:
    :return:Ture or False
    '''
    imbox = Imbox(imap_server_host,
                  port=imap_server_port,
                  username=username,
                  password=password,
                  ssl=imap_enable_ssl,
                  ssl_context=None,
                  starttls=False)
    return imbox.mark_unflag(folder, uids)

def move(source_folder, uids, target_folder):
    '''
    批量移动邮件，多个uid以英文逗号分隔
    :param source_folder: uids的原目录，取值inbox、sent、drafts、deleted、junk
    :param uids:
    :param target_folder: 目标目录，取值inbox、sent、drafts、deleted、junk
    :return:Ture or False
    '''
    imbox = Imbox(imap_server_host,
                  port=imap_server_port,
                  username=username,
                  password=password,
                  ssl=imap_enable_ssl,
                  ssl_context=None,
                  starttls=False)
    return imbox.move(source_folder, uids, target_folder)

def delete_by_uids(folder, uids):
    '''
    批量删除（移到已删除），多个uid以英文逗号分隔
    :param folder: uids的原目录，取值inbox、sent、drafts、deleted、junk
    :param uids:
    :return:Ture or False
    '''
    imbox = Imbox(imap_server_host,
                  port=imap_server_port,
                  username=username,
                  password=password,
                  ssl=imap_enable_ssl,
                  ssl_context=None,
                  starttls=False)
    return imbox.delete(folder, uids)

def permanently_delete_by_uids(folder, uids):
    '''
    批量永久删除，多个uid以英文逗号分隔
    :param folder: uids的原目录，取值inbox、sent、drafts、deleted、junk
    :param uids:
    :return:Ture or False
    '''
    imbox = Imbox(imap_server_host,
                  port=imap_server_port,
                  username=username,
                  password=password,
                  ssl=imap_enable_ssl,
                  ssl_context=None,
                  starttls=False)
    return imbox.permanently_delete(folder, uids)

def draft(receivers, mail_subject, mail_content, cc=None, bcc=None, attachment_names=None, illustrate_names=None):
    '''
    保存邮件到草稿箱
    :param receivers: 接收对象的邮箱，多个用英文逗号分隔
    :param mail_subject: 邮件标题
    :param mail_content: 邮件正文（html格式或plain格式）
    :param cc: 抄送对象的邮箱，多个用英文逗号分隔
    :param bcc: 密送对象的邮箱，多个用英文逗号分隔
    :param attachment_names: 附件名称，多个用英文逗号分隔
    :param illustrate_names: 插图名称，多个用英文逗号分隔
    :return:Ture or False

    注意：
        插图的名称不能是中文！！
        正文中用<img>标签插入图片时必须遵循以下格式，例：<img src="cid:xxx.jpg">
    '''
    imbox = Imbox(imap_server_host,
                  port=imap_server_port,
                  username=username,
                  password=password,
                  ssl=imap_enable_ssl,
                  ssl_context=None,
                  starttls=False)
    imbox.draft(receivers, mail_subject, mail_content, cc, bcc, attachment_names, illustrate_names)

def send_mail(receivers, mail_subject, mail_content, cc=None, bcc=None, attachment_names=None,
              illustrate_names=None):
    '''
    发送邮件
    :param receivers: 接收对象的邮箱，多个用英文逗号分隔
    :param mail_subject: 邮件标题
    :param mail_content: 邮件正文（html格式或plain格式）
    :param cc: 抄送对象的邮箱，多个用英文逗号分隔
    :param bcc: 密送对象的邮箱，多个用英文逗号分隔
    :param attachment_names: 附件名称，多个用英文逗号分隔
    :param illustrate_names: 插图名称，多个用英文逗号分隔
    :return:Ture or False
    注意：
        插图的名称不能是中文！！
        正文中用<img>标签插入图片时必须遵循以下格式，例：<img src="cid:xxx.jpg">
    '''
    smbox = Smbox(smtp_server_host,
                  port=smtp_server_port,
                  username=username,
                  password=password,
                  ssl=smtp_enable_ssl,
                  ssl_context=None, starttls=False)
    return smbox.send_mail(username, receivers, mail_subject, mail_content, cc, bcc, attachment_names, illustrate_names)