from datetime import datetime
from enum import Enum
from typing import List, Optional, Callable

from pydantic import BaseModel, SecretStr, Field


_people = []  # type: List[Person]


class LoginConflict(Exception):
    pass


class PersonNotFound(Exception):
    pass


class PersonStatus(str, Enum):
    active = 'active'
    deleted = 'deleted'


class Person(BaseModel):
    id: int
    name: str
    login: str
    status: PersonStatus
    created_at: datetime
    updated_at: datetime = None
    deleted_at: datetime = None
    last_seen_at: datetime = None
    _password: SecretStr

    def __eq__(self, other):
        return isinstance(other, Person) and self.id == other.id


class Gem(BaseModel):
    id: int
    name: str


class Elf(Person):
    favourite_gems: List[Gem] = Field(default_factory=list)


class Gnome(Person):
    is_master: bool = False


def _id_for(login: str) -> int:
    return abs(hash(login)) % (1 << 31) - 1


def create_elf(name: str, login: str, password: str) -> Elf:
    elf = Elf(
        id=_id_for(login),
        name=name,
        login=login,
        password=SecretStr(str(hash(password))),
        status=PersonStatus.active,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    if first(lambda p: p.login == login) is not None:
        raise LoginConflict()

    _people.append(elf)
    return elf


def create_gnome(name: str, login: str, password: str) -> Gnome:
    gnome = Gnome(
        id=_id_for(login),
        name=name,
        login=login,
        password=SecretStr(str(hash(password))),
        status=PersonStatus.active,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_master=False
    )

    if first(lambda p: p.login == login) is not None:
        raise LoginConflict()

    _people.append(gnome)
    return gnome


def get() -> List[Person]:
    return _people


def first(predicate: Callable[[Person], bool]) -> Optional[Person]:
    return next((person for person in _people if predicate(person)), None)


def update_person(person: Person):
    old_person = first(lambda p: p.id == person.id)

    if not old_person:
        raise PersonNotFound()

    _people.remove(old_person)
    _people.append(person)
