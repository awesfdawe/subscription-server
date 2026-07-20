from functools import cache
import msgspec
import os
from tinydb import TinyDB, Storage


class MsgspecStorage(Storage):
    def __init__(self, filename: str):
        self.filename = filename
        self.json_decoder = msgspec.json.Decoder()
        self.json_encoder = msgspec.json.Encoder()

    def read(self):
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            return None

        with open(self.filename, "rb") as f:
            return self.json_decoder.decode(f.read())

    def write(self, data):
        with open(self.filename, "wb") as f:
            f.write(self.json_encoder.encode(data))

    def close(self):
        pass

@cache
def get_db() -> TinyDB:
    return TinyDB("db.json", storage=MsgspecStorage)
