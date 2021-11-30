import random
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List

from pydantic import BaseModel

_all_gems = []  # type: List[Gem]


class DistributionError(Exception):
    pass


class GemType(str, Enum):
    diamond = 'diamond'
    emerald = 'emerald'
    amethyst = 'amethyst'
    sapphire = 'sapphire'
    garnet = 'garnet'
    ruby = 'ruby'


class Gem(BaseModel):
    id: int
    gem_type: GemType
    owner_id: Optional[int]
    gatherer_id: int
    gathered_at: datetime


def add(person_id: int, gems: Dict[GemType, int]) -> List[Gem]:
    gems = [Gem(
        id=random.randint(0, (1 << 31) - 1),
        gatherer_id=person_id,
        gem_type=gem_type,
        gathered_at=datetime.now()
    ) for gem_type, amount in gems.items() for _ in range(amount)]
    _all_gems.extend(gems)
    return gems


def undistributed() -> List[Gem]:
    return [gem for gem in _all_gems if gem.owner_id is None]


def apply_distribution(distribution: Dict[int, int]):
    for gem in _all_gems:
        if distribution.get(gem.id) and gem.owner_id is not None:
            raise DistributionError(f"Gem {gem.id} is already assigned")

    for gem in _all_gems:
        owner_id = distribution.get(gem.id)
        if owner_id is not None:
            gem.owner_id = owner_id


def distributed_to(person_id: int):
    return [gem for gem in _all_gems if gem.owner_id == person_id]


def gathered_by(person_id: int) -> List[Gem]:
    return [gem for gem in _all_gems if gem.gatherer_id == person_id]


def collection() -> List[Gem]:
    return _all_gems.copy()

