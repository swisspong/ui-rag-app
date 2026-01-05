from hashlib import md5
from typing import Any


def compute_args_hash(*args: Any) -> str:
    args_str = "".join(str(arg) for arg in args)
    try:
        return md5(args_str.encode("utf-8")).hexdigest()
    except UnicodeEncodeError:
        safe_bytes = args_str.encode("utf-8", errors="replace")
        return md5(safe_bytes).hexdigest()
