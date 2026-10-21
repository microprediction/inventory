# Errata and scope notes for *Trading Illiquid Goods*

The linked 2017--2022 presentation is a legacy working deck. Its source is not
tracked here, so this note records corrections without silently altering the
historical PDF. The current paper in `papers/skew_width_imbalance/` uses the
corrected identities and states the nonnegative-markup/interiority scope.

## Slides 24--25: convexity and quote signs

The deck defines

$$
K^\uparrow=\varepsilon+\frac{\nu(x+s)-\nu(x)}s,
\qquad
K^\downarrow=\varepsilon+\frac{\nu(x-s)-\nu(x)}s
$$

and bid and ask markups $m_{bid}=w+K^\uparrow$ and
$m_{ask}=w+K^\downarrow$. With its centered slope and convexity conventions,

$$
S=\frac{K^\uparrow-K^\downarrow}{2},
\qquad
C=\frac{K^\uparrow+K^\downarrow}{2}-\varepsilon.
$$

Thus slide 24's last sign must be **minus** $\varepsilon$, and slide 25's
quote identities must be

$$m_{bid}=w+\varepsilon+C+S,
\qquad m_{ask}=w+\varepsilon+C-S.$$

The printed slide swaps the signs of $S$.

## Slides 36 and 38: factor four

For the deck's constant-convexity ansatz
$\nu(x)=(C_0/s)x^2$, direct centered differencing gives

$$S_\delta^*(x)=2(C_0/s)x,$$

not $(C_0/(2s))x$. Equation (14) therefore uses
$\cosh(2hC_0x/s)$, not $\cosh(hC_0x/(2s))$.

## Slides 48--49: the accuracy curves cross the quote boundary

The plotted red and blue functions are

$$R_{red}(t)=e^{t^2/2}(1-t^2),
\qquad R_{blue}(t)=e^{-t^2/2}.$$

They arise by taking $Z\sim N(0,1)$, setting $Y=1+b+tZ$, and extending the
interior exponential payoff $Y e^{1-Y}$ to every real $Y$:

$$
R_\infty(t,b)=\mathbb E[Y e^{1-Y}]
=e^{-b+t^2/2}(1+b-t^2).
$$

The red curve sets $b=0$; maximizing this unbounded expression gives
$b=t^2$ and the blue curve. This calculation is internally correct, but it is
not the constrained model stated earlier in the deck. Competing markups have
nonnegative exponential support and the dealer's submitted markup is also
constrained to be nonnegative. The Gaussian extension assigns positive mass to
$Y<0$ and evaluates the exponential fill factor there as greater than one.

If $Y$ is the submitted normalized markup and the quote is clipped at zero, the
relative expected payoff is instead

$$
R_{clip}(t,b)=\mathbb E[Y e^{1-Y}\mathbf 1_{\{Y\ge0\}}]
=e^{-b+t^2/2}\left[
(1+b-t^2)\Phi(d)+t\phi(d)\right],
\qquad d=\frac{1+b-t^2}{t}.
$$

At the plotted endpoint $t=1$, this gives

$$R_{clip}(1,0)=0.6577446\ne R_{red}(1)=0,$$

and

$$R_{clip}(1,1)=0.6570640\ne R_{blue}(1)=0.6065307.$$

Moreover $b=t^2=1$ is no longer optimal: for example
$R_{clip}(1,0.48106)\approx0.6978566$. If the intended uncertainty perturbs a
latent strike rather than the submitted markup, the precise boundary formula
changes, but the unqualified Gaussian calculation still needs a capped fill
probability and an explicit statement of what is random. Thus the figure is a
useful small-error illustration (the tail correction is negligible at
$t=0.2$), not a global proof of the preceding "no diminishing returns" claim.

Run `python literature/verify_trading_illiquid_errata.py` for the arithmetic
checks and the slide-49 boundary values.
