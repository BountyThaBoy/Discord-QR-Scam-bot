from colorama import Fore
import json
import requests

def split(word):
    return [char for char in word]

def lgbtqprint(text = ""):
    rainbowarray = [f"{Fore.RED}", f"{Fore.YELLOW}", f"{Fore.GREEN}", f"{Fore.BLUE}", f"{Fore.CYAN}", f"{Fore.MAGENTA}"]
    chararray = []
    chararray += split(text)
    indexlength = 0
    rainowindexlength = 0

    newstring = ""
    for i in range(len(chararray)):
        if rainowindexlength > 5:
            rainowindexlength = 0
        if not indexlength > len(chararray):
            newstring += rainbowarray[rainowindexlength]
            newstring += chararray[indexlength]
        indexlength = indexlength + 1
        rainowindexlength = rainowindexlength + 1

    print(newstring + Fore.RESET)

def CheckWebHook(webhook_url):
    data = json.dumps({})

    header = {
        "content-type": "application/json"
    }

    response = requests.post(webhook_url, data, headers=header)

    if response.status_code == 401:
        return False
    else:
        return webhook_url