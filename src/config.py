import msgspec
import tomllib


class ForwardConfig(msgspec.Struct):
    domain: str
    path: str
    timeout: int = 1


class Config(msgspec.Struct):
    forward: ForwardConfig


def load_config(config_path: str = "config.toml") -> Config | None:
    try:
        with open(config_path, "rb") as file:
            data = tomllib.load(file)
    except Exception as e:
        print(f"Something goes wrong: {e}")
        return None
        # TODO: Proper logging

    try:
        return msgspec.convert(data, Config)
    except msgspec.ValidationError as e:
        print(f"Configuration validation failed: {e}")
        return None
        # TODO: Proper logging


raw_config = load_config()

if raw_config is None:
    pass
    # TODO: Exit app
else:
    config = raw_config
