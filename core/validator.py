def validate_target(target):

    if not target: 
        raise ValueError("Target cannot be empty")
    if not (target.startswith("http://") or target.startswith("https://")):
        raise ValueError("Invalid URL scheme")
    blocked_hosts = [
        "127.0.0.1",
        "localhost",
        "0.0.0.0"
    ]
    if any(host in target for host in blocked_hosts):
        raise ValueError("Blocked target")
    return target