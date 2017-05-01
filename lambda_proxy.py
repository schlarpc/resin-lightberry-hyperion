import os
from botocore.vendored import requests

def lambda_handler(event, context):
    url = 'https://{}.resindevice.io/'.format(os.environ['DEVICE_UUID'])
    return requests.post(url, json=event).json()
