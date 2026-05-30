from tools.tool_validator import validate_code

def load_tools_from_string(tool_code: str):
    if not validate_code(tool_code):
        raise ValueError("Unsafe code detected")

    local_scope = {}

    safe_globals = {
    "__builtins__": {
        "abs": abs,
        "min": min,
        "max": max,
        "sum": sum,
        "range": range,

        # ✅ ADD THESE
        "int": int,
        "float": float,
        "str": str,
        "len": len
    }
}

    exec(tool_code, safe_globals, local_scope)

    tools = [
        obj for obj in local_scope.values()
        if callable(obj)
    ]

    return tools

from models import Tool
from db import SessionLocal

def load_tools_from_db():
    db = SessionLocal()

    try:
        tools = db.query(Tool).all()

        loaded_tools = []

        for t in tools:
            funcs = load_tools_from_string(t.code)
            loaded_tools.extend(funcs)

        return loaded_tools

    finally:
        db.close()