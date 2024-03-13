from .a import foo
from .b import bar


def baz(n: int) -> int:
    return foo(n) + bar(n)
