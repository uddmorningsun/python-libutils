from urllib.parse import urljoin, urlsplit, SplitResult


def urljoin_v2(address, path: str) -> str:
    """Workaround for urljoin("http://1.2.3.4:80/foo", "/api/v1") => 'http://1.2.3.4:80/api/v1'"""
    if not address.startswith(("http://", "https")):
        raise ValueError("address must start with the http:// or https://")
    if not path:
        return address
    parts = urlsplit(address)  # type: SplitResult
    # urljoin("/api/v1", "users") => '/api/users'; urljoin("/api/v1/", "users") => '/api/v1/users'
    parts_path = parts.path
    if parts_path and parts_path[-1] != "/":
        parts_path = parts_path + "/"
    # https://stackoverflow.com/a/1793282
    return "%s://%s%s" % (
        parts.scheme,
        parts.netloc,
        urljoin(parts_path or "/", path[1:] if path[:1] == "/" else path),
    )
