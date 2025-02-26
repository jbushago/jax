# Copyright 2022 The JAX Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import scipy.stats as osp_stats
from jax import lax
from jax._src.numpy import lax_numpy as jnp
from jax._src.numpy.util import _wraps, _promote_args_inexact, _promote_args_numeric
from jax._src.scipy.special import gammaln, xlogy

@_wraps(osp_stats.multinomial.logpmf, update_doc=False)
def logpmf(x, n, p):
  """JAX implementation of scipy.stats.multinomial.logpmf."""
  p, = _promote_args_inexact("multinomial.logpmf", p)
  x, n = _promote_args_numeric("multinomial.logpmf", x, n)
  if not jnp.issubdtype(x.dtype, jnp.integer):
    raise ValueError(f"x and n must be of integer type; got x.dtype={x.dtype}, n.dtype={n.dtype}")
  x = x.astype(p.dtype)
  n = n.astype(p.dtype)
  logprobs = gammaln(n + 1) + jnp.sum(xlogy(x, p) - gammaln(x + 1), axis=-1)
  return jnp.where(jnp.equal(jnp.sum(x), n), logprobs, -jnp.inf)

@_wraps(osp_stats.multinomial.pmf, update_doc=False)
def pmf(x, n, p):
  """JAX implementation of scipy.stats.multinomial.pmf."""
  return lax.exp(logpmf(x, n, p))
