# Algorithm: The Shooting Method

# Define: f(S, x)        # The coupled 1st-order ODEs, S = [y, y']
# Define: y_initial      # Boundary condition y(0)
# Define: y_target       # Boundary condition y(L)
# Define: x_min = 0, x_max = L

def get_error(guess_slope, f, y_initial, y_target, x_min, x_max, solve_ivp):
    # 1. Set initial state vector
    S_initial = [y_initial, guess_slope]
    
    # 2. Run the IVP solver
    S_final = solve_ivp(f, S_initial, x_min, x_max)
    
    # 3. Calculate the "miss distance"
    y_final = S_final[0]  # Get the y-component at x=L
    error = y_final - y_target
    return error

# 4. Use a root-finder (e.g., Secant) on the error function
# find_root will call get_error() repeatedly with new guesses
# correct_slope = find_root(get_error, initial_guess_1, initial_guess_2)
