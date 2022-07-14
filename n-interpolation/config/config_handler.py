import yaml


def load_config(config_file):
    with open(config_file, 'r') as f:
        config = yaml.load(f)
    return config


def save_config(config_file, config):
    with open(config_file, 'w') as f:
        yaml.dump(config, f)
    return config
