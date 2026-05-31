def validate_code(code: str) -> bool:
    banned_keywords = [
        "import",
        "os",
        "sys",
        "__",
        "open",
        "eval",
        "exec"
    ]

    for keyword in banned_keywords:
        if keyword in code:
            return False
    return True