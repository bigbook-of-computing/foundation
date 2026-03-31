# **Chapter 1: Digital Lab Notebook (Codebook)**

---

This Codebook provides the exact, reproducible Python implementation for the foundational lab setup. We focus on environment verification, literate programming standards, and data artifact generation.

---

## Project 1: Environment Diagnostics & Verification

| Feature | Description |
| :--- | :--- |
| **Goal** | Verify the integrity of the scientific Python stack (NumPy, SciPy, Matplotlib) and record versions for reproducibility. |
| **Model** | System-level diagnostic script. |
| **Core Concept** | Auditing the "Digital Lab" before conducting physical simulations. |

### Complete Python Code

```python
import sys
import numpy as np
import matplotlib
import scipy
import pandas as pd

def run_diagnostics():
    """Prints the versions of all core libraries in the current environment."""
    print("=== Foundation Lab: Environment Check ===")
    print(f"Python:     {sys.version.split()[0]}")
    print(f"NumPy:      {np.__version__}")
    print(f"SciPy:      {scipy.__version__}")
    print(f"Matplotlib: {matplotlib.__version__}")
    print(f"Pandas:     {pd.__version__}")
    print("=" * 40)

if __name__ == "__main__":
    run_diagnostics()
```

**Sample Output:**
```text
=== Foundation Lab: Environment Check ===
Python:     3.13.9
NumPy:      2.2.6
SciPy:      1.16.3
Matplotlib: 3.10.6
Pandas:     2.2.3
========================================
```

### Expected Outcome and Interpretation

The script should run without `ImportError`. If any library is missing, the environment must be rebuilt using the provided `environment.yml`. Recording these versions is the first step in any scientific publication to ensure that future researchers can recreate your numerical conditions exactly.

---

## Project 2: Reproducible Figure Generation

| Feature | Description |
| :--- | :--- |
| **Goal** | Generate a high-resolution scientific plot of $\sin(x)$ and $\cos(x)$ and save it as a permanent artifact. |
| **Mathematical Model** | $y_1 = \sin(x)$, $y_2 = \cos(x)$ for $x \in [0, 2\pi]$. |
| **Core Concept** | Standardizing plot aesthetics (labels, grids, legends) and file-system discipline. |

### Complete Python Code

```python
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def generate_lab_artifact():
    """Generates and saves a standardized scientific plot."""
    
    # 1. Setup paths
    output_dir = Path("codes")
    output_dir.mkdir(exist_ok=True)
    
    # 2. Generate data
    x = np.linspace(0, 2*np.pi, 500)
    y_sin = np.sin(x)
    y_cos = np.cos(x)
    
    # 3. Create High-Quality Plot
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    
    ax.plot(x, y_sin, label=r'$\sin(x)$', color='#1f77b4', linewidth=2)
    ax.plot(x, y_cos, label=r'$\cos(x)$', color='#d62728', linestyle='--', linewidth=2)
    
    # Aesthetics
    ax.set_title("Chapter 1: Initial Lab Verification", fontsize=14, fontweight='bold')
    ax.set_xlabel("Phase Angle $\theta$ (rad)", fontsize=12)
    ax.set_ylabel("Amplitude $A$", fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.axhline(0, color='black', linewidth=1)
    ax.legend(loc='upper right', frameon=True)
    
    # 4. Save and Close
    output_path = output_dir / "ch1_verification_plot.png"
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    
    print(f"Artifact successfully saved to: {output_path}")

if __name__ == "__main__":
    generate_lab_artifact()
```

**Sample Output:**
```text
Artifact successfully saved to: codes/ch1_verification_plot.png
```

### Expected Outcome and Interpretation

The script produces a `.png` file with professional LaTeX-style labels. The visualization reveals the $90^\circ$ $(\pi/2)$ phase shift between the two functions. This project validates that the **visualization pipeline** is functional and that you can export high-resolution assets for documentation or publication.

---

## **References**

[1] Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*.

[2] Harris, C. R., et al. (2020). Array programming with NumPy. *Nature*.

[3] Perez, F., & Granger, B. E. (2007). IPython: A system for interactive scientific computing. *Computing in Science & Engineering*.