# MSDS 520: Math Fundamentals for Data Science

Course materials for **MSDS 520** at Meharry Medical College: the lecture-note PDFs and demo notebooks that accompany in-class teaching, plus a couple of slide decks. Lecturing in this course happens mostly on a whiteboard, the notebooks here are visual aids (animations, 3D plots, real-data demos, slider interactions) and typeset math you'd otherwise see derived live, not a replacement for the board. This repository is read-only for you, it is published from the instructor's working copy, so please don't open pull requests against it.

---

## Setting up your environment

This repository doesn't ship a pinned conda environment file. The notebooks use a standard scientific-Python stack: **numpy**, **pandas**, **matplotlib**, **scikit-learn** (a handful of Unit 2/3 notebooks, PCA, regression), and **Jupyter**. If you already have a working data-science Python environment, for example from Anaconda, you very likely already have everything you need; otherwise install those packages into whatever environment you use for this course.

### `msds520_helpers.py`

Shared helper functions used across the notebooks live in **`msds520_helpers.py`** at the root of this repository. Two things it provides:

- `helpers.show(v_or_M)` / `helpers.show_aug(A, b)`, pretty-print a vector or matrix as a typeset (LaTeX) array, the way it looks on the board, instead of raw NumPy text.
- `helpers.data(name)`, load one of the bundled datasets (see **Datasets** below).

The notebooks sit two folders below the root and reach it with:

```python
import sys
sys.path.append('../..')
import msds520_helpers as helpers
```

Keep that relative path working, if you move a notebook somewhere else, the import breaks.

---

## Layout

```
MSDS 520/
├── msds520_helpers.py
├── Datasets/                              # bundled data files (see below)
├── Unit 1 - Math Fundamentals/
│   ├── Lecture Notes/                     # typeset notes: logic, sets/functions, series, floating point
│   └── Notebooks/                         # 10 notebooks
├── Unit 2 - Linear Algebra/
│   ├── Lecture Notes/                     # typeset notes: systems, vectors, matrices, transformations, determinants, eigenvalues, PCA
│   ├── Slides/                            # 2 slide decks, Solving Systems, Vectors and Matrices
│   └── Notebooks/                         # 21 notebooks + 1 animation (.gif)
├── Unit 3 - Calculus/
│   ├── Lecture Notes/                     # typeset notes: approximation, derivatives, integrals, derivative/integral rules
│   ├── Slides/                            # 1 slide deck, Optimization
│   └── Notebooks/                         # 26 notebooks
└── Unit 4 - Prob Stat/
    ├── Lecture Notes/                     # typeset notes (this unit is intentionally the thinnest of the four)
    └── Notebooks/                         # 5 notebooks
```

All Lecture Notes and Slides content here is the compiled PDF only, the LaTeX source isn't included.

---

## Datasets

Unlike some other Meharry courses, the datasets these notebooks use are bundled directly in this repository, under `Datasets/`. `helpers.data(...)` finds them automatically, no setup, no separate download:

```
Datasets/
├── Real Estate/Real Estate Data.csv
├── MSDS 520 Calculus/
│   ├── mlr01.csv
│   └── slr02.csv
└── Hourly Energy Consumption/DAYTON_hourly.csv
```

---

## What is not in this repository

Distributed separately, on Blackboard:

- The syllabus
- Homework assignments, the midterm exam, and its study guide
- Chalkboard photos from lecture
- LaTeX (`.tex`) source for the lecture notes and slides, only the compiled PDFs are here

If something a notebook refers to isn't in this repository, check Blackboard before asking.
