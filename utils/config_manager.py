import yaml
import os

class ConfigManager:
    def __init__(self, config_path='config/crawler_config.yaml'):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {'headers': {}, 'sites': {}}

    def save_config(self, config):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

    def get_site_config(self, site_name):
        return self.config.get('sites', {}).get(site_name)

    def get_headers(self):
        return self.config.get('headers', {})

    def add_site_config(self, site_name, site_config):
        """
        添加或覆盖指定网站的配置信息
        :param site_name: 网站名称
        :param site_config: 网站配置信息
        """
        sites = self.config.setdefault('sites', {})
        sites[site_name] = site_config
        self.save_config(self.config)
