# Algorithm: Velocity-Verlet (Kick-Drift-Kick)

def velocity_verlet(x0, v0, h, F, m, N_steps):
    x = [x0]
    v = [v0]
    a = [F(x[0]) / m]
    
    for n in range(N_steps - 1):
        # 1. Half-Kick
        v_half = v[n] + 0.5 * h * a[n]
        
        # 2. Full-Drift
        x_next = x[n] + h * v_half
        x.append(x_next)
        
        # 3. New Acceleration
        a_next = F(x[n+1]) / m
        a.append(a_next)
        
        # 4. Half-Kick
        v_next = v_half + 0.5 * h * a[n+1]
        v.append(v_next)
    
    return x, v
