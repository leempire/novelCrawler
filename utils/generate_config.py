import requests
import yaml
from urllib.parse import urlparse


class Analyser:
    def generate_config(self, html_content):
        # 暂时空着，后续可添加具体提取逻辑
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
        try:
            with open('config/crawler_config.yaml', 'r', encoding='utf-8') as f:
                existing_config = yaml.safe_load(f)
            if existing_config is None:
                existing_config = {'headers': {}, 'sites': {}}
            # 不管域名是否存在，直接覆盖或新增
            existing_config['sites'][domain] = config
            with open('config/crawler_config.yaml', 'w', encoding='utf-8') as f:
                yaml.dump(existing_config, f, allow_unicode=True, default_flow_style=False)
        except FileNotFoundError:
            print("未找到配置文件，请检查 config 目录下是否存在 crawler_config.yaml 文件。")

    def analyse_site(self, url):
        try:
            # 获取全局 headers
            with open('config/crawler_config.yaml', 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            headers = config.get('headers', {})
            response = requests.get(url, headers=headers)
            response.encoding = response.apparent_encoding
            html_content = response.text
            domain = urlparse(url).netloc
            config = self.generate_config(html_content)
            self.save_config(domain, config)
            print(f"已为域名 {domain} 生成并保存配置。")
        except requests.RequestException as e:
            print(f"请求 URL 时出错: {e}")
        except Exception as e:
            print(f"分析网站时出错: {e}")


if __name__ == "__main__":
    analyser = Analyser()
    # 这里可以替换为实际的书籍目录 URL
    url = 'https://example.com/book/catalog'
    analyser.analyse_site(url)
