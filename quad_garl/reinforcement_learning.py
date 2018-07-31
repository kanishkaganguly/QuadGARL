import math

import numpy as np
import torch


class ReinforcementLearning:
    def __init__(self, log):
        # Logging
        self.log = log

        self.batch_size = 1
        self.I_size = 6  # type: int
        self.H_1 = 10  # type: int
        self.H_2 = 20  # type: int
        self.H_3 = 50  # type: int
        self.H_4 = 20  # type: int
        self.O_size = 4  # type: int
        self.input_tensor = torch.randn(self.batch_size, self.I_size, dtype=torch.float,
                                        requires_grad=False)  # type: torch.Tensor
        self.output_tensor = torch.randn(self.batch_size, self.O_size, dtype=torch.float,
                                         requires_grad=False)  # type: torch.Tensor
        self.model = torch.nn.Sequential(
            torch.nn.Linear(self.I_size, self.H_1),
            torch.nn.LogSigmoid(),
            torch.nn.Linear(self.H_1, self.H_2),
            torch.nn.ReLU(),
            torch.nn.Linear(self.H_2, self.H_3),
            torch.nn.LogSigmoid(),
            torch.nn.Linear(self.H_3, self.H_4),
            torch.nn.ReLU(),
            torch.nn.Linear(self.H_4, self.O_size)
        )  # type: torch.nn.Sequential
        self.chromosome_size = self.I_size * self.H_1 + self.H_1 * self.H_2 + self.H_2 * self.H_3 + \
                               self.H_3 * self.H_4 + self.H_4 * self.O_size
        self.chromosome = np.zeros((1, self.chromosome_size), dtype=np.float32)
        self.reward = 0.0  # type:float

    @property
    def chromosome_prop(self) -> np.array:
        return self.chromosome

    @chromosome_prop.setter
    def chromosome_prop(self, value: np.array):
        self.chromosome = value

    @property
    def reward_prop(self) -> float:
        return self.reward

    def update_reward(self, curr_state, target_state):
        deviation_x = np.linalg.norm(curr_state[0] - target_state[0])
        deviation_y = np.linalg.norm(curr_state[1] - target_state[1])
        deviation_z = np.linalg.norm(curr_state[2] - target_state[2])
        deviation_yaw = np.linalg.norm(curr_state[5] - target_state[5])

        sigma_x = 0.1
        sigma_y = 0.1
        sigma_z = 0.01
        sigma_yaw = 0.1
        reward_x = math.exp(-deviation_x ** 2 / (2 * sigma_x))
        reward_y = math.exp(-deviation_y ** 2 / (2 * sigma_y))
        reward_z = math.exp(-deviation_z ** 2 / (2 * sigma_z))
        reward_yaw = math.exp(-deviation_yaw ** 2 / (2 * sigma_yaw))

        self.reward = self.sigmoid(reward_x + reward_y + reward_z + reward_yaw)

    def sigmoid(self, val) -> float:
        return math.exp(val) / (math.exp(val) + 1)

    def update_tensor_data(self, _tensor: torch.Tensor, _data: np.array):
        _tensor.data = torch.from_numpy(_data.astype(np.float32)).data

    def get_layer_weight(self, layer_num: int) -> np.array:
        return self.model[layer_num].weight.data.numpy()

    def set_layer_weight(self, layer_num: int, layer_weights: np.array) -> np.array:
        self.model[layer_num].weight.data = torch.from_numpy(layer_weights)

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

# if __name__ == '__main__':
#     rl = ReinforcementLearning()
#     rl.update_tensor_data(_tensor=rl.input_tensor, _data=np.array([3, 6, 1, 2, 5, 4]))
#     rl.update_tensor_data(_tensor=rl.output_tensor, _data=np.array([2, 15, 10, 1]))
#     y_pred = rl.model(rl.input_tensor)
#     loss = rl.loss_fn(y_pred, rl.output_tensor)
