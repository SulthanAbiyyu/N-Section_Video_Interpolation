import yaml


def load_config(config_file="./ninterpolation/config/cfg.yaml"):
    with open(config_file, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def save_config(config_file, config):
    with open(config_file, 'w') as f:
        yaml.dump(config, f)
    return config
