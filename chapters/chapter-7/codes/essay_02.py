def euler_method(f, y0, t0, t_end, h):
    t_values = [t0]
    y_values = [y0]
    
    t = t0
    y = y0
    
    while t < t_end:
        y += h * f(t, y)
        t += h
        t_values.append(t)
        y_values.append(y)
        
    return t_values, y_values
