"""Shared display helpers for MSDS 520 notebooks.

Pretty-prints vectors and matrices as typeset (LaTeX) arrays so results render the
way they would on the whiteboard, instead of as raw NumPy text. Import it from a
notebook in this folder with:

    import msds520_helpers as helpers

then use helpers.show(...) for a vector/matrix and helpers.show_aug(A, b) for an
augmented matrix.

Both take two optional annotations:

    name='A'   ->  A = [matrix]        (the matrix *is* that thing)
    label=...  ->  label: [matrix]     (a caption, e.g. the row operation just done)

Use label for row operations -- name= would render "R2 -> R2 - 2R1 = [matrix]",
which reads as if the matrix equals the row operation.

It also resolves dataset paths. All three Meharry courses read their data from one
shared library outside this repo, so notebooks should never hard-code that path:

    df = pd.read_csv(helpers.data('Real Estate/Real Estate Data.csv'))
"""
import os
import re
from pathlib import Path

import numpy as np
from IPython.display import display, Math


# ---------------------------------------------------------------------------
# dataset paths
# ---------------------------------------------------------------------------
# The shared dataset library sits outside the course repo and is used by MSDS 520,
# MSDS 565, and MSCS 540 alike. Keeping the path here means notebooks never hard-code
# it, and moving the library later is a one-line change instead of a repo-wide sweep.
#
# A third resolution step, checked before the hardcoded fallback: a "Datasets/" folder
# sitting next to this file. That never exists in this dev repo (and per this course's
# CLAUDE.md, never should -- a prior manual copy went stale). It DOES exist in the live
# student repo, where sync_to_live.py populates it from the library on every run, so
# this same file works unmodified in both places: here it falls through to the
# hardcoded path below; there it resolves to the bundled copy automatically.
_LOCAL_DATASETS = Path(__file__).resolve().parent / "Datasets"
DATA_DIR = os.environ.get(
    "MEHARRY_DATASETS",
    str(_LOCAL_DATASETS) if _LOCAL_DATASETS.is_dir()
    else r"C:/Users/Graham West/Python Notebooks/Meharry Teaching/Datasets",
)


def data(name):
    """Full path to a file in the shared dataset library.

    `name` is the path relative to the library root, e.g.
    'Real Estate/Real Estate Data.csv'. Raises with a readable message if the file
    isn't there, rather than letting pandas emit a bare FileNotFoundError.
    """
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        raise FileNotFoundError(
            "Could not find '%s' in the shared dataset library.\n"
            "Looked in: %s\n"
            "If the library lives elsewhere on this machine, set the MEHARRY_DATASETS "
            "environment variable or edit DATA_DIR in msds520_helpers.py." % (name, DATA_DIR)
        )
    return path


def _format(x):
    """Format one number: integers stay integers, others get 3 significant digits."""
    x = float(x)
    if x == int(x):
        return str(int(x))
    return "{:.3g}".format(x)


def _matrix_latex(a):
    rows = [" & ".join(_format(x) for x in row) for row in a]
    return r"\begin{bmatrix}" + r" \\ ".join(rows) + r"\end{bmatrix}"


_SUP_SUB = re.compile(r"[\^_](\{[^{}]*\}|.)")


def _is_math_token(token):
    """True for things like A, A^T, 2A, R_2, +, \\to, a\\mathbf{v} -- false for words.

    Anything containing a backslash is LaTeX the caller wrote deliberately, so it is
    left in math mode. Otherwise strip sub/superscripts: a token carrying at most one
    letter is a symbol; anything wordier is prose that belongs in \\text{}.
    """
    if "\\" in token:
        return True
    return sum(c.isalpha() for c in _SUP_SUB.sub("", token)) <= 1


def _annotation_latex(text):
    """Typeset an annotation: symbols stay in math mode, words go inside \\text{}.

    So 'A (friendships)' renders as an italic A next to upright '(friendships)',
    instead of math mode turning the words into a product of italic variables.
    """
    parts = []                            # list of (is_text, latex) in order
    words = []
    for token in str(text).split():
        if _is_math_token(token):
            if words:
                parts.append((True, r"\text{" + " ".join(words) + "}"))
                words = []
            parts.append((False, token))
        else:
            words.append(token)
    if words:
        parts.append((True, r"\text{" + " ".join(words) + "}"))

    out = ""
    for i, (is_text, piece) in enumerate(parts):
        if i:
            # math mode eats plain spaces, so force one wherever prose abuts a symbol
            out += r"\;" if (is_text or parts[i - 1][0]) else " "
        out += piece
    return out


def _annotate(latex, name, label):
    """Prefix a matrix with 'name = ' or with 'label: ' (see the module docstring)."""
    if label is not None:
        return _annotation_latex(label) + r":\quad " + latex
    if name is not None:
        return _annotation_latex(name) + " = " + latex
    return latex


def show(array, name=None, label=None):
    """Display a vector or matrix as a typeset bracketed array.

    A 1-D array is shown as a column vector. Pass name='A' to prefix it with 'A = ',
    or label='...' to caption it instead (see the module docstring).
    """
    a = np.asarray(array)
    if a.ndim == 1:
        a = a.reshape(-1, 1)              # show a vector as a column
    display(Math(_annotate(_matrix_latex(a), name, label)))


def show_aug(A, b, name=None, label=None):
    """Display an augmented matrix [A | b] with a vertical bar (for solving systems)."""
    A = np.atleast_2d(np.asarray(A, dtype=float))
    b = np.asarray(b, dtype=float).reshape(-1, 1)
    n_cols = A.shape[1]
    rows = []
    for i in range(A.shape[0]):
        left = " & ".join(_format(x) for x in A[i])
        rows.append(left + " & " + _format(b[i, 0]))
    colspec = "c" * n_cols + "|c"
    latex = r"\left[\begin{array}{" + colspec + "}" + r" \\ ".join(rows) + r"\end{array}\right]"
    display(Math(_annotate(latex, name, label)))
