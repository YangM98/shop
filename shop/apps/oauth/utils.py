from itsdangerous import TimedJSONWebSignatureSerializer as TJWSerializer
from django.conf import settings

def generate_user_openid_token(openid):
    # TJWSerializer( 秘钥 ，有效期)
    serializer = TJWSerializer(settings.SECRET_KEY,600)
    data = {'openid':openid}
    token = serializer.dumps(data)

    return token.decode()



def check_user_token_openid(access_token):

    serializer = TJWSerializer(settings.SECRET_KEY,600)
    try:
        data = serializer.loads(access_token)
    except :
        return None
    else:
        openid = data.get('openid')
        return openid