from selenium import webdriver;
from selenium.webdriver.common.by import By

import os
import smtplib, ssl
import time


SENDER = os.getenv('sender')
TARGET = os.getenv('target') 
PASSWORD = os.getenv('pwd') 
PORT = 465
UPDATE_TIME = 12 * 60 * 60 # time between checks for new chapters
XPATH_TO_LAST_CHAPTER = '//*[@id="main-page"]/div/div[2]/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/a'


opt = webdriver.FirefoxOptions()
opt.add_argument('--headless')
driver = webdriver.Firefox(options=opt)

urls = { # format: '<title of manga>': [last_read_chapter, '<url>']
    'kenshin': [135, 'https://mangalib.me/rurouni_kenshin?section=chapters&ui=1899066'],
    'juujika-no-rokunin': [154, 'https://mangalib.me/juujika-no-rokunin?section=chapters&ui=1899066'],
    'one-piece': [1106, 'https://mangalib.me/one-piece?section=chapters&ui=1899066'],
    'chainsaw-man': [154, 'https://mangalib.me/chainsaw-man-2?section=chapters&ui=1899066'],
    'tower-of-god': [179, 'https://mangalib.me/tower-of-god?section=chapters&ui=1899066'],
    'guran-buru': [91, 'https://mangalib.me/guran-buru?section=chapters&ui=1899066'],
    'ao-no-miburu': [9, 'https://mangalib.me/ao-no-miburo?section=chapters&ui=1899066'],
    'kagura-bachi': [19, 'https://mangalib.me/kagura-bachi?section=chapters&ui=1899066'],
    'real': [95, 'https://mangalib.me/real?section=chapters&ui=1899066'],
    'sousou-no-frieren': [88, 'https://mangalib.me/sousou-no-frieren?section=chapters&ui=1899066'],
    'yofukashi-no-uta': [77, 'https://mangalib.me/yofukashi-no-uta?section=chapters&ui=1899066'],
    'ao-ashi': [358, 'https://mangalib.me/ao-ashi?section=chapters&ui=1899066'],
}


def send_email(msg: str, sender=SENDER, password=PASSWORD, port=PORT, target=TARGET):
    print("sending email...")
    ctx = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.mail.ru', port, context=ctx) as server:
        server.login(sender, password)
        server.sendmail(sender, target, msg)


def has_new_chapter(url: str, last_read_chapter: int) -> bool:
    print(f'cheching {url} for new chapters...')
    driver.get(url)
    res = driver.find_element(By.XPATH, XPATH_TO_LAST_CHAPTER).text.split()
    ch = int(res[3])
    return last_read_chapter < ch
     

def main():
    new_chapters: list[str] = []

    for title, [last_read_chapter, url] in urls.items():
        try:
            if has_new_chapter(url, last_read_chapter):
                new_chapters.append(title)
                urls[title][0] += 1
        except Exception as e:
            print(e)
            continue

    if not new_chapters:
        return
    
    msg = f'{", ".join(new_chapters)} have new chapters'
    send_email(msg)


if __name__ == '__main__':
    while 1:
        main()
        print('sleeping...')
        time.sleep(UPDATE_TIME)

