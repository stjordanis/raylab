import pytest
import torch

from raylab.policy.losses import ActionDPG
from raylab.policy.losses import DeterministicPolicyGradient
from raylab.policy.losses import ReparameterizedSoftPG


@pytest.fixture
def stochastic_actor(stochastic_policy):
    return stochastic_policy


@pytest.fixture
def critics(action_critics):
    return action_critics[0]


@pytest.fixture
def soft_pg_loss(stochastic_actor, critics):
    return ReparameterizedSoftPG(stochastic_actor, critics)


def test_soft_pg_loss(soft_pg_loss, stochastic_actor, critics, batch):
    loss, info = soft_pg_loss(batch)
    actor = stochastic_actor

    assert loss.shape == ()
    assert loss.dtype == torch.float32

    loss.backward()
    assert all(p.grad is not None for p in actor.parameters())
    assert all(p.grad is not None for p in critics.parameters())

    assert "loss(actor)" in info
    assert "entropy" in info


@pytest.fixture
def deterministic_actor(deterministic_policies):
    policy, _ = deterministic_policies
    return policy


@pytest.fixture
def action_dpg_loss(deterministic_actor, critics):
    return ActionDPG(deterministic_actor, critics)


def test_acme_dpg(action_dpg_loss, deterministic_actor, critics, batch):
    loss, info = action_dpg_loss(batch)
    actor = deterministic_actor

    assert torch.is_tensor(loss)
    assert loss.shape == ()

    loss.backward()
    assert all([p.grad is not None for p in actor.parameters()])
    assert all([p.grad is None for p in critics.parameters()])

    assert isinstance(info, dict)
    assert "loss(actor)" in info
    assert "dqda_norm" in info


def test_dpg_grad_equivalence(deterministic_actor, critics, batch):
    actor = deterministic_actor
    default_dpg = DeterministicPolicyGradient(actor, critics)
    acme_dpg = ActionDPG(actor, critics)

    loss_default, _ = default_dpg(batch)
    loss_acme, _ = acme_dpg(batch)

    default_grad = torch.autograd.grad(loss_default, actor.parameters())
    acme_grad = torch.autograd.grad(loss_acme, actor.parameters())

    zip_grads = list(zip(default_grad, acme_grad))
    assert all([torch.allclose(d, a) for d, a in zip_grads])
