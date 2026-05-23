from pydantic import BaseModel, Field
from typing import Any, Literal


class XhttpReuseSettings(BaseModel):
    max_concurrency: str | None = Field(default=None, validation_alias="max-concurrency")
    max_connections: str | None = Field(default=None, validation_alias="max-connections")
    c_max_reuse_times: str | None = Field(default=None, validation_alias="c-max-reuse-times")
    h_max_request_times: str | None = Field(default=None, validation_alias="h-max-request-times")
    h_max_reusable_secs: str | None = Field(default=None, validation_alias="h-max-reusable-secs")
    h_keep_alive_period: int | None = Field(default=None, validation_alias="h-keep-alive-period")


class XhttpTransport(BaseModel):
    transport: Literal["xhttp"] = "xhttp"

    path: str = "/"
    host: str | None = None
    mode: Literal["auto", "stream-one", "stream-up", "packet-up"] = "auto"

    headers: dict[str, str] | None = None
    no_grpc_header: bool | None = Field(default=None, validation_alias="no-grpc-header")

    uplink_http_method: Literal["POST", "GET", "PUT", "PATCH", "DELETE"] | None = Field(
        default=None, validation_alias="uplink-http-method"
    )
    uplink_data_placement: Literal["auto", "body", "cookie", "header"] | None = Field(
        default=None, validation_alias="uplink-data-placement"
    )
    uplink_data_key: str | None = Field(default=None, validation_alias="uplink-data-key")
    uplink_chunk_size: str | None = Field(default=None, validation_alias="uplink-chunk-size")

    session_placement: Literal["path", "query", "cookie", "header"] | None = Field(
        default=None, validation_alias="session-placement"
    )
    session_key: str | None = Field(default=None, validation_alias="session-key")
    seq_placement: Literal["path", "query", "cookie", "header"] | None = Field(
        default=None, validation_alias="seq-placement"
    )
    seq_key: str | None = Field(default=None, validation_alias="seq-key")

    sc_max_each_post_bytes: str | None = Field(default=None, validation_alias="sc-max-each-post-bytes")
    sc_min_posts_interval_ms: str | None = Field(default=None, validation_alias="sc-min-posts-interval-ms")
    sc_max_buffered_posts: int | None = Field(default=None, validation_alias="sc-max-buffered-posts")

    x_padding_bytes: int | None = Field(default=None, validation_alias="x-padding-bytes")
    x_padding_obfs_mode: bool | None = Field(default=None, validation_alias="x-padding-obfs-mode")
    x_padding_key: str | None = Field(default=None, validation_alias="x-padding-key")
    x_padding_header: str | None = Field(default=None, validation_alias="x-padding-header")
    x_padding_placement: Literal["queryInHeader", "cookie", "header", "query"] | None = Field(
        default=None, validation_alias="x-padding-placement"
    )
    x_padding_method: Literal["repeat-x", "tokenish"] | None = Field(default=None, validation_alias="x-padding-method")

    reuse_settings: XhttpReuseSettings | None = Field(default=None, validation_alias="reuse-settings")
    download_settings: dict[str, Any] | None = Field(default=None, validation_alias="download-settings")
