# Illustrative pseudo-code for Euler's Method

function euler_solver(f, x0, t_start, t_end, h):
# f is the derivative function f(x, t)
# x0 is the initial condition
# h is the step size

x = x0
t = t_start

trajectory = [x0]

while t < t_end:
    # Calculate the derivative at the current point
    slope = f(x, t)
    
    # Take the "Euler step"
    x = x + h * slope
    t = t + h
    
    append(trajectory, x)
    
return trajectory
