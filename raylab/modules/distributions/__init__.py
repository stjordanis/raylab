"""Distributions as PyTorch modules compatible with TorchScript."""
from .abstract import DistributionModule, Independent
from .uniform import Uniform

__all__ = ["DistributionModule", "Independent", "Uniform"]
