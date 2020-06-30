"""Network and configurations for model-based SAC algorithms."""
from dataclasses import dataclass
from dataclasses import field

from gym.spaces import Box

from .networks.model.stochastic import build_ensemble
from .networks.model.stochastic import EnsembleSpec
from .sac import SAC
from .sac import SACSpec


@dataclass
class MBSACSpec(SACSpec):
    """Specifications for model-based SAC modules.

    Args:
        model: Specifications for stochastic dynamics model ensemble
        actor: Specifications for stochastic policy and entropy coefficient
        critic: Specifications for action-value estimators
        initializer: Optional dictionary with mandatory `type` key corresponding
            to the initializer function name in `torch.nn.init` and optional
            keyword arguments. Overrides model, actor, and critic initializer
            specifications.
    """

    model: EnsembleSpec = field(default_factory=EnsembleSpec)

    def __post_init__(self):
        super().__post_init__()
        if self.initializer:
            self.model.initializer = self.initializer


class MBSAC(SAC):
    """NN module for Model-Based Soft Actor-Critic algorithms.

    Args:
        obs_space: Observation space
        action_space: Action space
        spec: Specifications for model-based SAC modules

    Attributes:
        model (StochasticModelEnsemble): Stochastic dynamics model ensemble
        actor (StochasticPolicy): Stochastic policy to be learned
        alpha (Alpha): Entropy bonus coefficient
        critics (QValueEnsemble): The action-value estimators to be learned
        target_critics (QValueEnsemble): The action-value estimators used for
            bootstrapping in Q-Learning
        spec_cls: Expected class of `spec` init argument
    """

    # pylint:disable=abstract-method
    spec_cls = MBSACSpec

    def __init__(self, obs_space: Box, action_space: Box, spec: MBSACSpec):
        super().__init__(obs_space, action_space, spec)

        self.models = build_ensemble(obs_space, action_space, spec.model)
