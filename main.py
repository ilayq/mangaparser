from selenium import webdriver;
from selenium.webdriver.common.by import By


import smtplib, ssl
import time


SENDER = 'fedotovmike1997@mail.ru'
TARGET = 'ilayfeeed@gmail.com'
PASSWORD = 'RHuYPiLVCnhuj4Gw65bZ'
PORT = 465
UPDATE_TIME = 12 * 60 * 60 # time between checks for new chapters
XPATH_TO_LAST_CHAPTER = '//*[@id="main-page"]/div/div[2]/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/a'

opt = webdriver.ChromeOptions()
opt.add_argument('--headless')
opt.add_argument('--window-size=1920,1080')
driver = webdriver.Chrome(options=opt)

urls = { # format: '<title of manga>': [last_read_chapter, '<url>']
    'kenshin': [135, 'https://mangalib.me/rurouni_kenshin?section=chapters&ui=1899066']
}


def send_email(msg: str, sender=SENDER, password=PASSWORD, port=PORT, target=TARGET):
    ctx = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.mail.ru', port, context=ctx) as server:
        server.login(sender, password)
        server.sendmail(sender, target, msg)


def has_new_chapter(url: str, last_read_chapter: int) -> bool:
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
        except:
            continue

    if not new_chapters:
        return
    
    msg = f'{", ".join(new_chapters)} have new chapters'
    send_email(msg)


if __name__ == '__main__':
    while 1:
        main()
        time.sleep(UPDATE_TIME)
