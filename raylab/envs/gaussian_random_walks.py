"""Wrapper for introducing irrelevant state variables."""
import numpy as np
import gym
from ray.rllib.utils.annotations import override


class GaussianRandomWalks(gym.Wrapper):
    """Add gaussian random walk variables to the observations.

    Arguments:
        env (gym.Env): a gym environment instance
        num_random_walks (int): the number of random walks to append to the observation.
    """

    def __init__(self, env, num_random_walks):
        super().__init__(env)
        self._num_random_walks = num_random_walks
        self._random_walk = None

        low = self.observation_space.low
        high = self.observation_space.high
        self.observation_space = gym.spaces.Box(
            low=np.concatenate([low, [-np.inf] * num_random_walks]),
            high=np.concatenate([high, [np.inf] * num_random_walks]),
            dtype=self.observation_space.dtype,
        )

        if hasattr(self.env, "reward_fn"):

            def reward_fn(state, action, next_state):
                return self.env.reward_fn(
                    state[..., :-num_random_walks],
                    action,
                    next_state[..., :-num_random_walks],
                )

            self.reward_fn = reward_fn

    @override(gym.Wrapper)
    def reset(self, **kwargs):
        observation = self.env.reset(**kwargs)
        self._random_walk = np.random.normal(size=self._num_random_walks)
        return np.concatenate([observation, self._random_walk])

    @override(gym.Wrapper)
    def step(self, action):
        observation, reward, done, info = self.env.step(action)
        self._random_walk += np.random.normal(size=self._num_random_walks)
        return np.concatenate([observation, self._random_walk]), reward, done, info
