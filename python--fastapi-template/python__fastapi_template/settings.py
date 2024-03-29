import yaml

from dataclasses import dataclass

@dataclass
class AppConfig:
    environment: str = "development"
    dbtype: str = ""
    dbname: str = ""

def get_settings() -> AppConfig:
    """Get application settings from configuration file"""

    with open('config/settings.yaml', 'r') as yml:
        config = yaml.load(yml, Loader=yaml.FullLoader)['app']

    return AppConfig(
        environment=config['environment'],
        dbtype=config['dbtype'],
        dbname=config['dbname'],
    )
