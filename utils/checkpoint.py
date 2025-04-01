import time
import os
import json
import threading


class Checkpoint:
    dir_name = 'data'

    def __init__(self):
        self.bookname = None
        self.remain = []
        self.working = []
        self.error = []
        self.lock = threading.Lock()

    def get_info(self):
        return len(self.remain), len(self.working), len(self.error)

    def set_remain(self, chapters, bookname):
        self.remain = chapters
        self.bookname = bookname

    def get_chapter(self):
        self.lock.acquire()
        if self.remain:
            chapter = self.remain.pop(0)
            self.working.append(chapter)
        else:
            chapter = None
        self.lock.release()
        return chapter

    def move_to_error(self, chapter):
        self.lock.acquire()
        self.working.remove(chapter)
        self.error.append(chapter)
        self.lock.release()

    def remove_from_working(self, chapter):
        self.lock.acquire()
        self.working.remove(chapter)
        self.lock.release()

    def save_checkpoint(self):
        """保存检查点"""
        if not os.path.exists(self.dir_name):
            os.mkdir(self.dir_name)
        checkpoint_path = os.path.join(self.dir_name, 'checkpoint.json')
        checkpoint = {
            'bookname': self.bookname,
            'remain': self.remain,
            'working': self.working,
            'error': self.error,
        }
        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, ensure_ascii=False, indent=4)

    def load_checkpoint(self, reset_error=True):
        """加载检查点"""
        checkpoint_path = os.path.join(self.dir_name, 'checkpoint.json')
        with open(checkpoint_path, 'r', encoding='utf-8') as f:
            checkpoint = json.load(f)
            self.bookname = checkpoint['bookname']
            self.remain = checkpoint['remain'] + checkpoint['working']
            self.working = []
            if reset_error:
                self.remain += checkpoint['error']
                self.error = []
            else:
                self.error = checkpoint['error']
        return self.bookname
