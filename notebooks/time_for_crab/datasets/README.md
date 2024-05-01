# Datasets :fax: :open_file_folder:

We will be studying tabular, non-time-series data.

> One debate which we only touch on briefly in the report is: what is the best type of model for tabular data problems?
> 
> As a quick reminder, by tabular data problems we mean any problem where the training data is structured as rows and
> columns of scalar numerical values — in contrast to problems where the data is structured as a series of images,
> or text, or interactions between an agent and its environment.
> 
> Many “business ML” problems fall into the category of tabular data problems.
> The main candidate models in recent years for tabular data are neural networks and gradient-boosted decision
> trees (GBDTs) , and the debate over which is better has been going on for a while.
> 
> Gradient-boosted decision trees are ensemble models — combinations of many smaller models — and are iteratively built up, one tree at a time. Popular GBDT libraries include LightGBM, CatBoost, and XGBoost.
> 
> https://mlcontests.com/tabular-data/

### Notebook

Check out the [Exploratory Data Analysis](../0-eda/README.md) notebook for more.

### Crab Age Prediction Dataset Columns

The crab dataset contains the following columns:

---

| Column Name    | Description                                                                                         |
|----------------|-----------------------------------------------------------------------------------------------------|
| Sex            | Gender of the Crab - Male, Female and Indeterminate.                                                |
| Length         | Length of the Crab (in Feet; 1 foot = 30.48 cms)                                                    |
| Diameter       | Diameter of the Crab (in Feet; 1 foot = 30.48 cms)                                                  |
| Height         | Height of the Crab (in Feet; 1 foot = 30.48 cms)                                                    |
| Weight         | Weight of the Crab (in ounces; 1 Pound = 16 ounces)                                                 |
| Shucked Weight | Weight without the shell (in ounces; 1 Pound = 16 ounces)                                           |
| Viscera Weight | is weight that wraps around your abdominal organs deep inside body (in ounces; 1 Pound = 16 ounces) |
| Shell Weight   | Weight of the Shell (in ounces; 1 Pound = 16 ounces)                                                |
| Age            | Age of the Crab (in months)                                                                         |

---

## Data Sources

- [Crab Age Prediction](https://www.kaggle.com/datasets/sidhus/crab-age-prediction) on Kaggle (10.34740/kaggle/dsv/2834512).
- Tabular [archive.ics.uci.edu search query](https://archive.ics.uci.edu/datasets?skip=0&take=10&sort=desc&orderBy=NumHits&search=&Types=Tabular).

Accessed 2024-04-27.

---
