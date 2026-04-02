from __future__ import annotations

from urllib.parse import parse_qsl
from urllib.parse import urlencode
from urllib.parse import urlsplit
from urllib.parse import urlunsplit

TRACKING_PARAM_PREFIXES = ("utm_",)
TRACKING_PARAMS = {
    "fbclid",
    "gclid",
    "dclid",
    "mc_cid",
    "mc_eid",
    "igshid",
}


def normalize_url(url: str) -> str:
    raw = url.strip()
    if not raw:
        raise ValueError("url is empty")

    split = urlsplit(raw)
    if not split.scheme or not split.netloc:
        raise ValueError(f"invalid absolute url: {url}")

    scheme = split.scheme.lower()
    hostname = (split.hostname or "").lower()
    port = split.port

    if port is None:
        netloc = hostname
    elif (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
        netloc = hostname
    else:
        netloc = f"{hostname}:{port}"

    filtered_query: list[tuple[str, str]] = []
    for key, value in parse_qsl(split.query, keep_blank_values=True):
        lowered = key.lower()
        if lowered.startswith(TRACKING_PARAM_PREFIXES):
            continue
        if lowered in TRACKING_PARAMS:
            continue
        if not key:
            continue
        filtered_query.append((key, value))

    query = urlencode(filtered_query, doseq=True)
    return urlunsplit((scheme, netloc, split.path, query, ""))
