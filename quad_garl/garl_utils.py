import numpy as np

import torch


class GARLUtils:
    def __init__(self, genetic_algorithm, reinforcement_learning):
        self._ga = genetic_algorithm
        self._rl = reinforcement_learning
        self._chromosome_size = self._rl.I_size * self._rl.H_1 + self._rl.H_1 * self._rl.H_2 + \
                                self._rl.H_2 * self._rl.H_3 + self._rl.H_3 * self._rl.H_4 + \
                                self._rl.H_4 * self._rl.O_size

    @property
    def chromosome_size(self) -> int:
        return self._chromosome_size

    @chromosome_size.setter
    def chromosome_size(self, value: int):
        self._chromosome_size = value

    def weights_to_chromosome(self):
        start_idx = 0
        end_idx = 0
        for idx, layer in enumerate(self.model):
            if isinstance(layer, torch.nn.Linear):
                num_weights_in_layer = layer.in_features * layer.out_features
                genes = self.get_layer_weight(layer_num=idx).flatten()
                end_idx += num_weights_in_layer
                np.put(a=self.chromosome, ind=np.arange(start=start_idx, stop=end_idx), v=genes)
                start_idx = end_idx

    def chromosome_to_weights(self):
        start_idx = 0
        end_idx = 0
        for idx, layer in enumerate(self.model):
            if isinstance(layer, torch.nn.Linear):
                num_weights_in_layer = layer.in_features * layer.out_features
                end_idx += num_weights_in_layer
                weights = np.reshape(a=self.chromosome[:, start_idx:end_idx],
                                     newshape=(layer.in_features, layer.out_features))
                self.set_layer_weight(layer_num=idx, layer_weights=weights)
                start_idx = end_idx
