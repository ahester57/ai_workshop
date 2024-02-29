# Simulated Annealing

A simulated annealing process to determine the optimal weight values of an artificial neuron.
Python 3.8+ is required.

```
function SIMULATED-ANNEALING(problem, schedule) returns a solution State
  current <- problem.INITIAL
  for t = 1 to inf do
      T <- schedule(t)
      if T = 0 then return current
      next <- a randomly selected successor of current
      delta_E <- VALUE(current) - VALUE(next)
      if delta_E > 0 then current <- next
      else current <- next only with probability e^(-delta_E/T)
```

## Temperature Analysis

Simulated annealing simulates the process of annealing glass or metal.
It involves heating it up until malleable, then shaping it until it cools and hardens.

The temperature parameter, as defined bythe `schedule` lambda function in this implementation, 
can have a large impact on the output of this algorithm.

See the [detailed temperature analysis](docs/temperature_analysis.md) in the `docs/` directory.

---

## Development

### Create a Virtual Environment

Create the virtual environment, enter into it with `source`-ry.

```bash
$ python -m venv .venv
$ source .venv/Scripts/activate
$ echo "Confirm you're using the correct python with: "
$ which python
=> Should show path to your .venv
```

And install the package locally:

```bash
(.venv)
$ pip install -e ".[dev]"
```

#### Install with Optional Dependencies

In the above, `".[dev]"` means you want to install the optional packages under 'dev' in [the project pyproject.toml](pyproject.toml).  
There is also a visual mode driven by networkx and matplotlib. To install dev tools plus visual mode, use this pip install command instead:

```bash
(.venv)
$ pip install -e ".[dev,visual]"
```

See this reference for more info about [installing Python packages](https://packaging.python.org/en/latest/tutorials/installing-packages/).

### Running

Now you can run the application from within the virtual environment:

```bash
(.venv)
$ simulated_annealing
```

#### Test Suite

Run tests:

```bash
(.venv)
$ python -m pytest -v tests/
```


### Documentation

See the [docs](docs/) directory.

---

## Execution

Once installed, the application can be via the command line. Inside your virtual environment:

```bash
(.venv)
$ simulated_annealing --help
usage: simulated_annealing [-h] [-c CONFIG] [-v] [-w WARN] {anneal} ...

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        config file [etc/config.toml]
  -v, --version         print version and exit
  -w WARN, --warn WARN  logger warning level [WARN]

subcommands:
  {anneal}
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
Find the code in the [core module](src/simulated_annealing/core/).


* [TOML](https://toml.io)
* [Python logging](https://docs.python.org/3/library/logging.html)

---
