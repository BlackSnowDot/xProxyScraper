import os, re
from requests import get
from json import load

class xProxyScraper():
    def __init__(self) -> None:
        self.version = "1.0"
        self.dateRegex = "[0-9]{4}-[0-9]{2}-[0-9]{2}"
        self.proxyRegex = r"\b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))\b:[0-9]?[0-9]?[0-9]?[0-9]"
        self.dates, self.proxies = [], []
        self.config = load(open("config.json"))
    
    def banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        return """
            ____                      ____                                 
        __  _|  _ \ _ __ _____  ___   _/ ___|  ___ _ __ __ _ _ __   ___ _ __ 
        \ \/ / |_) | '__/ _ \ \/ / | | \___ \ / __| '__/ _` | '_ \ / _ \ '__|
        >  <|  __/| | | (_) >  <| |_| |___) | (__| | | (_| | |_) |  __/ |   
        /_/\_\_|   |_|  \___/_/\_\\__, |____/ \___|_|  \__,_| .__/ \___|_|   
                                |___/                     |_|              
                                version %s

""" % self.version

    def getDates(self):
        request = requests.get("https://checkerproxy.net/api/archive/")
        if request.status_code == 200:
            for date in re.findall(self.dateRegex, str(request.json()),
                                   re.RegexFlag.MULTILINE):
                self.dates.append(date)
        return self.dates

    def start(self):
        global amount
        for date in self.getDates():
            request = requests.get("https://checkerproxy.net/api/archive/" + date)
            print(f"[+] {request.url}" if request.status_code == 200 else f"[-] {request.url}")
            for proxy in re.finditer(self.proxyRegex, str(request.json()),
                                     re.RegexFlag.MULTILINE):
                self.proxies.append(proxy.group())

        data = set(self.proxies)
        amount = len(data)
        open(self.config['output-File'], "w").write("\n".join(data))
        print(f"Done! {amount} Proxy Found")


if __name__ == "__main__":
    xProxyScraper().start()
