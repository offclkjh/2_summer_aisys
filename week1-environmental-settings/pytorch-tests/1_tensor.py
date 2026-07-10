import torch
import numpy as np

# ## initializing

# # from data
# data = [[1, 2],[3, 4]]
# x_data = torch.tensor(data)

# # from a numpy array
# np_array = np.array(data)
# x_np = torch.from_numpy(np_array)

# # from another tensor
# x_ones = torch.ones_like(x_data) # retains the properties of x_data
# print(f"Ones Tensor: \n {x_ones} \n")

# x_rand = torch.rand_like(x_data, dtype=torch.float) # overrides the datatype of x_data
# print(f"Random Tensor: \n {x_rand} \n")

# # with random or constant values

# shape = (2,3) # dimension
# rand_tensor = torch.rand(shape)
# ones_tensor = torch.ones(shape)
# zeros_tensor = torch.zeros(shape)

# print(f"Random Tensor: \n {rand_tensor} \n")
# print(f"Ones Tensor: \n {ones_tensor} \n")
# print(f"Zeros Tensor: \n {zeros_tensor}")


# ## attributes

# tensor = torch.rand(3, 4) # argument: shape
# print(tensor.shape)
# print(tensor.dtype)
# print(tensor.device)


# ## operations

# every oprations -> https://docs.pytorch.org/docs/2.13/torch.html

# # We move our tensor to the current accelerator if available
# if torch.accelerator.is_available():
#     tensor = tensor.to(torch.accelerator.current_accelerator())

# # indexing & slicing
# tensor = torch.ones(4, 4)
# print(tensor[0], tensor[:, 0], tensor[..., -1]) #row0, col0, col3
# tensor[:,1] = 0
# print(tensor)

# # joining tensors
# t1 = torch.cat([tensor, tensor, tensor], dim=0)
# print(t1)
# print(t1.shape)
# # (4, 4) -> (12, 4)

# t2 = torch.stack([tensor, tensor, tensor], dim=0)
# print(t2)
# print(t2.shape)
# # (4, 4) -> (3, 4, 4)
# t3 = torch.stack([tensor, tensor, tensor], dim=2)
# print(t3)
# print(t3.shape)
# # (4, 4) -> (4, 4, 3)

# # arimetric
# # This computes the matrix multiplication between two tensors. y1, y2, y3 will have the same value
# # ``tensor.T`` returns the transpose of a tensor
# y1 = tensor @ tensor.T
# y2 = tensor.matmul(tensor.T)
# y3 = torch.rand_like(y1)
# torch.matmul(tensor, tensor.T, out=y3)
# print(y1,y2,y3)

# # This computes the element-wise product. z1, z2, z3 will have the same value
# z1 = tensor * tensor
# z2 = tensor.mul(tensor)
# z3 = torch.rand_like(tensor)
# torch.mul(tensor, tensor, out=z3)
# print(z1,z2,z3)

# # single-element tensors
# agg = tensor.sum()
# print(agg, type(agg)) # tensor
# agg_item = agg.item()
# print(agg_item, type(agg_item)) # float

# # in-place operations (denoted by _)
# # x.add_(), x.copy_(y), x.t_(), ...
# print(tensor)
# print(tensor.t_())


## bridge with numpy
t = torch.ones(5)
print(f"t: {t}")
n = t.numpy()
print(f"n: {n}")

t.add_(1)
print(f"t: {t}")
print(f"n: {n}")

n = np.ones(5)
t = torch.from_numpy(n)

np.add(n, 1, out=n)
print(f"t: {t}")
print(f"n: {n}")