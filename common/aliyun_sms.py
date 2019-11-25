from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import random
def send_code(phone_number):
    client = AcsClient('LTAIRiQGIywYBeYN', 'ZOHiNBYPr72dCFog2fLU5Pu9RvVAIf', 'cn-hangzhou')
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone_number)
    request.add_query_param('SignName', "Disen工作室")
    request.add_query_param('TemplateCode', "SMS_128646125")
    # 随机生成验证码
    code = ''.join(random.choices(['0','1','2','4','5','6','7','8','9'],k=4))
    request.add_query_param('TemplateParam', "{\"code\":\"%s\"}"%code)
    response = client.do_action(request)
    print(str(response, encoding='utf-8'))
    # 返回code给后端
    return code