from TelegramProjects.helpers.functions import loadConfig


def test_load_config():
    config = loadConfig()
    assert config, "Couldn't load config"
    return config
