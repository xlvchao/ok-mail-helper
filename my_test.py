import mail_helper

# 列出当前邮箱账户下有哪些邮箱目录
boxes = mail_helper.list_boxes()
print(boxes)

# 获取收件箱中所有邮件
messages = mail_helper.get_messages('inbox')
print(messages)

# 分页获取收件箱中的邮件
messages = mail_helper.get_messages('inbox', current_page=1, page_size=5)
print(messages)

# 设置为已读，返回布尔值
result = mail_helper.mark_seen_by_uids('inbox', '1564,1565')
print(result)

# 设置为未读，返回布尔值
result = mail_helper.mark_unseen_by_uids('inbox', '1564,1565')
print(result)

# 邮件存草稿
receivers='xxx1@qq.com,xxx2@qq.com'
cc='cc1@qq.com,cc2@qq.com' # 抄送
bcc='bb1@qq.com,bb2@qq.com' # 密送
mail_subject='我是标题'
mail_content='我是内容<p><img src="cid:12.jpg"></p>' # 注意插图的引用方式！且插图名称不能是中文！
attachment_names='itinerary.pdf'
illustrate_names='12.jpg'
result = mail_helper.draft(receivers, mail_subject, mail_content, cc, bcc, attachment_names, illustrate_names)
print(result)

# 发送一封普通邮件
receivers='xxx1@qq.com,xxx2@qq.com'
mail_subject='我是标题'
mail_content='我是内容'
result = mail_helper.send_mail(receivers, mail_subject, mail_content)
print(result)

# 发送一封普通邮件，同时抄送、密送
receivers='xxx1@qq.com,xxx2@qq.com'
cc='cc1@qq.com,cc2@qq.com' # 抄送
bcc='bb1@qq.com,bb2@qq.com' # 密送
mail_subject='我是标题'
mail_content='我是内容'
result = mail_helper.send_mail(receivers, mail_subject, mail_content, cc, bcc)
print(result)

# 发送一封普通邮件，同时抄送、密送，并有附件和插图
receivers='xxx1@qq.com,xxx2@qq.com'
cc='cc1@qq.com,cc2@qq.com' # 抄送
bcc='bb1@qq.com,bb2@qq.com' # 密送
mail_subject='我是标题'
mail_content='我是内容<p><img src="cid:12.jpg"></p>' # 注意插图的引用方式！且插图名称不能是中文！
attachment_names='itinerary.pdf'
illustrate_names='12.jpg'
result = mail_helper.send_mail(receivers, mail_subject, mail_content, cc, bcc, attachment_names, illustrate_names)
print(result)