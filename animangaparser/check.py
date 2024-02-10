from .abc_classes import EmailSender, Parser
from time import sleep


def check(parsers: list[Parser], emailsender: EmailSender, timeout: int):
    while 1:
        new_chapters_titles = []
        for parser in parsers:
            if parser.has_new_chapter():
                new_chapters_titles.append(parser.title)

        if new_chapters_titles:
            msg = f"{', '.join(new_chapters_titles)} have new updates"
            emailsender.send_msg(msg)

        print(f'sleeping for {timeout} seconds...')
        sleep(timeout)
