# -*- coding: utf-8 -*-

'''
This module provide image storage.

'''

__version__ = '0.0.1'

ImageUpyunHost = "ueimage2.b0.upaiyun.com"

Bucket = "ueimage2"

User = "imageadmin"

Password = "14@upyunadmin"


rootpath = {
    'user': "/upload/user/",
    'work': "/upload/work/",
    'record': "/upload/record/"
}


def get_rootpath(item):

    if item in rootpath:
        return rootpath[item]
    else:
        return ""


def get_imagehost():

        return "http://" + ImageUpyunHost


def validate_image(imageBuffer, size):

    from cStringIO import StringIO
    from PIL import Image
    csio = StringIO(imageBuffer)
    try:
        im = Image.open(csio)
        if im.size[0] < size[0] or im.size[1] < size[1]:

            return 1
    except:
        print "open stringio error!"
        return -1
    return 0


def uploadToUpyun(uid, fileBuffer, rootpath, filename, headers={}):

    import upyun
    from hashlib import md5
    import time
    import os

    up = upyun.UpYun(Bucket, User, Password, timeout=30,
                     endpoint=upyun.ED_AUTO)
    name, ext = os.path.splitext(filename)
    linkname = str(uid) + name + str(time.time())
    realname = md5(linkname).hexdigest() + ext
    imghost = get_imagehost()
    try:

        res = up.put(rootpath + realname, fileBuffer, checksum=False,
                     headers=headers)
        if res:
            return imghost + rootpath + realname
        else:
            return ""
    except upyun.UpYunServiceException as se:
        import logging
        logging.info("HTTP Status Code: " + str(se.status))
        logging.error("Error Message:    " + se.msg)

    except upyun.UpYunClientException as ce:
        logging.error("Error Message:    " + se.msg)

    return ""
