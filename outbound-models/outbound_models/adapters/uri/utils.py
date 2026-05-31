def _get_param(query: dict[str, list[str]], key: str) -> str | None:
    values = query.get(key)
    return values[0] if values else None
