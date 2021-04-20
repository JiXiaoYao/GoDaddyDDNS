import requests
import re
import json
import time
import os


class Api:
    domain = ""
    name = ""
    key = ""
    secret = ""

    header = {
        "User-Agent": "curl/7.16.4 (i386-apple-darwin9.0) libcurl/7.16.4 OpenSSL/0.9.7l zlib/1.2.3",
        "Accept": "application/json",
        'Content-Type': "application/json"
    }

    lang = None

    def __init__(self, configPath):
        config = json.loads(self.fileRead(configPath))
        self.domain = config["domain"]
        self.name = config["name"]
        self.key = config["key"]
        self.secret = config["secret"]

    def fileRead(self, path):
        ''
        f = open(path,mode="r",encoding="utf-8")
        content = f.read()
        f.close()
        return str(content)

    def configLanguage(self,configPath):
        result = self.fileRead(configPath)
        jsonObj = json.loads(result)
        if jsonObj["lang"] is "":
            self.lang = jsonObj["text"]["en-US"]
        else:
            self.lang = jsonObj["text"][jsonObj["lang"]]

    def get(self, url, header={}, query={}):
        proxies = {"http": None, "https": None}
        response = requests.get(url=url, params=query, headers={
                                **header, **self.header}, proxies=proxies)
        if response.status_code is not 200:
            print(f"HTTP {response.status_code}:" + response.text)
            raise Exception(f"HTTP {response.status_code}:" + response.text)
        return response.text

    def put(self, url, data, header={}, query={}):
        proxies = {"http": None, "https": None}
        response = requests.put(url=url, data=data, params=query, headers={
                                **header, **self.header}, proxies=proxies)
        if response.status_code is not 200:
            print(f"HTTP {response.status_code}:" + response.text)
            raise Exception(f"HTTP {response.status_code}:" + response.text)
        return response.text

    def update(self):
        apiUrl = f"https://api.godaddy.com/v1/domains/{self.domain}/records/A/{self.name}"
        result = json.loads(self.get(url=apiUrl, header={"Authorization": f"sso-key {self.key}:{self.secret}"}))
        remote_ip = result[0]["data"] if len(result) > 0 else None
        local_ip = re.search(r'.*(?=\n)', self.get("http://ip.sb"))[0]
        if remote_ip != local_ip or remote_ip == None:
            self.put(url=apiUrl, data=json.dumps([{
                "data": local_ip,
                "name": self.name,
                "ttl": 600,
                "type": "A"}]), header={"Authorization": f"sso-key {self.key}:{self.secret}"})
            print(self.lang["update"].format(name=self.name,domain = self.domain,local_ip=local_ip))
            result = json.loads(self.get(url=apiUrl, header={"Authorization": f"sso-key {self.key}:{self.secret}"}))
            remote_ip = result[0]["data"] if len(result) > 0 else None
            print(self.lang["show"].format(remote_ip=remote_ip))
        else:
            print(self.lang["same"].format(local_ip=local_ip,remote_ip=remote_ip))

api = Api("config.json")
api.configLanguage("lang.json")
isRun = True
breakTime = 60 * 5
while (isRun):
    api.update()
    time.sleep(breakTime)