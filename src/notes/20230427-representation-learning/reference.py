import random

import matplotlib.pyplot as plt
import numpy as np
import torch
from sklearn.datasets import make_moons
from torch.nn import BCELoss, LazyLinear, ReLU, Sequential, Sigmoid
from torch.optim import Adam

# Seed semuanya untuk reproducibility
seed = 1
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)


x, y = make_moons(noise=0.05)

plt.scatter(*x[y == 0].T, label="class 1")
plt.scatter(*x[y == 1].T, label="class 2")
plt.xlabel("feature 1")
plt.ylabel("feature 2")
plt.title("Data original")
plt.legend()
plt.show()


x = torch.FloatTensor(x)
y = torch.FloatTensor(y.reshape(-1, 1))

# Transformasi data dari dimensi 2 ke dimensi 10 -> 5 -> 2.
# Dimensi 2 dipilih untuk mempermudah visualisasi saja.
encoder = Sequential(
    LazyLinear(10),
    ReLU(),
    LazyLinear(5),
    ReLU(),
    LazyLinear(2),
    ReLU(),
)

# Transformasi data ke dimensi 1 untuk binary classification
classifier = Sequential(LazyLinear(1), Sigmoid())

opt = Adam([*encoder.parameters(), *classifier.parameters()], lr=0.01)
loss_fn = BCELoss()

losses = []
for _ in range(300):
    opt.zero_grad()

    hidden = encoder(x)  # full-connected terakhir, sebelum klasifikasi
    y_pred = classifier(hidden)  # probability estimate

    loss = loss_fn(y_pred, y)
    loss.backward()

    opt.step()
    losses.append(loss.item())

hidden = hidden.detach().numpy()
x = x.detach().numpy()
y = y.detach().numpy().ravel()


plt.scatter(*hidden[y == 0].T, label="class 1")
plt.scatter(*hidden[y == 1].T, label="class 2")
plt.xlabel("feature 1")
plt.ylabel("feature 2")
plt.title(
    "Data setelah transformasi oleh model (ke dimensi 2),\nfully-connected layer sebelum classifier"
)
plt.legend()
plt.show()

plt.plot(losses)
plt.xlabel("iterasi")
plt.ylabel("nilai loss (binary cross-entropy)")
plt.show()
