import pytest
import torch

from raylab.agents.sop import SOPTorchPolicy
from raylab.utils.debug import fake_batch


@pytest.fixture(params=(True, False))
def double_q(request):
    return request.param


@pytest.fixture
def config(double_q):
    options = {"module": {"critic": {"double_q": double_q}}, "policy_delay": 2}
    return {"policy": options}


@pytest.fixture
def policy(obs_space, action_space, config):
    return SOPTorchPolicy(obs_space, action_space, config)


def test_target_critics_init(policy):
    params = list(policy.module.critics.parameters())
    target_params = list(policy.module.target_critics.parameters())
    assert all(torch.allclose(p, q) for p, q in zip(params, target_params))


@pytest.fixture
def samples(obs_space, action_space):
    return fake_batch(obs_space, action_space, batch_size=256)


def test_delayed_policy_update(policy, samples):
    actor = policy.module.actor
    params = [p.clone() for p in actor.parameters()]
    _ = policy.learn_on_batch(samples)

    assert all(torch.allclose(new, old) for new, old in zip(actor.parameters(), params))

    _ = policy.learn_on_batch(samples)
    assert all(
        not torch.allclose(new, old) for new, old in zip(actor.parameters(), params)
    )
