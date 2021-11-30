from gemstones import *
from gemstones import _all_gems
import pytest


@pytest.fixture(autouse=True)
def clear_gem_state():
    _all_gems.clear()


def test_adding_one_gem():
    gems = add(1, {GemType.ruby: 1})
    assert(len(undistributed())) == 1
    assert(gems == undistributed())
    gem, *_ = undistributed()
    assert(gem.gem_type == GemType.ruby)
    assert(gem.gatherer_id == 1)


def test_adding_more_gems():
    add(1, {GemType.ruby: 1})
    add(2, {GemType.sapphire: 1})
    add(3, {GemType.amethyst: 2, GemType.diamond: 3})
    assert(len(undistributed())) == 7
    assert(len(gathered_by(1)) == 1)
    assert(len(gathered_by(3)) == 5)


def test_gem_distribution():
    add(1, {GemType.ruby: 1})
    gems = undistributed()
    gem, *_ = gems
    assert (len(gems) == 1)
    apply_distribution({gem.id: 2})
    assert(len(undistributed()) == 0)
    assert(distributed_to(2) == [gem])
    assert(len(collection()) == 1)
    with pytest.raises(DistributionError):
        apply_distribution({gem.id: 3})



