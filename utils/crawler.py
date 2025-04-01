import requests
import yaml
from lxml import etree
from urllib.parse import urlparse
from urllib.parse import urljoin


def get_tree(url, headers):
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = response.apparent_encoding
    return etree.HTML(response.text)


def get_site_name(url):
    site_name = f'https://{urlparse(url).netloc}'
    return site_name


class Crawler:
    def __init__(self):
        self.site_name = None
        # 从配置文件中读取全局 headers 信息
        self.headers = None

    def load_config(self, site_name):
        with open('config/crawler_config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        site_config = config.get('sites', {}).get(site_name)
        if not site_config:
            raise ValueError(f"未找到 {site_name} 的配置信息。")
        
        # 加载到属性
        self.headers = config.get('headers', {})
        self.site_name = site_name
        self.site_config = site_config

    def extract_chapters(self, url):
        """
        输入书籍目录地址 url 获取章节信息
        返回列表 chapters：每个元素为一个章节的信息，按第一章到最后一章排序，每个章节信息为字典，包含 chapter_name, url
        """
        site_name = get_site_name(url)
        if self.site_name != site_name:
            self.load_config(site_name)
            
        tree = get_tree(url, self.headers)
        chapters = []
        chapter_list = tree.xpath(self.site_config['extract_chapters_selector']['chapter_list'])
        for i, chapter in enumerate(chapter_list):
            url = chapter.xpath(self.site_config['extract_chapters_selector']['url'])
            chapter_name = chapter.xpath(self.site_config['extract_chapters_selector']['chapter_name'])
            chapter_info = {
                'id': i,
                'chapter_name': chapter_name.strip(),
                'url': url.strip()
            }
            chapters.append(chapter_info)
        return chapters

    def extract_text(self, url):
        """
        输入章节地址 url
        输出章节标题 title 和正文 text
        """
        site_name = get_site_name(url)
        if self.site_name != site_name:
            self.load_config(site_name)

        tree = get_tree(url, self.headers)
        title = tree.xpath(self.site_config['extract_text_selector']['title'])[0]
        text = tree.xpath(self.site_config['extract_text_selector']['text'])
        text = '\n'.join(text)
        return title.strip(), text.strip()
    