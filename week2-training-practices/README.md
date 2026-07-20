# week2 : model training practice with pytorch

# goal : yes practice

- want to use other API dataset not pytorch's
- if can, comparing modules and performance

## plan
- CIFAR-10 (Learning Multiple Layers of Features from Tiny Images, Alex Krizhevsky, 2009.)


## progress
- just MLP -> batch 5, sample 50000, epoch 6, parameter 1,841,162
    => Test Result: 
    Accuracy: 28.5%, Avg loss: 2.012923 (sample 10000) 

- CNN -> batch 5, sample 50000, epoch 6, parameter 62,006
    => Test Result:
    Accuracy: 62.1%, Avg loss: 1.084221 (sample 10000)


## inspirations
- controlling part of DataLoader. adjusting DataLoader -> accuracy + latency?
- actual mechanism of CNN -> must read D2L (receptive field, same kernal for different area, etc.)
- with my experiment, MLP has much more parameter with other matched conditions.
- (1) MLP has less accuracy
    => this means we can save x 1/30 resources by
    telling & restricting spatial structure about image
- (2) CNN has much more learning time (with CPU)
    => gpt says, CPU can process matrix multiplication well (BLAS -> SIMD & multithreading??? ha..) and CNN (saving convolution & backwards with more operation (pooling and kernal window) converting)

## todo
- D2L -> further model understanding
- model evaluation -> accurate comparison and research about models (CNN & MLP)
- understanding about hardware & compilers