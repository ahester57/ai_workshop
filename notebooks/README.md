# Jupyter Notebooks :ringed_planet: :notebook_with_decorative_cover:

A collection of Jupyter notebooks for various ML tasks.

## Table of Contents

- [Breast Cancer Classification](breast_cancer/README.md)
- [Simulated Annealing](simulated_annealing/README.md)
- [Support Vector Machines](svm/README.md)
- [Time for Crab](time_for_crab/README.md) :crab:

## Datasets

Local copies of the following datasets have been saved in */datasets directories for reproducibility.

## Export a Notebook

You will need to install the optional `jupyter` dependencies to export the notebooks.

From the project root, run:

```bash
pip install -e .[jupyter]
```

### Export to HTML

To export the notebooks to HTML, use the following commands:

```bash
jupyter nbconvert --to html --embed-images notebooks/time_for_crab/0-eda/eda.ipynb
jupyter nbconvert --to html --embed-images notebooks/time_for_crab/0-eda/overfit.ipynb
jupyter nbconvert --to html --embed-images notebooks/time_for_crab/1-models/models.ipynb
jupyter nbconvert --to html --embed-images notebooks/time_for_crab/2-features/features.ipynb
jupyter nbconvert --to html --embed-images notebooks/time_for_crab/3-evaluation/evaluation.ipynb
```

### Export to LaTeX

To export the notebooks to LaTeX or PDF, you'll need some additional packages:

- `pandoc` - install with `pip install -e .[latex]` from the project root.
- `texlive` - install for your OS using the instructions [here](https://www.tug.org/texlive/).
    - TexLive focuses more on user security than MikTeX, hence the recommendation.
    - This takes a while to install, so be patient.

Then use the following commands to generate the LaTeX files:

```bash
jupyter nbconvert --to latex notebooks/time_for_crab/0-eda/eda.ipynb
```

Or to generate the PDF files:

```bash
jupyter nbconvert --to pdf notebooks/time_for_crab/0-eda/eda.ipynb
```
