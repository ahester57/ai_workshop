# Time for Crab :crab:

Crabs are here, and they're mighty tasty.

Knowing how old they are helps identify full-sized crabs that are ready for the pot.
 
Prediction (regression) of mud crab age based on physical features.

## YouTube Playlist

[![Time for Crab](https://i.ytimg.com/vi/2YvMW4UcBfA/hqdefault.jpg)](https://www.youtube.com/playlist?list=PL7gbeMmnbBH4yM3X_LzEfieB_VpacD9VE)

## Table of Contents

- [Datasets](datasets/README.md) :open_file_folder:
- [Exploratory Data Analysis](0-eda/README.md) :telescope: :mag_right:
    - [Overfitting](0-eda/overfit.ipynb) :dna:
- [Model Selection](1-models/README.md) :ballot_box:
- [Feature Engineering](2-features/README.md) :paintbrush:
- [Evaluation](3-evaluation/README.md) :chart_with_upwards_trend:


## Notebook Viewer

If you're having trouble viewing the notebooks in GitHub, try using [nbviewer](https://nbviewer.org/github/ahester57/ai_workshop/blob/master/notebooks/time_for_crab/0-eda/eda.ipynb).

https://nbviewer.org/github/ahester57/ai_workshop/blob/master/notebooks/time_for_crab/0-eda/eda.ipynb

### Also on Overleaf :leaves:

The project is also [available on Overleaf](https://www.overleaf.com/project/6638542e044376c414b65725), a LaTeX editor.
This is useful for writing reports and papers, but this repository remains the source of truth for this project.

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
