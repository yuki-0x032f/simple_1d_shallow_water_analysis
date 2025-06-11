import numpy as np
import matplotlib.pyplot as plt
import os
import yaml

def load_yaml(file_path: str) -> dict:
    with open(file_path, "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def print_dict(dict: dict) -> None:
    print("--------------------------------")
    for key, value in dict.items():
        print(f"{key}: {value} ({type(value).__name__})")

def print_tuple(tuple: tuple) -> None:
    print("--------------------------------")
    for i, value in enumerate(tuple):
        print(f"index {i}: {value} ({type(value).__name__})")

def initialize_computational_domain(channel_length: float, dx: float, simulation_time: float, dt: float, output_interval: int) -> tuple:
    iend0 = int(channel_length / dx)
    iend1 = iend0 + 1
    total_time_steps = int(simulation_time / dt) + 1

    x = np.linspace(0.0 + dx / 2, channel_length - dx / 2, iend0)
    t = np.linspace(0.0, simulation_time, total_time_steps // output_interval)

    return iend0, iend1, total_time_steps, x, t

def initialize_calculation_inputs(Q: float, ib: float, n: float, g: float, iend0: int, x: np.ndarray) -> tuple:
    h0 = np.power(Q * n / np.power(ib, 1/2), 3/5)
    u0 = 1 / n * np.power(h0, 2/3) * np.sqrt(ib)

    z = - ib * x
    z -= z.min()

    return h0, u0, z

def plot_result(x: np.ndarray, t: np.ndarray, z: np.ndarray, h_arr: np.ndarray, u_arr: np.ndarray, total_time_steps: int, output_interval: int) -> None:
    os.makedirs("./examples/result", exist_ok=True)

    for i in range(total_time_steps // output_interval):

        plt.plot(x, z + h_arr[i, :], label="water level")
        plt.plot(x, z, label="bed level")
        plt.legend()
        plt.savefig(f"./examples/result/{i:04d}.png")
        plt.close()