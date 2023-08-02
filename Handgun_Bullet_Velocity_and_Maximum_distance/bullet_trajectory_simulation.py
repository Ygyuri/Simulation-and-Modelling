import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
import math

# Constants
gravitational_acceleration = 9.81  # m/s²
air_density = 1.225  # kg/m³
horizontal_distance = 1546  # meters
launch_angles = [math.radians(45), math.radians(-45)]  # 45 degrees and -45 degrees in radians

# Handgun data (initial velocities in m/s)
handguns = [
    {"name": "Glock 17", "initial_velocity": 343, "mass": 0.00745},
    {"name": "Smith & Wesson M&P Shield", "initial_velocity": 300, "mass": 0.01166},
    {"name": "Colt 1911", "initial_velocity": 259, "mass": 0.0149},
    {"name": "SIG Sauer P226", "initial_velocity": 411, "mass": 0.00804},
    {"name": "Ruger LCP II", "initial_velocity": 290, "mass": 0.00583},
]

# Function to calculate air resistance (drag force)
def air_resistance_force(velocity, air_density):
    C_d = 0.4  # Approximate drag coefficient for a bullet
    A = 0.00007  # Approximate cross-sectional area of a typical bullet (in square meters)
    return -0.5 * C_d * A * air_density * velocity ** 2

# Function to define the ODEs for bullet motion with air resistance
def bullet_odes(t, state, mass):
    velocity_x, velocity_y, x, y = state
    velocity = np.sqrt(velocity_x ** 2 + velocity_y ** 2)
    drag_force = air_resistance_force(velocity, air_density)

    acceleration_x = -drag_force * velocity_x / (mass * velocity)
    acceleration_y = -drag_force * velocity_y / (mass * velocity) - gravitational_acceleration

    return [acceleration_x, acceleration_y, velocity_x, velocity_y]

# Function to simulate the bullet trajectory with air resistance using ODE solver
def simulate_trajectory(mass, muzzle_velocity, launch_angle):
    launch_velocity_x = muzzle_velocity * np.cos(launch_angle)
    launch_velocity_y = muzzle_velocity * np.sin(launch_angle)

    initial_state = [launch_velocity_x, launch_velocity_y, 0, 0]
    t_span = (0, 20)  # Time span for the simulation (extend to get more accurate trajectories)
    sol = solve_ivp(bullet_odes, t_span, initial_state, args=(mass,), method='RK45', t_eval=np.linspace(t_span[0], t_span[1], 1000))

    return sol.y[2], sol.y[3]

# Function to calculate maximum height and maximum horizontal distance
def calculate_max_height_distance(initial_velocity, launch_angle):
    time_of_flight = 2 * initial_velocity * np.sin(launch_angle) / gravitational_acceleration
    max_height = initial_velocity ** 2 * np.sin(launch_angle) ** 2 / (2 * gravitational_acceleration)
    max_distance = initial_velocity ** 2 * np.sin(2 * launch_angle) / gravitational_acceleration
    return max_height, max_distance

# Animation function for updating the plot with interactive elements
def animate_trajectory(i):
    ax.cla()
    ax.set_xlim(0, horizontal_distance)
    ax.set_ylim(0, horizontal_distance)
    ax.set_xlabel("Horizontal Distance (m)")
    ax.set_ylabel("Vertical Distance (m)")
    ax.set_title(f"{handguns[i]['name']} Bullet Trajectory")

    initial_velocity = handguns[i]['initial_velocity']
    launch_angle = np.deg2rad(angle_slider.val)
    x, y = simulate_trajectory(handguns[i]['mass'], initial_velocity, launch_angle)
    ax.plot(x, y, label="Trajectory")
    ax.legend()

    # Calculate and display maximum height and maximum horizontal distance
    max_height, max_distance = calculate_max_height_distance(initial_velocity, launch_angle)
    ax.text(0.05, 0.9, f"Max Height: {max_height:.2f} meters", transform=ax.transAxes)
    ax.text(0.05, 0.85, f"Max Distance: {max_distance:.2f} meters", transform=ax.transAxes)

# Create the animation with interactive elements
fig, ax = plt.subplots()
animation = FuncAnimation(fig, animate_trajectory, frames=len(handguns), interval=2000, repeat=False)

# Add slider for launch angle
angle_slider_ax = plt.axes([0.1, 0.01, 0.65, 0.03], facecolor='lightgoldenrodyellow')
angle_slider = Slider(angle_slider_ax, 'Launch Angle (degrees)', -90, 90, valinit=45)

# Update the plot when the slider is changed
angle_slider.on_changed(lambda val: animation.event_source.stop())

plt.show()

