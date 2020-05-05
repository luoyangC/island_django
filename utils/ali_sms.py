import json
import random

from django.core.cache import cache
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from config.settings import ALI_ACCESS_KEYID, ALI_ACCESS_SECRET, ALI_REGION_ID
from config.settings import ALI_SIGN_NAME, ALI_TEMPLATE_CODE

client = AcsClient(ALI_ACCESS_KEYID, ALI_ACCESS_SECRET, ALI_REGION_ID)
request = CommonRequest()
request.set_accept_format('json')
request.set_domain('dysmsapi.aliyuncs.com')
request.set_method('POST')
request.set_protocol_type('https')
request.set_version('2017-05-25')
request.set_action_name('SendSms')


def send_sms(mobile, send_type):
    request.add_query_param('RegionId', ALI_REGION_ID)
    request.add_query_param('PhoneNumbers', mobile)
    request.add_query_param('SignName', ALI_SIGN_NAME)
    request.add_query_param('TemplateCode', ALI_TEMPLATE_CODE)
    request.add_query_param('TemplateParam', {'code': make_verification_code(mobile, send_type)})

    response = client.do_action(request)
    response = json.loads(response, encoding='utf-8')
    return {'message': response['Message'], 'code': response['Code']}


def make_verification_code(mobile, send_type):
    code = str(random.randint(100000, 999999))
    cache.set(mobile, (send_type, code), timeout=60 * 100000)
    return code
