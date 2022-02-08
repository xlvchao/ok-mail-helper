from gevent import monkey
monkey.patch_all()
import mail_helper
from flask import Flask, request, jsonify
from gevent import pywsgi
import os
import uuid
from werkzeug.utils import secure_filename
import configparser
import py_eureka_client.eureka_client as eureka_client
from utils.log_helper import LoggerFactory

logger = LoggerFactory().getLogger()


# 获取配置
base_dir = os.path.dirname(os.path.abspath(__file__))
conf = configparser.ConfigParser()
conf.read(os.path.join(base_dir, 'config.conf'))

# application
application_name = conf.get("application", "name")
application_host = conf.get("application", "host")
application_port = conf.getint("application", "port")

# eureka
eureka_server = conf.get("eureka", "server")

# mailbox
attachment_path = conf.get("mailbox", "attachment_path")
illustrate_path = conf.get("mailbox", "illustrate_path")

if not os.path.exists(attachment_path):
    os.mkdir(attachment_path)
if not os.path.exists(illustrate_path):
    os.mkdir(illustrate_path)

app = Flask(__name__)


@app.route('/get_messages', methods=["POST"])
def get_messages():
    try:
        folder = request.form.get("folder")
        current_page = int(request.form.get("current_page"))
        page_size = int(request.form.get("page_size"))
        page_data = mail_helper.get_messages(folder=folder, current_page=current_page, page_size=page_size)
        return jsonify({'code': 0, 'message': 'success', 'data': page_data})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})


@app.route('/get_unread_messages', methods=["POST"])
def get_unread_messages():
    try:
        folder = request.form.get("folder")
        current_page = int(request.form.get("current_page"))
        page_size = int(request.form.get("page_size"))
        page_data = mail_helper.get_unread_messages(folder=folder, unread=True, current_page=current_page, page_size=page_size)
        return jsonify({'code': 0, 'message': 'success', 'data': page_data})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})


@app.route('/get_flagged_messages', methods=["POST"])
def get_flagged_messages():
    try:
        folder = request.form.get("folder")
        current_page = int(request.form.get("current_page"))
        page_size = int(request.form.get("page_size"))
        page_data = mail_helper.get_flagged_messages(folder=folder, flagged=True, current_page=current_page, page_size=page_size)
        return jsonify({'code': 0, 'message': 'success', 'data': page_data})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})


@app.route('/get_date_before_messages', methods=["POST"])
def get_date_before_messages():
    try:
        folder = request.form.get("folder")
        date_str = request.form.get("date_str")
        current_page = int(request.form.get("current_page"))
        page_size = int(request.form.get("page_size"))
        page_data = mail_helper.get_date_before_messages(folder=folder, date_str=date_str, current_page=current_page, page_size=page_size)
        return jsonify({'code': 0, 'message': 'success', 'data': page_data})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})


@app.route('/get_date_after_messages', methods=["POST"])
def get_date_after_messages():
    try:
        folder = request.form.get("folder")
        date_str = request.form.get("date_str")
        current_page = int(request.form.get("current_page"))
        page_size = int(request.form.get("page_size"))
        page_data = mail_helper.get_date_after_messages(folder=folder, date_str=date_str, current_page=current_page, page_size=page_size)
        return jsonify({'code': 0, 'message': 'success', 'data': page_data})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})


@app.route('/mark_seen_by_uids', methods=["POST"])
def mark_seen_by_uids():
    try:
        folder = request.form.get("folder")
        uids = request.form.get("uids")
        result = mail_helper.mark_seen_by_uids(folder=folder, uids=uids)
        return jsonify({'code': 0 if result else 1, 'message': 'success' if result else 'failed'})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})


@app.route('/mark_unseen_by_uids', methods=["POST"])
def mark_unseen_by_uids():
    try:
        folder = request.form.get("folder")
        uids = request.form.get("uids")
        result = mail_helper.mark_unseen_by_uids(folder=folder, uids=uids)
        return jsonify({'code': 0 if result else 1, 'message': 'success' if result else 'failed'})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})


