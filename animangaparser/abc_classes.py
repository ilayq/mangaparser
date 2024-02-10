from abc import ABC, abstractmethod


class Parser(ABC):
    def __init__(self, title: str, url: str, last_read_chapter: int):
        self.title = title
        self.url = url
        self.last_read_chapter = last_read_chapter

    @abstractmethod
    def get_last_chapter(self) -> int:
        raise NotImplemented("Please implement get_last_chapter method")

    def has_new_chapter(self) -> bool:
        try: 
            return self.last_read_chapter < self.get_last_chapter()
        except Exception as e:
            print(e)
            return False


class EmailSender(ABC):
    def __init__(self, sender: str, password: str, target: str):
        self.sender = sender
        self.password = password
        self.target = target
        self.port = 465 # default port, can be changed
    
    @abstractmethod
    def send_msg(self, msg: str) -> None:
        raise NotImplemented("Please implement send_msg method") 
