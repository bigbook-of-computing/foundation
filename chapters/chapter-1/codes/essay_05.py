# Create a figure and a set of axes
fig, ax = plt.subplots()

# Plot the (x, y) data on the axes
ax.plot(x, y, label='f(x) = sin(x)')

# ALWAYS label your plots! This is non-negotiable.
ax.set_title("My First Physics Plot")
ax.set_xlabel("x (radians)")
ax.set_ylabel("f(x)")
ax.legend()
ax.grid(True) # Add a grid for readability

# Show the plot
plt.show()
