import threading
import requests
import socket
import argparse

argpar = argparse.ArgumentParser(description="Help for UrlScan.")
argpar.add_argument('-s','--host',help='Site scan target.',default="baidu.com")
argpar.add_argument('-t','--thread',help='Site scan thread.',default=3)
args = argpar.parse_args()
# print(args)

TarGetUrl = args.host
ThreadNum = args.thread


lock = threading.Lock()
# 请求头
header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "X-Forwarded-For": "127.0.0.1"
    }


AllUrl_D = []
ScanAll = []

def job(self):
    lock.acquire()
    with open('./dic.txt','r+') as FileOpen:
        for line in FileOpen.readlines():
            DictList = line.replace("\n","")
            ScanUrl = DictList + "." + TarGetUrl
            AllUrl_D.append(ScanUrl)

    for NewUrl in AllUrl_D:
        try:
            Response = requests.get(url="https://" + NewUrl,timeout=3,headers=header)
            GetIP = socket.gethostbyname(NewUrl)
            if Response.status_code in [200,302,403]:
                print("[*] " + NewUrl + "  ->  " + GetIP)
                ScanAll.append(NewUrl)
            else:
                pass
        except:
            pass


def main():
    print('''
       _____  .__                       .__
      /  _  \ |  | _____    ____   ____ |__|
     /  /_\  \|  | \__  \  /    \ /    \|  |
    /    |    \  |__/ __ \|   |  \   |  \  |
    \____|__  /____(____  /___|  /___|  /__|
            \/          \/     \/     \/
    ''')
    for i in str(ThreadNum):
        Th = threading.Thread(target=job, args=(i,))
        Th.start()
        Th.join()
        print('\nScan is done...')
        print("Successful discovery %s" % (len(ScanAll)) + " strip\n")



if __name__ == '__main__':
    main()