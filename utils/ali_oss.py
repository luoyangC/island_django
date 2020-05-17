import base64
import time
import datetime
import json
import hmac
import hashlib

from config.settings import ALI_ACCESS_KEYID, ALI_ACCESS_SECRET
from config.settings import ALI_OSS_BUCKET, ALI_OSS_UPLOAD_DIR, ALI_OSS_EXPIRE_TIME


def get_iso_8601(expire):
    gmt = datetime.datetime.utcfromtimestamp(expire).isoformat()
    gmt += 'Z'
    return gmt


def get_oss_token():
    now = int(time.time())
    expire_sync_point = now + ALI_OSS_EXPIRE_TIME
    expire = get_iso_8601(expire_sync_point)

    array_item = ['starts-with', '$key', ALI_OSS_UPLOAD_DIR]
    condition_array = [array_item]

    policy_dict = {'expiration': expire, 'conditions': condition_array}
    policy = json.dumps(policy_dict).strip()
    policy_encode = base64.b64encode(policy.encode())

    h = hmac.new(ALI_ACCESS_SECRET.encode(), policy_encode, hashlib.sha1)
    sign_result = base64.encodestring(h.digest()).strip()

    token_dict = {
        'dir': ALI_OSS_UPLOAD_DIR,
        'host': ALI_OSS_BUCKET,
        'policy': policy_encode.decode(),
        'accessid': ALI_ACCESS_KEYID,
        'signature': sign_result.decode(),
    }

    return token_dict
