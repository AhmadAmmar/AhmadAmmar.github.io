"""Build the tutorial notebooks: each src/NN_name.py (cells separated by '# %%', markdown cells by '# %% [markdown]')
becomes notebooks/NN_name.ipynb and is executed top to bottom, so every output shown is a real result.

    python build.py            # all notebooks
    python build.py 02 05      # only those whose name starts with these numbers

Run with the analysis environment (pandas, geopandas, folium, plotly, statsmodels, lightgbm, scikit-learn).
"""
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

HERE = Path(__file__).resolve().parent


def cells(text):
    """Split a percent-format script into notebook cells."""
    out, kind, buf = [], None, []

    def flush():
        """Close the current cell."""
        src = "\n".join(buf).strip("\n")
        if kind == "md":
            src = "\n".join(l[2:] if l.startswith("# ") else l.lstrip("#") for l in src.splitlines())
            out.append(nbformat.v4.new_markdown_cell(src))
        elif kind == "code" and src.strip():
            out.append(nbformat.v4.new_code_cell(src))
    for line in text.splitlines():
        if line.startswith("# %%"):
            flush(); buf = []
            kind = "md" if "[markdown]" in line else "code"
        else:
            buf.append(line)
    flush()
    return out


def build(src):
    """Convert and execute one notebook."""
    nb = nbformat.v4.new_notebook()
    nb.cells = cells(src.read_text(encoding="utf-8"))
    nb.metadata["kernelspec"] = {"name": "eo", "display_name": "Python (eo)", "language": "python"}
    NotebookClient(nb, timeout=3600, kernel_name="eo", resources={"metadata": {"path": str(HERE / "notebooks")}}).execute()
    out = HERE / "notebooks" / (src.stem + ".ipynb")
    nbformat.write(nb, out)
    print("built", out.name, flush=True)


if __name__ == "__main__":
    (HERE / "notebooks").mkdir(exist_ok=True)
    for s in sorted((HERE / "src").glob("*.py")):
        if len(sys.argv) == 1 or any(s.name.startswith(a) for a in sys.argv[1:]):
            build(s)
