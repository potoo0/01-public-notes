# flake8: noqa
# 部分类型可能是高版本引入，可使用 typing_extensions 包
# 部分 hint 使用方式低版本不支持, 可通过 `from __future__ import annotations` 来支持(3.7+)
#      __future__ 模块的说明: https://docs.python.org/zh-cn/3/library/__future__.html
#      比如 Union 简化为 |, 以及类型自指不加引号 等
from typing import List, Dict, Tuple, Callable, Protocol, Any, TypeAlias, Self, TypeVar, Type

# 1. 类型别名, 建议使用 TypeAlias 来增强可读性
# https://peps.python.org/pep-0484/#type-aliases
# https://peps.python.org/pep-0613/#abstract  加入 TypeAlias
Options = Dict[str, str]
option: Options

FOO: TypeAlias = Tuple[List[str], Dict[str]]
foo: FOO

# 2. 元组
addr: Tuple[str, int]


# 3. 函数
# 3.1 str int 输入, str 返回
# https://peps.python.org/pep-0484/#callable
def invoke_func_simple(func: Callable[[str, int | None], str]):
    func('lc', 80)


def func_simple(host: str, port: int | None) -> str: ...


invoke_func_simple(func_simple)


# 3.2 复杂函数使用 Protocol
# https://peps.python.org/pep-0544/#defining-a-protocol
class Handler(Protocol):
    def __call__(self, host: str, port: int | None, e: Exception | None = None) -> Any: ...


def invoke_func(func: Handler):
    func('lc', 80)


def func_default_val(host: str, port: int | None, e: Exception | None = None) -> str: ...


invoke_func(func_default_val)


# 4. Forward references
# https://peps.python.org/pep-0484/#forward-references
# 如果一个类型还未被指定, 则可以使用 引号 包裹作为字符串
# 如不要引号, 需导入 `from __future__ import annotations`
class Node:
    def add(self) -> 'Node': ...


# 4. 类型自指 Self Type
# https://peps.python.org/pep-0673/
# 两种方式:
#       a. 直接注明自身类名
#       b. 使用 typing.Self


class Shape:
    def set_scale(self, scale: float) -> Self:
        print(scale)
        return self

    @staticmethod
    def of() -> 'Shape': ...


class Circle(Shape):
    def set_radius(self, radius: float) -> Self:
        print(radius)
        return self


Shape.of().set_scale(1)  # => should be Shape
Circle().set_scale(1).set_radius(2)  # => should be Circle
