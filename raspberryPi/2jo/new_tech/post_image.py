# -*- coding: utf-8 -*--
# Make Command line like this!
# python3 something.py image_name.png 'What you want to say'
# python3 post_image.py high_resolution_image.png 'Checkout this cool image!'
# upload image in same directory
# pip3 install hashlib, python-magic
import re
import requests
import sys
from hashlib import md5
import magic
import os

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

consumer_key="voZZvBqJvSdoIGe9XBCaBjQFp"
consumer_secret="RyRdaJYsQjY7rSGhmAvwMZydCT9O0cbGrWilz3PfDQaK1WbNSV"
access_token="1023246194883973121-87Kh3B8GIkfwm73oOL3WjJ3XjPUN05"
access_token_secret="ypnT5BQRrporKD94aSwvRSEV4SYFOu1S8RbxnH3omj40b"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

if len(sys.argv) < 2:
    print(len(sys.argv[1]))
    print("Usage: %s <file/url> [text]" % (sys.argv[0]),)
    sys.exit(1)

if re.match(r'^https?://', sys.argv[1]):
    # it's an url, so we need to download it
    image_url = sys.argv[1]

    session = requests.session()
    response = session.get(image_url)
    print("Update")
    if response.status_code != requests.codes.ok:
        raise Exception('Not 200.')

    filename = 'poster_%s.jpeg' % md5.new(image_url).hexdigest()

    with open(filename, 'wb') as handle:
        for block in response.iter_content(1048576):
            if not block:
                break
            handle.write(block)
        handle.close()

    mimetype = magic.from_file(filename, mime=True)
    if not mimetype.startswith('image/'):
        raise Exception('Not an image: ' + mimetype)
    if os.stat(filename).st_size > 3072 * 1024: # 3MB? unsure
        raise Exception('Bigger than 3MB')
else:
    filename = sys.argv[1]

try:
    api.update_with_media(filename, status=sys.argv[2])
except IndexError:
    api.update_with_media(filename)

