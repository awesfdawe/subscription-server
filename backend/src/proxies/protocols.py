# from pydantic import BaseModel, Field
# from typing import Any, Dict, Optional, Literal, List
# from urllib.parse import ParseResult, urlparse, parse_qsl

# class ProxyBase(BaseModel):
#     server: str
#     port: int

#     @classmethod
#     def from_url(cls, url: str):
#         parsed = urlparse(url)

#         base_data = {"server": parsed.hostname, "port": parsed.port}

#         return cls._parse_extra(parsed, base_data)

#     @classmethod
#     def _parse_extra(cls, parsed: ParseResult, base_data):
#         return cls(**base_data)


# class VlessConfig(ProxyBase):
#     uuid: str
#     security: str = "none"
#     flow: Optional[Literal["xtls-rprx-vision"]]
#     sni: str
#     fingerprint: str = Field(default="chrome", validation_alias="fp")
#     public_key: str = Field(validation_alias="pbk")
#     short_id: str | None = Field(default=None, validation_alias="sid")

#     @classmethod
#     def _parse_extra(cls, parsed: ParseResult, base_data: dict):
#         query_params = dict(parse_qsl(parsed.query))

#         extra_data = {**base_data, **query_params, "uuid": parsed.username}

#         return cls(**extra_data)
