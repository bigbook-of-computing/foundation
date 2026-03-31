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
