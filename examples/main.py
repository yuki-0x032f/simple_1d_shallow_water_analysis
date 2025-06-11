import numpy as np
from swe import solver, utils

def main():

    conditions = utils.load_yaml("examples/conditions.yml") 
    utils.print_dict(conditions)

    ch_len = conditions["channel_length"]
    sim_t = conditions["simulation_time"]
    dx = conditions["dx"]
    dt = conditions["dt"]
    ib = conditions["bed_slope_numerator"] / conditions["bed_slope_denominator"]
    Q = conditions["discharge"]
    n = conditions["n_manning"]
    g = conditions["gravity"]
    d_lim = conditions["depth_limit"]
    h_down_ratio = conditions["h_down_ratio"]
    output_interval = conditions["output_interval"]

    ret = utils.initialize_computational_domain(ch_len, dx, sim_t, dt, output_interval)
    utils.print_tuple(ret)
    iend0, iend1, total_time_steps, x, t = ret

    ret = utils.initialize_calculation_inputs(Q, ib, n, g, iend0, x)
    utils.print_tuple(ret)
    h0, u0, z = ret

    ret = solver.initialize_hydraulic_variables(iend0, iend1, total_time_steps, output_interval)
    utils.print_tuple(ret)
    M_temp, M_h_point, wl_temp, h_u_point, wl_arr, M_arr, h_arr, u_arr = ret

    ret = solver.setup_initial_conditions(Q, h0, u0, z, M_temp, M_h_point, wl_temp, h_u_point, wl_arr, M_arr, h_arr, u_arr)
    utils.print_tuple(ret)
    M_temp, M_h_point, wl_temp, h_u_point, wl_arr, M_arr, h_arr, u_arr = ret

    time_index = 0
    for i in range(1, total_time_steps):
        print(f"time: {i}/{total_time_steps - 1}")

        # Equation of motion
        h_u_point = solver.calculate_h_u_point(wl_temp, z, iend0, iend1)

        M_temp = solver.pressure_term(M_temp, h_u_point, iend1, dt, dx, g, wl_temp)
        M_temp = solver.advection_term(M_temp, h_u_point, iend1, d_lim, dt, dx)
        M_temp = solver.friction_term(M_temp, h_u_point, iend1, d_lim, n, dt, dx, g)

        # Equation of continuity
        M_h_point = solver.calculate_M_h_point(M_temp, iend0, iend1)

        wl_temp = solver.update_water_level(wl_temp, M_h_point, iend0, dt, dx, h0 * h_down_ratio, z)

        M_temp, wl_temp = solver.update_boundary_condition(M_temp, wl_temp, Q, iend0, iend1, z, h0 * h_down_ratio)

        if i % output_interval == 0:
            wl_arr, M_arr, h_arr, u_arr = solver.update_array(M_temp, wl_temp, h_u_point, iend0, iend1, time_index, wl_arr, M_arr, h_arr, u_arr)
            time_index += 1

    utils.plot_result(x, t, z, h_arr, u_arr, total_time_steps, output_interval)

if __name__ == "__main__":
    main()