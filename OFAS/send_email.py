"""
_*_ coding : utf-8 -*_ 
@author：86136
@date：2023年04月07日
@File : send_email
@Project : Archive
"""

from django.core.mail import send_mail
# from app01.models import Subscription
# from django.conf import settings
import smtplib
from email.mime.text import MIMEText

if __name__ == '__main__':
    mail_host = 'smtp.163.com'
    # 163用户名
    mail_user = '13603005294'
    # 密码(部分邮箱为授权码)
    mail_pass = 'EJSPIZGXDNFTDNAM'
    # 邮件发送方邮箱地址
    sender = '13603005294@163.com'
    # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = ['1293843791@qq.com']
    message = MIMEText('content', 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = 'title'
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = '1293843791@qq.com'
    # 登录并发送邮件
    # try:
    smtpObj = smtplib.SMTP()
    # 连接到服务器
    smtpObj.connect(mail_host, 25)
    # 登录到服务器
    smtpObj.login(mail_user, mail_pass)
    # 发送
    print(message)
    smtpObj.sendmail(
        sender, receivers, message.as_string())
    # 退出
    smtpObj.quit()
    print('success')
    # except smtplib.SMTPException as e:
    #     print('error', e)  # 打印错误




