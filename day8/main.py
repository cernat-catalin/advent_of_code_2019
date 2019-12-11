import numpy as np


def compose_layers(layer_1, layer_2):
    h, w = layer_1.shape
    return np.array([y if x == 2 else x for (x, y) in zip(layer_1.flatten(), layer_2.flatten())]).reshape(h, w)

with open('day8/input') as f:
    height = 6
    width = 25

    digits = np.array([int(x) for x in f.readline().rstrip()], dtype=np.int64)
    n_layers = digits.shape[0] // (height * width)
    layers = np.reshape(digits, (n_layers, height, width))

    layer = np.argmin(np.sum(layers == 0, axis=(1, 2)))
    n_ones = np.sum(layers == 1, axis=(1, 2))[layer]
    n_twos = np.sum(layers == 2, axis=(1, 2))[layer]
    print(n_ones * n_twos) # part one

    image = layers[0]
    for i in range(1, n_layers):
        image = compose_layers(image, layers[i])

    msg ='\n'.join([''.join(str(x) for x in layer.flatten()) for layer in image]).replace('0', ' ')
    print(msg)