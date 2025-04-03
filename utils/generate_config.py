from urllib.parse import urlparse
from .config_manager import ConfigManager
from .tools import get_tree


def get_xpath(element):
    path = []
    while element is not None:
        tag = element.tag
        siblings = [sib for sib in element.itersiblings(preceding=True) if sib.tag == tag]
        index = len(siblings) + 1
        if index > 1:
            path.append(f"{tag}[{index}]")
        else:
            path.append(tag)
        element = element.getparent()
    path.reverse()
    return '/' + '/'.join(path)


class Analyser:
    def __init__(self):
        self.config_manager = ConfigManager()

    def generate_config(self, domain, html, chapter_name, title):
        # 暂时空着，后续可添加具体提取逻辑
        chapter_tag = html.xpath('//*[contains(text(), "{}")]'.format(chapter_name))
        xpath = get_xpath(chapter_tag[0])
        print(xpath)
        url = domain + xpath.xpath('//@href')
        return {
            'extract_chapters_selector': {
                'chapter_list': '',
                'chapter_name': '',
                'url': ''
            },
            'extract_text_selector': {
                'title': '',
                'text': ''
            }
        }

    def save_config(self, domain, config):
        return
        self.config_manager.add_site_config(domain, config)

    def analyse_site(self, url, **kwargs):
        # 请求html
        html = get_tree(url, self.config_manager.get_headers())
        # 解析域名
        domain = urlparse(url).netloc
        domain = 'https://' + domain

        config = self.generate_config(domain, html, **kwargs)
        self.save_config(domain, config)


if __name__ == "__main__":
    analyser = Analyser()
    # 这里可以替换为实际的书籍目录 URL
    url = 'https://m.bqg9527.cc/book/383070/'
    analyser.analyse_site(url)
