import os
import sys
import re
import requests

class xProxyScraper():
    def __init__(self) -> None:
        self.version = "1.0"
        self.dateRegex = "[0-9]{4}-[0-9]{2}-[0-9]{2}"
        self.proxyRegex = r"\b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))\b:[0-9]?[0-9]?[0-9]?[0-9]"
        self.dates = []
        self.proxies = []
        self.dup = []
    
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
            for date in re.findall(self.dateRegex, str(request.json()), re.RegexFlag.MULTILINE):
                self.dates.append(date)
        return self.dates

    def duplicateremove(self):
        with open(sys.argv[1], "r+") as f:
            self.dup = [x.strip() for x in f.readlines()]
        data = set(self.dup)
        current_data = len(data)
        with open(sys.argv[1], "w+") as f:
            f.write("\n".join(data))
        print("Done, Scraped %s Proxy" % current_data)

    def start(self):
        print(self.banner())
        if len(sys.argv) < 2:
            exit(f"Usage: {os.path.basename(__file__)} output.txt")
        for date in self.getDates():
            request = requests.get("https://checkerproxy.net/api/archive/" + date)
            print(f"Getting proxies from {request.url}")
            for proxy in re.finditer(self.proxyRegex, str(request.json()), re.RegexFlag.MULTILINE):
                self.proxies.append(proxy.group())
                print("Founded: %s" % len(self.proxies), end="\r")
                
        with open(sys.argv[1], "a+") as file:
            for proxy in self.proxies:
                file.write(f"{proxy}\n")
        print("Removing Duplicates...")
        self.duplicateremove()


if __name__ == "__main__":
    xProxyScraper().start()