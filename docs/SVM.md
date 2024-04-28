# Support Vector Machine (SVM)

- SVMs use kernel functions to transform data into alternate dimensions.
    - Seek a linearly separable plane where one does not exist in the input dimensions.
- SVMs do **not** require prior knowledge of the problem domain.

**"Support Vector"** - points closest to the boundary.

The key insight of SVMs is that some example are more important that others,
and that paying attention to them can lead to better generalization. 


### Three Attractive Properties of SVMs

1. **Maximum Margin Separator** - decision bounder with the *largest margin* between support vectors.
2. **Kernel Trick** - Use kernel functions on pairs of input data in different dimensions or *feature spaces*.
3. **Nonparametric** - No need to tune hyperparameters.


## Usage

```shell
$ aiw svm -h
usage: aiw svm [-h] -f DATASET_FILENAME

options:
  -h, --help            show this help message and exit
  -f DATASET_FILENAME, --file DATASET_FILENAME
                        .csv file containing your dataset
(.venv-ai)
```

## Dataset

Dataset used was coronavirus prediction dataset [here](/docs/notebooks/data/corona-1.csv).

Upon first loading the dataset, this warning is output:

```shell
DtypeWarning: Columns (2,3,4,5,6,8) have mixed types. Specify dtype option on import or set low_memory=False.
```

This tells us that we need to clean whatever dataset we run an SVM model on.
