# AI Workshop

## Notebooks

A [collection](notebooks) of Jupyter notebooks for various ML tasks.

### Notebooks ToC

- [Breast Cancer Classification](notebooks/breast_cancer/README.md)
- [Simulated Annealing](notebooks/simulated_annealing/README.md)
- [Support Vector Machines](notebooks/svm/README.md)
- [Time for Crab](notebooks/time_for_crab/README.md) :crab:

## Development

### Create a Virtual Environment

Create the virtual environment with the following commands:

```shell
$ mkdir -p ~/dev
$ python -m venv ~/dev/.venv
$ source ~/dev/.venv/Scripts/activate
$ echo "Confirm you're using the correct python with: "
$ which python
=> Should show path to your .venv
```

Alternatively, you can use the provided bash scripts to enter into it with `source`-ry.

```shell
$ ./create-venv.sh
$ source source-me-to-activate-venv.sh
```


#### Install Development Dependencies

```shell
(.venv)
$ pip install -e ".[dev]"
```

#### Install with Optional Dependencies

In the above, `".[dev]"` means you want to install the optional packages under 'dev' in [the project pyproject.toml](pyproject.toml).  
There is also a visual mode driven by networkx and matplotlib. To install dev tools plus visual mode, use this pip install command instead:

```shell
(.venv)
$ pip install -e ".[dev,jupyter]"
```

See this reference for more info about [installing Python packages](https://packaging.python.org/en/latest/tutorials/installing-packages/).

### Running

Now you can run the application from within the virtual environment:

```shell
(.venv)
$ aiw
```

#### Test Suite

Run tests:

```shell
(.venv)
$ python -m pytest -v tests/
```


### Documentation

### Contents

* [Simulated Annealing Temperature Analysis](docs/ANNEAL.md)
* [Support Vector Machines](docs/SVM.md)
* [Image Convolution](docs/CONVOLVE.md)

See the [docs](docs/) directory for more.

---

## Execution

Once installed, the application can be run via the command line. Inside your virtual environment:

```shell
(.venv)
$ aiw --help
usage: aiw [-h] [-c CONFIG] [-v] [-w WARN] {anneal,svm,convolve} ...

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        config file [etc/config.toml]
  -v, --version         print version and exit
  -w WARN, --warn WARN  logger warning level [WARN]

subcommands:
  {anneal,svm,convolve}
(.venv-ai)
```

---

### Configuration

The application uses `TOML` files for configuration. Configuration supports
runtime parameter substitution via a shell-like variable syntax, *i.e.*
`var = ${VALUE}`. CLI invocation will use the current environment for
parameter substitution, which makes it simple to pass host-specific values
to the application without needing to change the config file for every
installation. Config file is located in [/etc](etc/).

```toml
    logging = "INFO"
```

### Logging

The application uses standard `Python logging`. All logging is to `STDERR`,
and the logging level can be set via the config file or on the command line.
Find the code in the [core module](src/ai_workshop/core/).


* [TOML](https://toml.io)
* [Python logging](https://docs.python.org/3/library/logging.html)

---
