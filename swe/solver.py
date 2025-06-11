import numpy as np

def initialize_hydraulic_variables(iend0: int, iend1: int, total_time_steps: int, output_interval: int) -> tuple:
    M_temp = np.zeros(iend1)
    M_h_point = np.zeros(iend0)

    wl_temp = np.zeros(iend0)
    h_u_point = np.zeros(iend1)

    wl_arr = np.zeros((total_time_steps // output_interval, iend0))
    M_arr  = np.zeros((total_time_steps // output_interval, iend0))
    h_arr  = np.zeros((total_time_steps // output_interval, iend0))
    u_arr  = np.zeros((total_time_steps // output_interval, iend0))

    return M_temp, M_h_point, wl_temp, h_u_point, wl_arr, M_arr, h_arr, u_arr

def setup_initial_conditions(
    Q: float,
    h0: float,
    u0: float,
    z: np.ndarray,
    M_temp: np.ndarray,
    M_h_point: np.ndarray,
    wl_temp: np.ndarray,
    h_u_point: np.ndarray,
    wl_arr: np.ndarray,
    M_arr: np.ndarray,
    h_arr: np.ndarray,
    u_arr: np.ndarray
) -> tuple:
    M_temp[:] = Q
    wl_temp[:-1] = z[:-1] + h0
    wl_temp[-1] = z[-1] + h0

    wl_arr[0, :] = wl_temp
    M_arr[0, :] = (M_temp[1:] + M_temp[:-1]) / 2
    h_arr[0, :] = wl_temp - z
    u_arr[0, :] = u0

    return M_temp, M_h_point, wl_temp, h_u_point, wl_arr, M_arr, h_arr, u_arr

def calculate_h_u_point(wl_temp: np.ndarray, z: np.ndarray, iend0: int, iend1: int) -> np.ndarray:
    h_u_point = np.zeros(iend1)
    for i in range(iend0 - 1):
        h_u_point[i+1] = (wl_temp[i+1] + wl_temp[i] - z[i+1] - z[i]) / 2
    h_u_point[0] = h_u_point[1]
    h_u_point[-1] = h_u_point[-2]

    return h_u_point

def calculate_M_h_point(M_temp: np.ndarray, iend0: int, iend1: int) -> np.ndarray:
    M_h_point = np.zeros(iend0)
    for i in range(iend0):
        M_h_point[i] = (M_temp[i+1] + M_temp[i]) / 2

    return M_h_point

def pressure_term(M_temp: np.ndarray, h_u_point: np.ndarray, iend1: int, dt: float, dx: float, g: float, wl_temp: np.ndarray) -> None:
    for i in range(1, iend1 - 1):
        M_temp[i] = M_temp[i] - dt/dx * g * h_u_point[i] * (wl_temp[i] - wl_temp[i-1])

    return M_temp

def advection_term(M_temp: np.ndarray, h_u_point: np.ndarray, iend1: int, d_lim: float, dt: float, dx: float) -> None:
    for i in range(1, iend1 - 1):
        if h_u_point[i] < d_lim:
            M_temp[i] = 0.0
        elif M_temp[i] < 0.0 and h_u_point[i+1] > d_lim:
            M_temp[i] = M_temp[i] - dt/dx * (np.power(M_temp[i+1], 2) / h_u_point[i+1] - np.power(M_temp[i], 2) / h_u_point[i])
        elif M_temp[i] > 0.0 and h_u_point[i-1] > d_lim:
            M_temp[i] = M_temp[i] - dt/dx * (np.power(M_temp[i], 2) / h_u_point[i] - np.power(M_temp[i-1], 2) / h_u_point[i-1])
        else:
            M_temp[i] = 0.0

    return M_temp

def friction_term(M_temp: np.ndarray, h_u_point: np.ndarray, iend1: int, d_lim: float, n: float, dt: float, dx: float, g: float) -> None:
    for i in range(1, iend1):
        if h_u_point[i] < d_lim:
            M_temp[i] = 0.0
        else:
            M_temp[i] = M_temp[i] - dt/dx * g * np.power(n, 2) * M_temp[i] * np.abs(M_temp[i]) / np.power(h_u_point[i], 7/3)

    return M_temp

def update_water_level(wl_temp: np.ndarray, M_h_point: np.ndarray, iend0: int, dt: float, dx: float, h_down: float, z: np.ndarray) -> None:
    for i in range(iend0 - 1):
        wl_temp[i] = wl_temp[i] - dt/dx * (M_h_point[i+1] - M_h_point[i])

    return wl_temp

def update_boundary_condition(M_temp: np.ndarray, wl_temp: np.ndarray, Q: float, iend0: int, iend1: int, z: np.ndarray, h_down: float) -> tuple:
    M_temp[0] = Q
    M_temp[-1] = M_temp[-2]

    wl_temp[-1] = z[-1] + h_down

    return M_temp, wl_temp

def update_array(M_temp: np.ndarray, wl_temp: np.ndarray, h_u_point: np.ndarray, iend0: int, iend1: int, time: int, wl_arr: np.ndarray, M_arr: np.ndarray, h_arr: np.ndarray, u_arr: np.ndarray) -> None:
    wl_arr[time, :] = wl_temp
    M_arr[time, :] = (M_temp[:-1] + M_temp[1:]) / 2
    h_arr[time, :] = (h_u_point[:-1] + h_u_point[1:]) / 2
    u_arr[time, :] = M_arr[time, :] / h_arr[time, :]

    return wl_arr, M_arr, h_arr, u_arr
