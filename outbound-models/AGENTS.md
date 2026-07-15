# Project Overview
`outbound-models` is a Python library written on top of msgspec for serializing and deserializing advanced proxy client-side configurations (server-side only options out of scope). It provides strict type safety, validation, parsing, and conversion for various proxy formats (e.g., Xray, Sing-box, Mihomo Clash).

## Project Architecture
Project separated into 3 main domains:
- `outbound_models/models`: Contains msgspec models that input data converts into.
- `outbound_models/adapters`: Contains adapters for converting between different proxy formats.
- `outbound_models/schemas`: Contains schemas for different proxy formats.

## Testing instructions
- Use `ty check` to run Python type checking.
- Use `ruff check` to run Python basic errors checking.
- Use `pytest` to run unit tests.
