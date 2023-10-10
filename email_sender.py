import smtplib
from email.mime.text import MIMEText

def send_email(receiver_email, subject, message, smtpCon):
    
    sender_email=smtpCon['sender_email']
    smtp_server=smtpCon['smtp_server']
    smtp_port=smtpCon['smtp_port']
    username=smtpCon['username']
    password=smtpCon['password']
    # 创建 MIMEText 对象
    msg = MIMEText(message)
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    try:
        # 连接 SMTP 服务器
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        # 登录 SMTP 服务器
        server.login(username, password)
        # 发送邮件
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('邮件发送成功')
    except Exception as e:
        print('邮件发送失败:', str(e))
    finally:
        # 关闭连接
        server.quit()