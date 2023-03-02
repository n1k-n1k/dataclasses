from abc import ABC
from typing import Dict, List, Any, Type, Optional, Union, Iterable

from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped

from metaclass.mapper import dataclass_mapper


class ABCSuperPet(ABC):
    __mnemonic__: str = "parent_pet"


class ABCPet(ABCSuperPet):
    __mnemonic__: str = "parent_pet"


# @dataclass_mapper.mapped_as_dataclass(unsafe_hash=True)
class Cat(ABCPet):
    __tablename__ = 'cats_table'
    __table_args__ = {"comment": "cat comment"}
    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=True, comment="pet_name")


# @dataclass_mapper.mapped_as_dataclass(unsafe_hash=True)
class Dog(ABCPet):
    __mnemonic__: str = "gog_mnemonic"
    __tablename__ = 'dog_table'
    __table_args__ = {"comment": "dog comment"}
    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=True, comment="pet_name")


if __name__ == '__main__':
    from devtools import debug

    # cat = Cat(name='mew')
    cat = Cat()
    debug(cat)
    print()
