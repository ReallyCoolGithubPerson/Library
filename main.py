import json
import os
import tempfile
import time

import requests
from ascii_magic import AsciiArt
from isbnlib import cover, desc, isbn_from_words, meta
from PIL import Image

SERVICE = "openl"

def snatchimage(link):
    r = requests.get(link, stream=True)
    basic = Image.open(r.raw)
    img = basic
    if img is not None:
        return img
    else:
        return None

def snatchinfo(isbn):
    data = meta(isbn, SERVICE)
    parseddata = json.loads(json.dumps(data))
    os.system('clear')
    print(parseddata["Title"], end=" ") #Remember that the JSON tags are caps senstitive
    print("\x1b[32m (" + parseddata["Year"] + ") \x1b[39m", end="\n\n")
    print("\x1b[36mWritten by ", end="\x1b[39m")
    print("\x1b[95m" + "".join(parseddata["Authors"]), end="\x1b[39m\n\n")
    print("\x1b[36mPublished by ", end="\x1b[39m")
    print("\x1b[95m" + "".join(parseddata["Publisher"]), end="\x1b[39m\n\n")
    print("\x1b[94m\x1b[36mShort description: \n " + "\x1b[95m" + desc(isbn), end="\x1b[39m\n\n")
    print("\x1b[94m\x1b[36mAmazon listing: \x1b[95mhttps://www.amazon.com/s?k=" + isbn + "&i=stripbooks&crid=1VSHL9E84NQ3J&sprefix=0062366963%2Cstripbooks%2C132&ref=nb_sb_noss\n")
    print("\x1b[94m\x1b[36mGoodReads listing: \x1b[95mhttps://www.goodreads.com/book/isbn/"+isbn+"\n")
    if cover(isbn):
        with tempfile.NamedTemporaryFile(suffix=".jpeg") as temp:
            othercover = json.loads(json.dumps(cover(isbn)))
            snatchimage(othercover["thumbnail"]).save(temp.name)
            localcover = AsciiArt.from_image(temp.name)
            size = os.get_terminal_size()
            localcover.to_terminal(columns=int(size.columns / 1.5), width_ratio=2)
            print("\n\n\x1b[36mgbs cover link:\x1b[95m " + othercover["thumbnail"] + "\n\n")
    else:
        print("No cover has been found.")
    ctrl = input("\033[0mR = return:")
    if ctrl.capitalize() == "R":
        start()
        return
def start():
    os.system("clear")
    type = input("\033[0mEnter the name of your book:")
    isbn = isbn_from_words(type)
    metas = meta(isbn, SERVICE)
    data = json.loads(json.dumps(metas))
    if data:
        snatchinfo(isbn_from_words(type))
    else:
        print("\n \033[1;31;40mNo such book found, check spelling and try again in three seconds. \x1b[39m\033[0m")
        time.sleep(3)
        start()
        return
start()