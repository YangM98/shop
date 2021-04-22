
'''
将该app中的常用变量 保存到一个文件中 避免设置错误
'''

SMS_CODE_REDIS_EXPIRES = 300   # 短信验证码有效期 300秒
SEND_SMS_CODE_INTERVAL = 60    # flag标记有效期60秒