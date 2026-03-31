# **Chapter 1: Building Your Computational Physics Lab (Workbook)**

---

## Workbook Purpose

This workbook is for active learning. By the end of this chapter you should be able to:

1. Explain why reproducibility matters in computational science.
2. Create and verify a Python environment for scientific computing.
3. Use Jupyter Notebook cells intentionally (code vs markdown).
4. Use Git to capture meaningful experiment checkpoints.
5. Complete a small project with clear deliverables.

---

## Part A: Quick Concept Check

!!! note "Quiz 1: Reproducibility"
    Why is reproducibility a core requirement in scientific computing?
    
    - A. It makes notebooks look professional.
    - B. It ensures others can verify and rebuild your result.
    - C. It removes all numerical error.
    - D. It replaces peer review.
    
!!! note "Quiz 2: Environment Management"
    What is the main reason to use isolated environments (e.g., conda envs)?
    
    - A. To increase CPU clock speed.
    - B. To avoid dependency conflicts across projects.
    - C. To reduce memory use to zero.
    - D. To avoid writing documentation.
    
!!! note "Quiz 3: Jupyter Cell Types"
    Which statement is correct?
    
    - A. Markdown cells execute Python code.
    - B. Code cells are only for comments.
    - C. Markdown cells document assumptions, interpretation, and conclusions.
    - D. Cell order never affects results.
    
!!! note "Quiz 4: NumPy Motivation"
    Why is NumPy central in scientific Python workflows?
    
    - A. It provides fast vectorized numerical operations on arrays.
    - B. It is only used for plotting.
    - C. It is a Git replacement.
    - D. It manages package installation.
    
!!! note "Quiz 5: Git Commit Quality"
    Which commit message is best practice?
    
    - A. "update"
    - B. "stuff"
    - C. "Chapter 1: add first sin(x) plot with labeled axes"
    - D. "works now maybe"
    
---

## Part B: Interview-Style Questions

Answer each in 4 to 8 sentences. Use technical vocabulary.

1. Why is "it works on my machine" considered a reproducibility failure?
2. Explain literate programming in your own words and why it fits computational physics.
3. Compare absolute and relative error at a high level. Why does this matter before advanced simulations?
4. In what situations should a notebook be converted into a script for repeatable execution?
5. What information should always appear in a scientific plot before sharing it?

---

## Part C: Guided Lab Tasks

### Lab 1: Environment Verification (15-20 min)

Goal: prove your machine is ready.

1. Create or activate your chapter environment.
2. Run the script below.
3. Save output in your notes.

```python
import sys
import numpy as np
import matplotlib
import scipy

print("Python:", sys.version.split()[0])
print("NumPy:", np.__version__)
print("Matplotlib:", matplotlib.__version__)
print("SciPy:", scipy.__version__)
```
**Sample Output:**
```python
Python: 3.13.9
NumPy: 2.2.6
Matplotlib: 3.10.6
SciPy: 1.16.3
```


Success criteria:

- Script runs without import errors.
- You can report all versions.

### Lab 2: Notebook Discipline (20-25 min)

Goal: separate computation from interpretation.

1. Create `chapter1_lab.ipynb`.
2. Add 4 cells in order:
   - Markdown: objective and hypothesis.
   - Code: imports.
   - Code: generate $x$ and $y=\sin(x)$.
   - Markdown: interpret shape, roots, and amplitude.
3. Re-run all cells from top and confirm deterministic output.

Use this core code:

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)

plt.figure(figsize=(8, 4))
plt.plot(x, y, linewidth=2)
plt.title("Chapter 1 Lab: sin(x)")
plt.xlabel("x (radians)")
plt.ylabel("sin(x)")
plt.grid(True)
plt.show()
```

### Lab 3: Git Snapshot Workflow (10-15 min)

Goal: create auditable history.

Run in terminal inside project root:

```python
git status
git add docs/chapters/chapter-1/workbook.md
git add docs/chapters/chapter-1/codebook.md
git commit -m "Chapter 1: complete workbook and codebook activities"
```

Reflection prompt:

- Why is a descriptive commit message useful during peer collaboration?

---

## Part D: Mini Project (Student Submission)

### Project Title

Reproducible First Experiment: Plot, Explain, and Record

### Objective

Build a complete mini scientific artifact using Chapter 1 tools.

### Required Deliverables

1. A notebook with code + markdown explanation.
2. A saved figure file in the chapter `codes` folder.
3. A short "experiment log" markdown section (5-8 lines).
4. A Git commit capturing the snapshot.

### Technical Requirements

- Plot $\sin(x)$ on $[0, 2\pi]$ with title, axes labels, and grid.
- Use NumPy arrays (no manual list of points).
- Include one brief interpretation paragraph in markdown.
- Save figure as `codes/ch1_student_plot.png`.

### Stretch Goals

1. Add $\cos(x)$ on same figure with legend.
2. Compute and print max absolute difference between sampled and analytical values for a selected point set.
3. Export plot at higher resolution (`dpi=160`).

### Evaluation Rubric (20 points)

- Technical correctness (8)
- Clarity of documentation (4)
- Plot quality and labeling (4)
- Reproducibility and Git hygiene (4)

---

## Part E: Answer Key (Self-check)

!!! success "Quiz Answers"
        1. B
        2. B
        3. C
        4. A
        5. C
    
---

## Exit Ticket

Before moving to Chapter 2, confirm:

- I can build a clean environment and verify packages.
- I can create a readable notebook mixing code and reasoning.
- I can produce a labeled scientific plot.
- I can track my work with meaningful Git commits.