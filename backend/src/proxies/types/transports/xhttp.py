from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, Literal


class XhttpReuseSettings(BaseModel):
    max_concurrency: Optional[str] = Field(default=None, validation_alias="max-concurrency")
    max_connections: Optional[str] = Field(default=None, validation_alias="max-connections")
    c_max_reuse_times: Optional[str] = Field(default=None, validation_alias="c-max-reuse-times")
    h_max_request_times: Optional[str] = Field(default=None, validation_alias="h-max-request-times")
    h_max_reusable_secs: Optional[str] = Field(default=None, validation_alias="h-max-reusable-secs")
    h_keep_alive_period: Optional[int] = Field(default=None, validation_alias="h-keep-alive-period")


class XhttpTransport(BaseModel):
    network: Literal["xhttp"] = "xhttp"

    path: str = "/"
    host: Optional[str] = None
    mode: Literal["auto", "stream-one", "stream-up", "packet-up"] = "auto"

    headers: Optional[Dict[str, str]] = None
    no_grpc_header: Optional[bool] = Field(default=None, validation_alias="no-grpc-header")

    uplink_http_method: Optional[Literal["POST", "GET", "PUT", "PATCH", "DELETE"]] = Field(
        default=None, validation_alias="uplink-http-method"
    )
    uplink_data_placement: Optional[Literal["auto", "body", "cookie", "header"]] = Field(
        default=None, validation_alias="uplink-data-placement"
    )
    uplink_data_key: Optional[str] = Field(default=None, validation_alias="uplink-data-key")
    uplink_chunk_size: Optional[str] = Field(default=None, validation_alias="uplink-chunk-size")

    session_placement: Optional[Literal["path", "query", "cookie", "header"]] = Field(
        default=None, validation_alias="session-placement"
    )
    session_key: Optional[str] = Field(default=None, validation_alias="session-key")
    seq_placement: Optional[Literal["path", "query", "cookie", "header"]] = Field(default=None, validation_alias="seq-placement")
    seq_key: Optional[str] = Field(default=None, validation_alias="seq-key")

    sc_max_each_post_bytes: Optional[str] = Field(default=None, validation_alias="sc-max-each-post-bytes")
    sc_min_posts_interval_ms: Optional[str] = Field(default=None, validation_alias="sc-min-posts-interval-ms")
    sc_max_buffered_posts: Optional[int] = Field(default=None, validation_alias="sc-max-buffered-posts")

    x_padding_bytes: Optional[str] = Field(default=None, validation_alias="x-padding-bytes")
    x_padding_obfs_mode: Optional[bool] = Field(default=None, validation_alias="x-padding-obfs-mode")
    x_padding_key: Optional[str] = Field(default=None, validation_alias="x-padding-key")
    x_padding_header: Optional[str] = Field(default=None, validation_alias="x-padding-header")
    x_padding_placement: Optional[Literal["queryInHeader", "cookie", "header", "query"]] = Field(
        default=None, validation_alias="x-padding-placement"
    )
    x_padding_method: Optional[Literal["repeat-x", "tokenish"]] = Field(default=None, validation_alias="x-padding-method")

    reuse_settings: Optional[XhttpReuseSettings] = Field(default=None, alvalidation_aliasias="reuse-settings")
    download_settings: Optional[Dict[str, Any]] = Field(default=None, validation_alias="download-settings")
