import re


class TextProcess:
    def __init__(self):
        pass

    def process(self, text):
        """将正文加工为可读形式"""
        text = [p.strip() for p in text.split('\n')]
        text = '\n'.join(text)
        text = re.sub(r'\n+', '\n', text)
        return text
