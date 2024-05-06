# Time for Crab :clock430: :crab:

Crabs are here, and they're mighty tasty.

Knowing how old they are helps identify full-sized crabs that are ready for the pot.
 
## Table of Contents

- [Datasets](datasets/README.md) :fax: :open_file_folder:
- [Exploratory Data Analysis](0-eda/README.md) :telescope: :mag_right:
    - [Overfitting](0-eda/overfit.ipynb) :pen: :dna:
- [Model Selection](1-models/README.md) :joystick: :ballot_box:
- [Feature Engineering](2-features/README.md) :paintbrush: :toolbox: 
- [Evaluation](3-evaluation/README.md) :microscope: :chart_with_upwards_trend:

![Crab](https://upload.wikimedia.org/wikipedia/commons/b/b1/Mud_crab%2C_Scylla_serrate.jpg?20220920192756)

Prediction (regression) of mud crab age based on physical features.

## Notebook Viewer

If you're having trouble viewing the notebooks in GitHub, try using [nbviewer](https://nbviewer.org/github/ahester57/ai_workshop/blob/master/notebooks/time_for_crab/0-eda/eda.ipynb).

https://nbviewer.org/github/ahester57/ai_workshop/blob/master/notebooks/time_for_crab/0-eda/eda.ipynb

### Also on Overleaf :leaves:

The project is also [available on Overleaf](https://www.overleaf.com/project/6638542e044376c414b65725), a LaTeX editor.
This is useful for writing reports and papers, but this repository remains the source of truth for this project.

## Export a Notebook

To export the notebooks to HTML, use the following commands:

```bash
jupyter nbconvert --to html --embed-images notebooks/time_for_crab/0-eda/eda.ipynb
jupyter nbconvert --to html --embed-images notebooks/time_for_crab/0-eda/overfit.ipynb
jupyter nbconvert --to html --embed-images notebooks/time_for_crab/1-models/models.ipynb
jupyter nbconvert --to html --embed-images notebooks/time_for_crab/2-features/features.ipynb
jupyter nbconvert --to html --embed-images notebooks/time_for_crab/3-evaluation/evaluation.ipynb
```
