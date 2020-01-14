# pylint: disable=missing-docstring,redefined-outer-name,protected-access
import pytest
import ray


def setup_module():
    ray.init()


def teardown_module():
    ray.shutdown()


@pytest.mark.slow
def test_trainer_step(trainer_cls, env_creator):
    trainer = trainer_cls(env=env_creator, config={"num_workers": 0})
    trainer.train()
