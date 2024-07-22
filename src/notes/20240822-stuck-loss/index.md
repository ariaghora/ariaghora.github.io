# Diagnosing stuck loss in neural networks: cross-entropy and random guessing

I recently trained a custom neural net model and wondered why the loss was stuck at a certain value.
For more context, I trained the model to predict 5 classes, and the loss value where it got stuck was around $1.6$.
Upon inspecting the model thoroughly, I noticed that the model was only slightly better than (if not equal to) a random guess.

Apparently, we can diagnose this behavior early during training just by inspecting the loss value and the number of classes, provided that we use the standard cross-entropy loss function.
The cross-entropy loss for a single sample is defined as

\begin{equation}
L = -\sum_{i=1}^{K} y_i\log(p_i)
\end{equation}

where $y_i$ is the true distribution and one-hot encoded in most cases ($y_i=1$ for the correct class and $y_i=0$ for the other classes) and $p_i$ is the predicted probability for class $i$.
Suppose the **true** class is $j$. Since $y_i$ is 1 for the correct class $j$ (i.e., when $y_i=y_j$) and 0 for all other classes, then

\begin{equation}
\begin{aligned}
L &= -(0+\dots+0+y_j\cdot\log(p_j)+0+\dots+0) \\\\
  &= -y_j \cdot \log(p_j) \\\\
  &= -\log(p_j).
\end{aligned}
\end{equation}

Since the model is guessing randomly, then the probability for it to give correct predicted class (the $p_j$) over $K$ classes is $\frac 1 K$.
Now, substituting $p_j$ with $\frac 1 5$, we have the so-called $L_{rand}$ to denote loss for random guess.

\begin{equation}
\begin{aligned}
L_{rand} &= -\log\left(\frac 1 K\right)\\\\
  &= -(\log(1)-\log(K))\\\\
  &= \log(K).
\end{aligned}
\end{equation}

I use PyTorch. For some reason, in PyTorch, the cross-entropy is implemented based on the natural logarithm, so we can replace $\log(K)$ in the equations above with $\ln(K)$.
Quick checking using my calculator app, I got $\ln(5)=1.6094379124341$, which is consistent with the value I obtained before.
Yeah, it's a random-guess grade model.

**Key takeaway:** when training a neural net classifier, aim for loss values smaller than $\ln(K)$.
Ideally we want as close as possible to zero, but take $\ln(K)$ as your hard threshold.
Smaller than that, you're in the right direction.
Larger than that, there must be something wrong with your training setup.
