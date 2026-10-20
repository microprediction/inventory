# A one-parameter forecast curve need not have a finite-dimensional filter

The curve/state realisation question in `formulation.md` §6 is not the same
as closure of a posterior family. Here is an explicit statistical counterexample.
It isolates that distinction; it is not a complete commodity-pricing model.

## One hidden state and one forecast-curve parameter

Let $\Theta$ be uniform on $(0,1)$ and let the hidden state evolve as

$$X_k=2^{-k}\Theta,\qquad X_{k+1}=X_k/2.$$

At integer times observe

$$Z_k=g(X_k)+\epsilon_k,\qquad
g(x)=\frac{1}{1+x},\qquad
\epsilon_k\overset{\mathrm{iid}}\sim N(0,\sigma^2),\quad \sigma>0,$$

with the noises independent of $\Theta$. Write
$\mathcal Z_n=\sigma(Z_1,\ldots,Z_n)$ and
$m_n=\mathbb E[X_n\mid\mathcal Z_n]$. For every integer horizon $h\ge0$,

$$\mathbb E[X_{n+h}\mid\mathcal Z_n]=2^{-h}m_n.$$

Thus every conditional-mean forecast curve lies **exactly** in the same
one-parameter family. Adding a known positive equilibrium coverage $Y^e$ gives
the equally simple family $Y^e+2^{-h}m_n$. The hidden dynamics themselves are
one-dimensional and Markov. Neither statement establishes a closed recursion
for $m_n$ from the forecast-curve parameter alone.

## Posterior dimension grows with the observation history

Set $f_k(\theta)=(1+2^{-k}\theta)^{-1}$. For observations
$z=(z_1,\ldots,z_n)$, Bayes' rule gives a positive posterior density of
$\Theta$ on $(0,1)$:

$$p_n(\theta;z)=\frac{1}{C_n(z)}
\exp\!\left\{\frac{1}{\sigma^2}\sum_{k=1}^n z_k f_k(\theta)
-\frac{1}{2\sigma^2}\sum_{k=1}^n f_k(\theta)^2\right\}.$$

Its log-density derivatives in the observation directions are

$$\partial_{z_k}\log p_n(\theta;z)
=\frac{f_k(\theta)-\mathbb E_{p_n}[f_k]}{\sigma^2}.$$

These $n$ centered functions are linearly independent. Indeed, if
$\sum_k a_k f_k$ is constant on $(0,1)$, it is a constant rational function.
Its distinct simple poles at $-2^k$ have residues $2^k a_k$, so every $a_k$
must vanish. Centering does not change independence modulo constants.
Because $p_n$ is positive, the density derivatives $\partial_{z_k}p_n$ are
also independent. The observation-to-posterior map therefore has rank $n$.

Consequently no fixed-dimensional **regular smooth posterior family** can
contain all these posteriors for all times: its dimension would have to be
at least $n$ for every $n$. This is the usual smooth-family meaning of an
exact finite-dimensional filter, not a claim about pathological encodings
of an entire history into a real number. Passing from $\Theta$ to $X_n$ is
an invertible known rescaling at each fixed $n$, so it does not change the rank.

This gives an unbounded-dimension posterior family despite the exactly
one-parameter forecast curves above. It also shows why the observation law
and prior cannot be omitted from a posterior-closure question.

## Equal current forecasts can still give different updates

For a short illustration, compare two current beliefs about $X$:

- $A$: a point mass at $1/2$;
- $B$: equal masses at $0$ and $1$.

Both have mean $1/2$ and hence identical mean-forecast curves under the decay
dynamics. Observe $Z=1$ with the same sensor $g$ and noise standard deviation
$\sigma=0.2$. Belief $A$ retains mean $1/2$, whereas belief $B$ updates to

$$\mathbb E_B[X\mid Z=1]
=\frac{e^{-25/8}}{1+e^{-25/8}}\approx0.0420877.$$

The forecast mean is not a sufficient statistic for this update. This
two-belief illustration alone would not rule out a larger finite-dimensional
filter; the rank argument above supplies the unbounded-dimension result for
one fixed continuous prior and observation model.

## Reproducible checks

Run `python notes/verify_filter_realization.py` (standard library only).
It checks the two-belief update and uses rational Gaussian elimination to
verify independence modulo constants at distinct rational test points for
history lengths 1 through 8. Those finite checks are regressions, not a
substitute for the pole argument proving independence for arbitrary $n$.
