# Illustrative pseudo-code for Extended Trapezoidal Rule

function trapezoidal_rule(y_values, h):
N = length(y_values) - 1
# Start with the endpoint contributions
integral = (y_values[0] + y_values[N]) / 2.0

# Add all the interior points
for i from 1 to N-1:
    integral = integral + y_values[i]

# Multiply by the slice width
integral = integral * h

return integral
