# Chatterjee's "rank correlation" 

[Sourav Chatterjee](https://scholar.google.com/citations?user=F6QiwyMAAAAJ&hl=en) proposed a [new correlation coefficient](https://arxiv.org/abs/1909.10140).
Different from the classical correlation coefficient (e.g., Pearson's) that can only capture linear relationship, the Chatterjee's coefficient can indicate if $Y$ is related to any function of $X$, whether it is linear or nonlinear.
Suppose $Y_i = X_i^2$ for all $i$, then $Y_i$ is determined by $X_i$.
Pearson's coefficient will yield very low coefficient since there was **little to no linear correlation** found.
Meanwhile, Chatterjee's coefficient will still have high value because it knows that $Y_i$ depends on $X_i$ by some function (in this case, quadratic).

This coefficient value is between 0 and 1.
Meaning, the relationship is weak if the coefficient value gets closer to 0 and strong as it gets closer to 1.
It is 0 if and only if $X$ and $Y$ are independent, and is 1 if and only if $Y$ is a measurable function of $X$ *almost surely*.


given pairs of i.i.d. random variables $(X_i, Y_i)$ where $i=1, ..., n$.
Chatterjee's correlation is obtained through following procedure:

- Sort the pairs according to $X$ as $(X_{[i]}, Y_{[i]})$ such that $X_{[i]} \leq ... \leq X_{[n]}$
- Calculate $r_i$, which is the rank for $Y_{[i]}$, for $i=1, ..., n$.
  The rank is basically the count of $j$ such that $Y_{[j]} \leq Y_{[i]}$.
  Formally, $r_i$ itself is obtained by
  $$ r_i = \sum_{j=1}^n \mathbb{1}\left(Y_{[j]} \leq Y_{[i]}\right) $$
  where $\mathbb{1}\left(Y_{[j]} \leq Y_{[i]}\right)$ is an indicator function that evaluates to 1 if the expression in the parenthesis is true, and zero otherwise.
- And finally calculate the coefficient itself:

  $$ \xi_n(X, Y) = 1-\frac{3 \sum_{i=1}^{n-1} \lvert r_{i+1} - r_i \rvert}{n^2 - 1} $$

It can be implemented as a python function in few lines of code:

```python
import numpy as np

def chatterjee(x, y):
    # sort x and get the sorted index
    idx = np.argsort(x.ravel())

    # rearrange y based on idx
    y_ = y.ravel()[idx]

    # calculate a list of ranks
    r = (y_[:, None] <= y_).sum(1)

    # the coefficient calculation
    xi = 1 - (3 * np.sum(np.abs(r[1:] - r[:-1]))) / (len(y_) ** 2 - 1)

    return xi
```

I compared the classical linear correlation coefficient, i.e., Pearson's r-score ($r$), with Chatterjee's xi-score ($\xi$).
It is interesting to see  in a glimpse that xi-score can capture relationship between $X$ and $Y$, where the function of $X$ is not necessarily linear.
For example, the last example, i.e., quadratic function.

![](https://i.ibb.co/yXRk2m3/linear.png)
<p class="caption">Linear relationship</p>

![](https://i.ibb.co/wYB749d/random.png)
<p class="caption">Random scatter</p>

![](https://i.ibb.co/B3c4JD4/quadratic.png)
<p class="caption">Quadratic relationship</p>

Note that although in the first example $Y=X$, the xi-score is **less than** one!
This is one of the caveats of Chatterjee's xi-score.
Chatterjee himself put a remark:

> "(9) If there are no ties among the $Y_i$'s, the maximum possible value of $\xi_n(X, Y)$ is $(n -2) / (n + 1)$, which is attained if $Y_i = X_i$ for all $i$. This can be noticeably less than 1 for small $n$."