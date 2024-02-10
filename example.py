from animangaparser import Parser, EmailSender
from animangaparser import check
from os import getenv

from selenium import webdriver
from selenium.webdriver.common.by import By

import smtplib, ssl


class MailRuSender(EmailSender):
    def send_msg(self, msg: str) -> None:
        print("sending email...")
        ctx = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.mail.ru', self.port, context=ctx) as server:
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.target, msg)


class MangaLibParser(Parser):
    def __init__(self, title: str, url: str, last_read_chapter: int, driver: webdriver.Firefox):
        super().__init__(title, url, last_read_chapter)
        self.driver = driver

    def get_last_chapter(self) -> int:
        print(f'checking {self.title} for updates')
        xpath_to_last_chapter = '//*[@id="main-page"]/div/div[2]/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/a'
        self.driver.get(self.url)
        res = self.driver.find_element(By.XPATH, xpath_to_last_chapter).text.split()
        ch = int(res[3])
        return ch


parsers = []
email = MailRuSender(
    sender=getenv('sender'),
    password=getenv('pwd'),
    target=getenv('target')
)

urls = { # format: '<title of manga>': [last_read_chapter, '<url>']
    'juujika-no-rokunin': [155, 'https://mangalib.me/juujika-no-rokunin?section=chapters&ui=1899066'],
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

opt = webdriver.FirefoxOptions()
opt.add_argument('--headless')
opt.binary_path = '/usr/bin/geckodriver'
driver = webdriver.Firefox(options=opt)


for title, [lrc, url] in urls.items():
    parsers.append(MangaLibParser(title, url, lrc, driver))


check(parsers, email, 12 * 60 * 60)
