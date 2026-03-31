# **Chapter 1: End-to-End Reproducible First Experiment () () (Codebook)**

---

## Project Scope

This codebook implements Chapter 1 from setup verification to saved visualization and experiment record.

Project outputs (inside this chapter):

- Environment diagnostics in terminal output.
- Plot image: `codes/ch1_sin_plot.png`

---

## Step 1: Environment Verification Script

Run this first to ensure toolchain consistency.

```python
import sys
import numpy as np
import matplotlib
import scipy

print("=== Chapter 1 Environment Check ===")
print("Python:", sys.version.split()[0])
print("NumPy:", np.__version__)
print("Matplotlib:", matplotlib.__version__)
print("SciPy:", scipy.__version__)
```
**Sample Output:**
```
=== Chapter 1 Environment Check ===
Python: 3.13.9
NumPy: 2.2.6
Matplotlib: 3.10.6
SciPy: 1.16.3
```


Interpretation:

- If imports fail, resolve environment before continuing.
- Record versions in your experiment notes for reproducibility.

---

## Step 2: Core Experiment Script (Generate and Save Plot)

This script builds the first scientific figure and saves it to chapter assets.

```python
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Resolve output location relative to the chapter directory
codes_dir = Path("docs/chapters/chapter-1/codes")
codes_dir.mkdir(parents=True, exist_ok=True)

# 1. Generate data
x = np.linspace(0.0, 2.0 * np.pi, 400)
y = np.sin(x)

# 2. Plot with scientific labeling
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(x, y, color="tab:blue", linewidth=2.0, label="sin(x)")
ax.set_title("Chapter 1: First Reproducible Plot")
ax.set_xlabel("x (radians)")
ax.set_ylabel("Amplitude")
ax.grid(True, alpha=0.35)
ax.legend()

# 3. Save artifact for docs and reports
out_file = codes_dir / "ch1_sin_plot.png"
fig.savefig(out_file, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Saved figure to: {out_file}")
```
**Sample Output:**
```
Saved figure to: docs/chapters/chapter-1/codes/ch1_sin_plot.png
```

---

## Step 3: Experiment Metadata Summary

Create a concise run summary directly in console output.

```python
from pathlib import Path
from datetime import datetime
import numpy as np

x = np.linspace(0.0, 2.0 * np.pi, 400)
y = np.sin(x)

summary_text = "\n".join([
    "Chapter 1 Experiment Log",
    f"Timestamp (UTC): {datetime.utcnow().isoformat()}Z",
    "Experiment: Plot sin(x) on [0, 2pi]",
    f"Samples: {len(x)}",
    f"x_min: {x.min():.6f}",
    f"x_max: {x.max():.6f}",
    f"y_min: {y.min():.6f}",
    f"y_max: {y.max():.6f}",
    "Notes: Figure generated with NumPy + Matplotlib and saved to codes/ch1_sin_plot.png"
])

print(summary_text)
```
**Sample Output:**
```
Chapter 1 Experiment Log
Timestamp (UTC): 2026-03-20T05:19:25.198013Z
Experiment: Plot sin(x) on [0, 2pi]
Samples: 400
x_min: 0.000000
x_max: 6.283185
y_min: -0.999992
y_max: 0.999992
Notes: Figure generated with NumPy + Matplotlib and saved to codes/ch1_sin_plot.png
```

---

## Step 4: Documentation Asset Preview

Rendered artifact expected from Step 2:

![Chapter 1 sin plot](codes/ch1_sin_plot.png)

---

## Step 5: Reproducibility Checklist

1. All scripts run without manual edits.
2. Output files are created under this chapter only.
3. Plot has title, labels, legend, and grid.
4. Console summary captures enough metadata to reproduce later.

---

## Step 6: Git Snapshot

After generating outputs, track them in version history.

```bash
git add docs/chapters/chapter-1/codebook.md
git add docs/chapters/chapter-1/codes/ch1_sin_plot.png
git commit -m "Chapter 1: add reproducible end-to-end codebook workflow"
```

---

## Notes For Chapter Bridge

You now have a baseline reproducible workflow. In Chapter 2, the same workflow will be used to study floating-point representation error, precision limits, and numerical stability.