from utils.crawler import Crawler
from utils.text_process import TextProcess
from utils.checkpoint import Checkpoint
from utils.tools import merge
import time
import os
import threading
import random


class Main:
    def __init__(self, thread_num=1):
        self.bookname = None
        self.thread_num = thread_num
        self.crawler = Crawler()
        self.process = TextProcess()
        self.checkpoint = Checkpoint()

    def download_book(self, url, bookname='novel'):
        self.bookname = bookname
        chapters = self.crawler.extract_chapters(url)
        # 记录所有待爬取的章节
        self.checkpoint.set_remain(chapters, self.bookname)
        self.download_multi_thread()

    def download_book_from_checkpoint(self):
        self.bookname = self.checkpoint.load_checkpoint()
        self.download_multi_thread()

    def download_multi_thread(self):
        threads = []
        for _ in range(self.thread_num):
            thread = threading.Thread(target=self.download_thread)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

    def download_thread(self):
        while True:
            chapter = self.checkpoint.get_chapter()
            if chapter is None:
                break

            signal = self.download_single_chapter(chapter)

            if signal:  # 本章成功爬取
                self.checkpoint.remove_from_working(chapter)
            else:  # 爬取失败
                self.checkpoint.move_to_error(chapter)
                
            self.checkpoint.save_checkpoint()

            time.sleep(random.uniform(0.1, 1))

    def download_single_chapter(self, chapter):
        for i in range(5):
            try:
                title, text = self.crawler.extract_text(chapter['url'])
                text = self.process.process(text)
                self.save(chapter['id'], chapter['chapter_name'], text)
                return True
            except Exception as e:
                time.sleep(2 ** i)
        return False

    def save(self, id_, title, text):
        path = os.path.join('data', self.bookname)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, '{:0>4} {}.txt'.format(id_ + 1, title)), 'w', encoding='utf-8') as f:
            f.write(title + '\n' + text + '\n')


if __name__ == "__main__":
    app = Main(10)
    # 首次下载
    # app.download_book('https://m.bqg9527.cc/book/383070/', '哥布林进化系统')

    # 从检查点继续下载
    app.download_book_from_checkpoint()
    # merge(app.bookname)
