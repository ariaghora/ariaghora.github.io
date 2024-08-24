import torch
from torch.nn import Sequential, Linear, ReLU

model = Sequential(
    Linear(3, 5),
    ReLU(),
    Linear(5, 2),
)

print(model)


print(model[0].weight.detach().numpy(), "\n")
print(model[0].bias.detach().numpy(), "\n")
print(model[2].weight.detach().numpy(), "\n")
print(model[2].bias.detach().numpy(), "\n")

import numpy as np
from io import BufferedWriter

def dump_ndarray(x: np.ndarray, f: BufferedWriter):
    x = np.ascontiguousarray(x, dtype=np.float32)
    # Secara berurutan, tuliskan  ndim, shape, data tensor
    np.array(x.ndim, dtype=np.int32).tofile(f)
    np.array(x.shape, dtype=np.int32).tofile(f)
    f.write(x.tobytes())

x = np.array(
    [[1, 2, 3], 
     [4, 5, 6],
     [1, 2, 3],
     [4, 5, 6],
     [1, 2, 3]]
)

with open("x.dat", "wb") as f:
    dump_ndarray(x, f)