@app.route('/mark_flag_by_uids', methods=["POST"])
def mark_flag_by_uids():
    try:
        folder = request.form.get("folder")
        uids = request.form.get("uids")
        result = mail_helper.mark_flag_by_uids(folder=folder, uids=uids)
        return jsonify({'code': 0 if result else 1, 'message': 'success' if result else 'failed'})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})


@app.route('/mark_unflag_by_uids', methods=["POST"])
def mark_unflag_by_uids():
    try:
        folder = request.form.get("folder")
        uids = request.form.get("uids")
        result = mail_helper.mark_unflag_by_uids(folder=folder, uids=uids)
        return jsonify({'code': 0 if result else 1, 'message': 'success' if result else 'failed'})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})


@app.route('/move', methods=["POST"])
def move():
    try:
        source_folder = request.form.get("source_folder")
        uids = request.form.get("uids")
        target_folder = request.form.get("target_folder")
        result = mail_helper.move(source_folder=source_folder, uids=uids, target_folder=target_folder)
        return jsonify({'code': 0 if result else 1, 'message': 'success' if result else 'failed'})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})


@app.route('/delete_by_uids', methods=["POST"])
def delete_by_uids():
    try:
        folder = request.form.get("folder")
        uids = request.form.get("uids")
        result = mail_helper.delete_by_uids(folder=folder, uids=uids)
        return jsonify({'code': 0 if result else 1, 'message': 'success' if result else 'failed'})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})


@app.route('/permanently_delete_by_uids', methods=["POST"])
def permanently_delete_by_uids():
    try:
        folder = request.form.get("folder")
        uids = request.form.get("uids")
        result = mail_helper.permanently_delete_by_uids(folder=folder, uids=uids)
        return jsonify({'code': 0 if result else 1, 'message': 'success' if result else 'failed'})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})


@app.route('/upload_files', methods=["POST"])
def upload_files():
    try:
        # type为0表示附件，1表示插图
        type = int(request.form.get("type"))
        # 获取到上传文件的最后一个文件，用于单文件上传
        # file = request.files['file']
        upload_files = request.files.getlist('file')
        file_dict = {}
        for file in upload_files:
            # secure_filename方法会去掉文件名中的中文
            filename = secure_filename(file.filename)
            filename_new = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1]
            base_path = attachment_path if type == 0 else illustrate_path
            file.save(os.path.join(base_path, filename_new))
            file_dict[filename] = filename_new
        return jsonify({'code': 0, 'message': 'success', 'data': file_dict})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})


@app.route('/send_message', methods=["POST"])
def send_message():
    try:
        receivers = request.form.get("receivers")
        mail_subject = request.form.get("mail_subject")
        mail_content = request.form.get("mail_content")
        cc = request.form.get("cc")
        bcc = request.form.get("bcc")
        attachment_names = request.form.get("attachment_names").split(',')
        illustrate_names = request.form.get("illustrate_names").split(',')
        result = mail_helper.send_mail(receivers, mail_subject, mail_content, cc, bcc, attachment_names, illustrate_names)
        return jsonify({'code': 0 if result else 1, 'message': 'success' if result else 'failed'})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})


@app.route('/save_draft', methods=["POST"])
def save_draft():
    try:
        receivers = request.form.get("receivers")
        mail_subject = request.form.get("mail_subject")
        mail_content = request.form.get("mail_content")
        cc = request.form.get("cc")
        bcc = request.form.get("bcc")
        attachment_names = request.form.get("attachment_names").split(',')
        illustrate_names = request.form.get("illustrate_names").split(',')
        result = mail_helper.draft(receivers, mail_subject, mail_content, cc, bcc, attachment_names, illustrate_names)
        return jsonify({'code': 0 if result else 1, 'message': 'success' if result else 'failed'})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})


if __name__ == "__main__":
    logger.info('ok-mail-helper web_service starting...')

    eureka_client.init(
        eureka_server=eureka_server,
        app_name=application_name,
        instance_host=application_host,
        instance_port=application_port,
        instance_id=application_name + ':' + str(application_port))

    # 这种是不太推荐的启动方式，我这只是做演示用，官方启动方式参见：http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application
    # app.run(host="0.0.0.0", port=application_port, debug=False)

    # 使用WSGI启动服务
    server = pywsgi.WSGIServer(('0.0.0.0', application_port), app)
    server.serve_forever()