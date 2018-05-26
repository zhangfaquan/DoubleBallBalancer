"""Simple test script for 3D Double Ball Balancer
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time
import copy

from dynamic_model_3d import ModelParam, DynamicModel, ModelState

print_sim_time = False
plot_visualization = True
plot_states = True

# create parameter struct
param = ModelParam()
param.l = 1
param.m1 = 1
param.m2 = 1
param.m3 = 1
param.r1 = 3
param.r2 = 2
param.tau = 0.100
param.theta1 = 1
param.theta2 = 1
param.theta3 = 1

# initial state
x0 = ModelState()
x0.psi_y = 0.25
# x0.psi_z = 0.3
# x0.omega_2 = np.array([0,0,0.75])
x0.psi_y_dot = -0.3

# instantiate model
model = DynamicModel(param, x0)

# simulation time step
dt = 0.05

# prepare simulation
max_sim_time = 15
sim_time = 0
sim_time_vec = [sim_time]
state_vec = [copy.copy(model.state)]
start_time = time.time()

if plot_visualization:
    fig = plt.figure(0)
    ax = fig.add_subplot(111, projection='3d')

# simulate until system is irrecoverable or max_sim_time reached
while not model.is_irrecoverable() and sim_time < max_sim_time:
    if plot_visualization:
        # get visualization
        vis = model.get_visualization()

        # plot
        plt.cla()

        ax.plot_wireframe(*vis['lower_ball'], color='b')
        ax.plot_wireframe(*vis['upper_ball'], color='r')

        plt.xlabel('x [m]')
        plt.ylabel('y [m]')
        ball_pos = model.state.pos
        range = param.r1 + param.r2
        ax.set_xlim3d(ball_pos[0] - range, ball_pos[0] + range)
        ax.set_ylim3d(ball_pos[1] - range, ball_pos[1] + range)
        ax.set_zlim3d(0, 2 * range)
        plt.show(block=False)
        time_passed = time.time() - start_time
        plt.pause(max(dt - time_passed, 0.001))

        start_time = time.time()

    # simulate one time step
    model.simulate_step(dt)
    sim_time += dt

    # save states as matrix, sim_time and inputs as lists
    state_vec.append(copy.copy(model.state))
    sim_time_vec.append(sim_time)

    if print_sim_time:
        print('sim_time: {0:.3f} s'.format(sim_time))

if plot_states:
    plt.figure()
    plt.plot(sim_time_vec, [state.psi_y for state in state_vec], label='psi_y')
    plt.plot(sim_time_vec, [state.psi_z for state in state_vec], label='psi_z')
    plt.xlabel('time [s]')
    plt.ylabel('angles [rad]')
    plt.legend()
    plt.title('angles')

    plt.figure()
    plt.plot(sim_time_vec, [state.psi_y_dot for state in state_vec], label='psi_y_dot')
    plt.plot(sim_time_vec, [state.psi_z_dot for state in state_vec], label='psi_z_dot')
    plt.xlabel('time [s]')
    plt.ylabel('omega [rad]')
    plt.legend()
    plt.title('omega')
    plt.show(block=True)