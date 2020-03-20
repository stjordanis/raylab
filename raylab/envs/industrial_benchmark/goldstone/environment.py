"""
The MIT License (MIT)

Copyright 2017 Siemens AG

Author: Alexander Hentschel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from .dynamics import Dynamics


class GoldstoneEnvironment:
    # pylint:disable=missing-docstring

    def __init__(self, number_steps, max_required_step, safe_zone):
        self._dynamics = Dynamics(number_steps, max_required_step, safe_zone)

    @property
    def safe_zone(self):
        return self._dynamics.safe_zone

    def reward(self, phi_idx, effective_shift):
        return self._dynamics.reward(phi_idx, effective_shift)

    def state_transition(self, domain, phi_idx, system_response, effective_shift):
        domain, phi_idx, system_response = self._dynamics.state_transition(
            domain, phi_idx, system_response, effective_shift
        )
        return self.reward(phi_idx, effective_shift), domain, phi_idx, system_response
