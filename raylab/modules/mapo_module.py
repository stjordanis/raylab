"""MAPO Architecture with disjoint model, actor, and critic."""
from ray.rllib.utils import merge_dicts

from .model_actor_critic import AbstractModelActorCritic
from .stochastic_model_mixin import StochasticModelMixin
from .deterministic_actor_mixin import DeterministicActorMixin
from .action_value_mixin import ActionValueMixin


BASE_CONFIG = {
    "torch_script": False,
    "double_q": False,
    "exploration": None,
    "exploration_gaussian_sigma": 0.3,
    "smooth_target_policy": False,
    "target_gaussian_sigma": 0.3,
    "actor": {
        "units": (32, 32),
        "activation": "ReLU",
        "initializer_options": {"name": "xavier_uniform"},
        # === SQUASHING EXPLORATION PROBLEM ===
        # Maximum l1 norm of the policy's output vector before the squashing
        # function
        "beta": 1.2,
    },
    "critic": {
        "units": (32, 32),
        "activation": "ReLU",
        "initializer_options": {"name": "xavier_uniform"},
        "delay_action": True,
    },
    "model": {
        "units": (32, 32),
        "activation": "ReLU",
        "initializer_options": {"name": "xavier_uniform"},
        "delay_action": True,
        "input_dependent_scale": False,
        "residual": False,
    },
}


class MAPOModule(
    StochasticModelMixin,
    DeterministicActorMixin,
    ActionValueMixin,
    AbstractModelActorCritic,
):
    """Module architecture used in Model-Aware Policy Optimization."""

    # pylint:disable=abstract-method

    def __init__(self, obs_space, action_space, config):
        super().__init__(obs_space, action_space, merge_dicts(BASE_CONFIG, config))
