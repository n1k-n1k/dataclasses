from pydantic import BaseModel
from pydantic.main import ModelMetaclass

from typing import Dict, List, Any, Type, Optional, Union, Iterable

from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped

from metaclass.mapper import dataclass_mapper

_classes = {}  # type: Dict[str, Type[BaseDataclass]]




def get_class_mnemonics() -> List[str]:
    """Возвращает все мнемонические имена зарегистрированы классов"""
    return list(_classes.keys())


def get_class(name: str) -> Type['BaseDataclass']:
    """Возвращает классы (именно классы, не объекты) по мнемоническому имени"""

    metrics_class = _classes.get(name, None)
    if metrics_class is None:
        raise KeyError(
            f"class name should be one of this: {get_class_mnemonics()}, but given `{name}`")
    return metrics_class


# class DataclassMeta(ModelMetaclass):
class DataclassMeta:
    __mnemonic__: str | None

    """Метакласс, который будет отслеживать, когда мы объявляем новый класс-наследник :class:`BaseEDataclass`
       Классы записываются в глобальный словарь _classes, ключами словаря являются
       атрибут ``__mnemonic__`` каждого класса.
    """

    def __init__(self, name, bases, attrs):
        """Вызывается каждый раз, когда объявляется класс проверок (наследник :class:`BaseDataclass`)"""
        # super().__init__(name, bases, attrs)
        # if "__mnemonic__" not in self.__dict__:
        #     raise AttributeError("__mnemonic__ class attribute should be provided in this class")
        print()
        if self.__mnemonic__ in _classes:
            raise AttributeError(f"__mnemonic__ `{self.__mnemonic__}` already registered!")
        _classes[self.__mnemonic__] = self


# class BaseDataclass(BaseModel, metaclass=DataclassMeta):
#     """Базовый класс
#
#     Переопределяемые в наследниках атрибуты:
#         * `__mnemonic__` - мнемоническое имя.
#         * `_aggregation_statement` - шаблон данных.
#     """
#
#     __mnemonic__: str = "basic"
#     _aggregation_statement: Optional[Union[str, List[str]]] = None
#
#     field: Optional[str]
#
#     def __init__(self, field: str, **data: Any):
#         super().__init__(**data)
#         self.field = field
#
#     def __call__(self, *args, **kwargs):
#         self.calculate(*args, **kwargs)
#
#     def calculate(self):
#         if self._aggregation_statement is None:
#             raise NotImplementedError(
#                 "Please set _aggregation_statement or implement calculate(...) method in your child classes!")

@dataclass_mapper.mapped_as_dataclass(unsafe_hash=True)
# class Cat:
class Cat(metaclass=DataclassMeta):
    __mnemonic__: str = "cat_mnemonic"
    __tablename__ = 'cats'
    __table_args__ = {"comment": "cat comment"}
    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=True, comment="cat_name")

    def __post_init__(self):
        pass

if __name__ == '__main__':
    from devtools import debug
    mnms = get_class_mnemonics()
    print(mnms)

    cat = Cat(name='nnm')
    debug(cat)
    print()




