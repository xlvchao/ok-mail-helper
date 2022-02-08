# ok-mail-helper

![](https://img.shields.io/badge/python-3.x-blue.svg) ![](https://img.shields.io/badge/version-1.0.0-brightgreen.svg) ![](https://img.shields.io/badge/license-MIT-000000.svg)

ok-mail-helper是一个基于imap/smtp协议邮件客户端，使用python3.x开发，支持邮件接收并解析、邮件发送，用户可在自己的项目中直接引入、开箱即用，或者结合flask等web框架轻松做成http接口供前端调用、把邮箱管理集成到自己的系统中，亦可通过注册中心（Eureka、Consul、Nacos等）的加持，做成微服务供其他系统调用。



# 提供哪些方法

| 方法名称                                                     | 说明                                                         |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| list_boxes()                                                 | 列出当前邮箱账户下有哪些邮箱目录                             |
| get_messages(folder, current_page=None, page_size=None)      | 分页获取指定文件夹中的邮件（如需获取全部，current_page、page_size不设置即可） |
| get_unread_messages(folder, unread=True, current_page=None, page_size=None) | 分页获取指定文件夹中的未读邮件（如需获取全部，current_page、page_size不设置即可） |
| get_flagged_messages(folder, flagged=True, current_page=None, page_size=None) | 分页获取指定文件夹中的星标邮件（如需获取全部，current_page、page_size不设置即可） |
| get_date_before_messages(folder, date_str, current_page=None, page_size=None) | 分页获取指定文件夹中、指定日期之前的邮件（注意：date_str的格式必须是YYYY-mm-dd，如需获取全部，current_page、page_size不设置即可） |
| get_date_after_messages(folder, date_str, current_page=None, page_size=None) | 分页获取指定文件夹中、指定日期之后的邮件（注意：date_str的格式必须是YYYY-mm-dd，如需获取全部，current_page、page_size不设置即可） |
| mark_seen_by_uids(folder, uids)                              | 批量设置为已读，多个uid以英文逗号分隔（uid是邮件的唯一编码） |
| mark_unseen_by_uids(folder, uids)                            | 批量设置为未读，多个uid以英文逗号分隔uid是邮件的唯一编码）   |
| mark_flag_by_uids(folder, uids)                              | 批量设为星标，多个uid以英文逗号分隔uid是邮件的唯一编码）     |
| mark_unflag_by_uids(folder, uids)                            | 批量去掉星标，多个uid以英文逗号分隔uid是邮件的唯一编码）     |
| move(source_folder, uids, target_folder)                     | 批量移动邮件，多个uid以英文逗号分隔uid是邮件的唯一编码）     |
| delete_by_uids(folder, uids)                                 | 批量删除（移到已删除），多个uid以英文逗号分隔uid是邮件的唯一编码） |
| permanently_delete_by_uids(folder, uids)                     | 批量永久删除，多个uid以英文逗号分隔uid是邮件的唯一编码）     |
| draft(receivers, mail_subject, mail_content, cc=None, bcc=None, attachment_names=None, illustrate_names=None) | 把邮件保存到草稿箱                                           |
| send_mail(receivers, mail_subject, mail_content, cc=None, bcc=None, attachment_names=None, illustrate_names=None) | 发送邮件                                                     |

提示：具体每个方法的使用及参数说明，请参考mail_helper.py源码中的注释。



# 配置说明

配置文件config.conf

```
[application]
name=ok-mail-helper
host=127.0.0.1
port=7003

[mailbox]
username=xxx@qq.com
password=xxx # 这里填‘授权码’，不是密码！去邮箱设置里获取授权码！
attachment_path=C:\Users\lenovo\Desktop\attachments # 发送和接收的附件临时存储目录
illustrate_path=C:\Users\lenovo\Desktop\illustrates # 发送和接收的插图临时保存目录

[imap]
server_host=imap.qq.com
server_port=993
enable_ssl=True

[smtp]
server_host=smtp.qq.com
server_port=465
enable_ssl=True

# 若对外提供HTTP接口，则需要配置以下项，详看web_service.py
[webservice]
appid=123456 # 唯一校验码

# 注册中心
[eureka]
server=http://www.baoxue123.com:1001/eureka/
```



# 使用举例

```python
# 测试前，请先去邮箱设置里开启imap/smtp，以及可获取的邮件数量设置为全部，并生成授权码！

import mail_helper

# 列出当前邮箱账户下有哪些邮箱目录
boxes = mail_helper.list_boxes()
print(boxes)

# 获取收件箱中所有邮件
messages = mail_helper.get_messages('inbox')
print(messages)

# 分页获取已发送中的邮件
messages = mail_helper.get_messages('sent', current_page=1, page_size=5)
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
```



# 重要说明

目前只测试了腾讯QQ邮箱和腾讯企业邮箱，所有功能均可正常使用。其他第三方厂商的邮箱暂时只测试了网易系，但是网易系邮箱的imap/smtp服务器不允许其他第三方客户端与其对接，只支持自家邮件客户端。另外，每个邮箱厂商的邮箱目录及名称可能不一样，项目提供了vendor机制，若需要对接其他第三方厂商的邮箱，需要自行参照已实现的vendor，添加新的vendor，并且可能需要微调代码。



# 问题和建议

如果有什么问题、建议、BUG都可以在这个[Issue](https://github.com/superman-stack/mail-helper/issues/1)和我讨论



# 公众号

关注不迷路，微信扫描下方二维码或搜索关键字“**spartacus**”，关注「**spartacus**」公众号，时刻收听**spartacus**更新通知！

在公众号后台回复“**加群**”，即可加入「**spartacus**」扯淡交流群！

![mp_qrcode](imgs/mp_qrcode.jpg)


# 许可证

```
Copyright [2022] [xlvchao]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
