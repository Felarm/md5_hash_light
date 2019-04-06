import requests, hashlib
from send_mail import sendemail


def count_md5(url, email=''):
    file_flow = requests.get(url, stream=True)
    if file_flow.status_code != 404:
        md5hash = hashlib.md5()
        for chunk in file_flow.iter_content(chunk_size=500):
            md5hash.update(chunk)
        if email != '':
            try:
                message = 'url: {}; hash: {}'.format(url, md5hash.hexdigest())
                sendemail(to_addr=email, message=message)
            except:
                print('error during sending, probably wrong configuration or wrong address')
        return md5hash.hexdigest(), url
    else:
        pass
