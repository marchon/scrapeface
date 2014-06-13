#!/usr/bin/env python
from StringIO import StringIO
from colorama import init
#from colorama import Fore, Back, Style
from colorama import Fore, Style
import lxml.html
import time
import re
import os
import urllib
import argparse
import sys
import os.path
if sys.platform != 'win32' and sys.platform != 'darwin':
    from pyvirtualdisplay import Display


def extract_facebook_user_ids_list(html_source): 
        user_id_list = re.findall("user.php\\?id=(\\d+)", html_source)
        return sorted(set(user_id_list))




def extract_mutual_friends(html_source):

    data = list()

    xpath_name_params = ".//div[@class='fsl fwb fcb']/a/@href"
    xpath_name_params2 = ".//div[@class='fsl fwb fcb']/a/text()"

    #html_source = open(filename).read()

    html_source = urllib.unquote(html_source).decode('utf8') 


    #print html_source

    # parse to lxml object
    html_lxml = lxml.html.parse(StringIO(html_source))
    params_result = html_lxml.xpath(xpath_name_params)
    params_result2 = html_lxml.xpath(xpath_name_params2)

    for prm, prm2 in zip(params_result, params_result2):

        if "profile.php" in prm:
            result = re.search(
                '(?<=\profile\.php\?id=)(.*\n?)(?=&fref=pb_other)', prm)
            if result.group() not in data:
                data.append(result.group())
            if prm2 not in data:
                data.append(prm2)
        else:
            result = re.search('(?<=\.com\/)(.*\n?)(?=\?)', prm)
            if result.group() not in data:
                data.append(result.group())
            if prm2 not in data:
                data.append(prm2)

    print Fore.GREEN + "\nTotal of %s hidden friends have been found\n" % str(len(data))
    return data

import sys
data =' '.join(sys.stdin.readlines())

print extract_facebook_user_ids_list(data)

