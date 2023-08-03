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
launch_angles = np.linspace(-np.pi, np.pi, 100)  # Simulate angles from -π to π

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
    velocity_x, velocity_y, velocity_z, x, y, z = state
    velocity = np.sqrt(velocity_x ** 2 + velocity_y ** 2 + velocity_z ** 2)
    drag_force = air_resistance_force(velocity, air_density)

    acceleration_x = -drag_force * velocity_x / (mass * velocity)
    acceleration_y = -drag_force * velocity_y / (mass * velocity)
    acceleration_z = -drag_force * velocity_z / (mass * velocity) - gravitational_acceleration

     # Special handling for vertical launch
    if velocity_x == 0 and velocity_y == 0 and velocity_z == 0:
        acceleration_z = 0  # Set vertical acceleration to 0 for vertical firing
    else:
        acceleration_z = -drag_force * velocity_z / (mass * velocity) - gravitational_acceleration

    return [acceleration_x, acceleration_y, acceleration_z, velocity_x, velocity_y, velocity_z]

# Function to simulate the bullet trajectory with air resistance using ODE solver
def simulate_trajectory(mass, muzzle_velocity, launch_angle):
    launch_velocity_x = muzzle_velocity * np.cos(launch_angle)
    launch_velocity_y = muzzle_velocity * np.sin(launch_angle)

    initial_state = [launch_velocity_x, launch_velocity_y, 0, 0, 0, 0]
    t_span = (0, 20)  # Time span for the simulation (extend to get more accurate trajectories)
    sol = solve_ivp(bullet_odes, t_span, initial_state, args=(mass,), method='RK45', t_eval=np.linspace(t_span[0], t_span[1], 1000))

    return sol.y[3], sol.y[4], sol.y[5]

# Function to check if an object is injured (reaches a specific height threshold and crosses it)
def is_injured(z_values, target_height):
     # Check if the bullet trajectory crosses the target_height
    for i in range(len(z_values) - 1):
        if (z_values[i] - target_height) * (z_values[i + 1] - target_height) <= 0:
            return True

    return False

# Function to calculate maximum height and maximum horizontal distance
def calculate_max_height_distance(initial_velocity, launch_angle):
    time_of_flight = (2 * initial_velocity * np.sin(launch_angle)) / gravitational_acceleration
    max_height = (initial_velocity ** 2) * (np.sin(launch_angle) ** 2) / (2 * gravitational_acceleration)
    max_distance = initial_velocity * np.cos(launch_angle) * time_of_flight
    return max_height, max_distance

# Animation function for updating the 3D plot with interactive elements
def animate_trajectory(i, launch_angle, target_height):
    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
    ax.set_xlim(0, horizontal_distance)
    ax.set_ylim(0, horizontal_distance)
    ax.set_zlim(0, 200)  # Setting a fixed height range for better visualization
    ax.set_xlabel("Horizontal Distance (m)")
    ax.set_ylabel("Horizontal Distance (m)")  # Fixing the label for y-axis
    ax.set_zlabel("Vertical Distance (m)")  # Fixing the label for z-axis
    ax.set_title(f"{handguns[i]['name']} Bullet Trajectory")

    initial_velocity = handguns[i]['initial_velocity']
    x, y, z = simulate_trajectory(handguns[i]['mass'], initial_velocity, launch_angle)

    # Check if the object is injured
    injured = is_injured(z, target_height)

    ax.plot(x, y, z, label="Trajectory", linestyle='-', marker='o', markersize=3)
    ax.scatter(horizontal_distance, horizontal_distance, target_height, color='red', marker='o', label="Target")

    if injured:
        # Use text2D to display text on the 2D canvas (screen)
        ax.text2D(0.5, 0.5, "INJURED!", color='red', fontsize=12, transform=ax.transAxes)

    ax.legend()

    # Calculate and display maximum height and maximum horizontal distance
    max_height, max_distance = calculate_max_height_distance(initial_velocity, launch_angle)
    if not np.isnan(max_height):
        ax.text2D(0.05, 0.9, f"Max Height: {max_height:.2f} meters", fontsize=12, transform=ax.transAxes)
    else:
        ax.text2D(0.05, 0.9, "Max Height: N/A", fontsize=12, transform=ax.transAxes)

    if not np.isnan(max_distance):
        ax.text2D(0.05, 0.85, f"Max Distance: {max_distance:.2f} meters", fontsize=12, transform=ax.transAxes)
    else:
        ax.text4D(0.05, 0.85, "Max Distance: N/A", fontsize=12, transform=ax.transAxes)

    ax.grid()

    # Save the figure as a PNG image
    fig.savefig(f"{handguns[i]['name']}_trajectory.png")

# Create the 3D animation with interactive elements
fig, axes = plt.subplots(1, len(handguns), figsize=(20, 5), subplot_kw={'projection': '3d'})

# Add sliders for launch angle and target height
angle_slider_ax = plt.axes([0.1, 0.01, 0.65, 0.03], facecolor='lightgoldenrodyellow')
angle_slider = Slider(angle_slider_ax, 'Launch Angle (degrees)', -180, 180, valinit=45)

height_slider_ax = plt.axes([0.1, 0.06, 0.65, 0.03], facecolor='lightgoldenrodyellow')
height_slider = Slider(height_slider_ax, 'Target Height (m)', 0, 200, valinit=50)

# Update the plot when the sliders are changed
def update(val):
    launch_angle = np.deg2rad(angle_slider.val)
    target_height = height_slider.val
    for i in range(len(handguns)):
        animate_trajectory(i, launch_angle, target_height)

angle_slider.on_changed(update)
height_slider.on_changed(update)

# Create the animation for each handgun and save the figures
for i in range(len(handguns)):
    animate_trajectory(i, math.radians(45), 50)

plt.show()

