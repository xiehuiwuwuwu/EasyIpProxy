#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import re
import time
from bs4 import BeautifulSoup
import random
from userAgent import user_agent
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
headers = { "User-Agent": random.choice(user_agent)}
#http://www.66ip.cn/1.html

class IpProxyPool:
    def __init__(self):
        self.pools = []

    def addPool(self,str):
        self.pools.append(str)


def getIpProxyAndCheckValid(ipProxyPool):
    for page in range(4):
        if page == 0:
            continue

        url     = "http://www.66ip.cn/" + str(page) + ".html"
        s       = requests.session()
        html    = s.get(url,headers=headers)    #网页的html

        while True:
            if html.status_code == 200:
                break

        strr = html.content
        soup     = BeautifulSoup(strr,"html.parser")
        a        = soup.select("table tr")
        a = str(a)
        ip = re.findall("<tr><td>([1-9].*?)</td><td>([1-9].*?)</td><td>",a)
        for l in range(len(ip)):
            s = ip[l][0] + ":" + ip[l][1]

            proxies = {
                'http': 'http://{}'.format(s),
            }

            try:
                resp = requests.get(url="https://aiqicha.baidu.com/?from=fc", proxies=proxies, headers=headers, timeout=3, verify=False)
                if resp.status_code == 200:
                    ipProxyPool.addPool(s)
                else:
                    print("Error")
            
            except Exception as e:
                print("error")

if __name__=='__main__':
    ipPool = IpProxyPool()
    getIpProxyAndCheckValid(ipPool)
    print(ipPool.pools)

    # <Method to Use>:
    # for i in ipPool.pools
    #     proxies = {
    #                 'http': 'http://{}'.format(i),
    #             }
    #     resp = requests.get(url="https://www.baidu.com/", proxies=proxies, headers=headers, timeout=3, verify=False)