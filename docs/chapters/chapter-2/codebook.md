# **Chapter 2: Precision, Error, and Numerical Judgment (Codebook)**

---

This Codebook implements the core diagnostic tools for assessing numerical reliability. We move from measuring hardware constants like **Machine Epsilon** to observing the catastrophic failure of algorithms through **Cancellation** and **Instability**.

---

## Project 1: Measuring the "Grid of Numbers"

| Feature | Description |
| :--- | :--- |
| **Goal** | Quantify the absolute and relative spacing between floating-point numbers across 16 orders of magnitude. |
| **Model** | Spacing analysis using `np.nextafter`. |
| **Core Concept** | Understanding that the "density" of representable numbers decreases as magnitude increases. |

### Complete Python Code

```python
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def audit_float_spacing():
    """Plots the absolute and relative gap between adjacent float64 numbers."""
    
    # 1. Generate magnitudes from 10^0 to 10^16
    x = np.logspace(0, 16, 100)
    
    # 2. Find the "next" representable number
    next_x = np.nextafter(x, np.inf)
    
    # 3. Calculate gaps
    abs_gap = next_x - x
    rel_gap = abs_gap / x
    
    # 4. Visualize
    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=150)
    
    color1 = 'tab:blue'
    ax1.set_xlabel('Magnitude of $x$ (log scale)')
    ax1.set_ylabel('Absolute Gap $\Delta x$', color=color1)
    ax1.loglog(x, abs_gap, color=color1, linewidth=2, label='Absolute Gap')
    ax1.tick_params(axis='y', labelcolor=color1)
    
    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel('Relative Gap $\Delta x / x$', color=color2)
    ax2.loglog(x, rel_gap, color=color2, linestyle='--', label='Relative Gap')
    ax2.tick_params(axis='y', labelcolor=color2)
    
    plt.title("The 'Staircase of Error': Growth of Representation Gaps")
    ax1.grid(True, which="both", ls="-", alpha=0.2)
    plt.tight_layout()
    
    # Save artifact
    output_path = Path("codes/ch2_gap_scaling.png")
    output_path.parent.mkdir(exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    
    print(f"Machine Epsilon (measured at 1.0): {abs_gap[0]:.2e}")

if __name__ == "__main__":
    audit_float_spacing()
```

### Expected Outcome and Interpretation

The output shows that while the **Relative Gap** remains constant near $10^{-16}$ (Machine Epsilon), the **Absolute Gap** grows linearly. At $x=10^{16}$, the distance between representable numbers is approximately $2.0$. This means that in this regime, the computer cannot distinguish between $10^{16}$ and $10^{16} + 1$. This "graininess" is the fundamental limit of all digital physics.

---

## Project 2: Stress-Testing Loss of Significance

| Feature | Description |
| :--- | :--- |
| **Goal** | Observe the exponential collapse of precision when subtracting nearly identical large numbers. |
| **Mathematical Model** | $f(x, \Delta) = (x + \Delta) - x$ for large $x$ and small $\Delta$. |
| **Core Concept** | **Catastrophic Cancellation**: the leading bits cancel, leaving only trailing noise. |

### Complete Python Code

```python
import numpy as np
import matplotlib.pyplot as plt

def test_cancellation():
    """Measures relative error for (x + delta) - x as delta shrinks."""
    
    x = 1.0e8  # Large base
    deltas = np.logspace(-2, -14, 100)
    
    # Theoretical result should be exactly 'delta'
    computed = (x + deltas) - x
    rel_error = np.abs(computed - deltas) / deltas
    
    plt.figure(figsize=(10, 5))
    plt.loglog(deltas, rel_error, 'o-', color='darkred', markersize=3)
    plt.axhline(1.0, color='black', linestyle='--')
    plt.title("Relative Error vs. Perturbation Size (x=10^8)")
    plt.xlabel("True $\Delta$")
    plt.ylabel("Relative Error")
    plt.grid(True, which="both", alpha=0.3)
    
    plt.savefig("codes/ch2_cancellation_error.png")
    plt.close()

if __name__ == "__main__":
    test_cancellation()
```

### Expected Outcome and Interpretation

The resulting plot shows a "V-shape" error profile. As $\Delta$ becomes smaller than $10^{-8}$ (the precision limit relative to $x=10^8$), the relative error hits **100%**. At this point, the calculation returns $0.0$ or a random bit pattern, effectively "losing" the entire physical signal. This highlights why subtraction is the most dangerous operation in numerical analysis.

---

## **References**

[1] Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*. SIAM.

[2] Goldberg, D. (1991). What every computer scientist should know about floating-point arithmetic. *ACM Computing Surveys*.

[3] Knuth, D. E. (1997). *The Art of Computer Programming, Volume 2: Seminumerical Algorithms*. Addison-Wesley.