# On Markov's and Chebyshev's inequality

## Markov's inequality

Markov proposed that the probability of a random variable $X$ greater than a certain number $a$ is less than or equal to $\mu/a$ (or $\mathbb{E}[X] / a$).
Formally,

\begin{equation}
P(X \geq a) \leq \frac{\mathbb{E}[X]}{a}.
\end{equation}

The proof is straightforward.
Let's start with the definition of expectation,

\begin{equation}
\mathbb{E}[X] = \int_{-\infty}^{\infty} x f(x) dx
\end{equation}

where $f(x)$ is the probability density function of $X$.
We can split the integral into two parts, one for $x \leq a$ and one for $x \geq a$.

\begin{equation}
\begin{aligned}
\mathbb{E}[X] &= \int_{-\infty}^{a} x f(x) dx + \int_{a}^{\infty} x f(x) dx\\\\
&\geq \int_{a}^{\infty} x f(x) dx\\\\
&\geq a \int_{a}^{\infty} f(x) dx = a P(X \geq a)\\\\
\frac{\mathbb{E}[X]}{a} &\geq P(X \geq a). \blacksquare
\end{aligned}
\end{equation}

However, Markov's inequality can only give us an upper bound of the probability, and it is not tight when the distribution is heavy-tailed.

## Chebyshev's inequality

When we have information about the variance of the random variable, we can get a tighter bound using Chebyshev's inequality.
Chebyshev's inequality states that the probability of a random variable $X$ deviating from its mean by more than $k$ standard deviations is at most $1/k^2$.
Formally,
\begin{equation}
P(|X - \mu| \geq k \sigma) \leq \frac{1}{k^2}
\end{equation}

Chebyshev's inequality follows from Markov's inequality.
Let $Y = (X - \mu)^2$.
Then, $\mathbb{E}[Y] = \sigma^2$.
Also, let $a = (k \sigma)^2$.
Applying Markov's inequality to $Y$ gives us
\begin{equation}
\begin{aligned}
P(Y \geq a) &\leq \frac{\mathbb{E}[Y]}{a^2}\\\\
P((X-\mu)^2 \geq k^2 \sigma^2) &\leq \frac{\sigma^2}{k^2 \sigma^2}
\end{aligned}
\end{equation}

Note that if expression $(X-\mu)^2 \geq k^2\sigma$ holds, then $|X-\mu| \geq k\sigma$ must also hold.
Thus,
\begin{equation}
P(|X-\mu| \geq k\sigma) \leq \frac{\sigma^2}{k^2 \sigma^2} = \frac{1}{k^2}. \blacksquare
\end{equation}

Consider an example of determining the probability of a coin landing heads up after being flipped a certain number of times.
Using Markov inequality, we can say that if we flip the coin n times, the probability that the number of heads will be less than or equal to $n/2$ is at most $1/2$.
On the other hand, using Chebyshev inequality, we can say that for any number of coin flips, the probability that the difference between the number of heads and tails will be more than k times the standard deviation is at most 1/k^2.
This bound is much tighter and gives a more accurate probability estimate.