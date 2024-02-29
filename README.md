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

Now you can run the application from within the virtual environment:

```bash
python -m simulated_annealing
```

### Test Suite
Run tests:

```bash
(.venv)
$ python -m pytest -v tests/
```


### Documentation

Build documentation:

```bash
(.venv)
$ python -m sphinx -M html docs docs/_build
```


## Installation

Packaging and distributing a Python application is dependent on the target
operating system(s) and execution environment, which could be a Python virtual
environment, Linux container, or native application.

Install the application to a self-contained Python virtual environment:

```bash
(.venv)
$ python -m pip install <project source>
$ cp -r <project source>/etc .venv/
$ .venv/Scripts/simulated_annealing --help
```


## Execution

The installed application includes a wrapper script for command line execution.
The location of this scripts depends on how the application was installed.

---

### Configuration

The application uses `TOML` files for configuration. Configuration supports
runtime parameter substitution via a shell-like variable syntax, *i.e.*
`var = ${VALUE}`. CLI invocation will use the current environment for
parameter substitution, which makes it simple to pass host-specific values
to the application without needing to change the config file for every
installation.

```toml
    mailhost = $SENDMAIL_HOST
```

### Logging

The application uses standard `Python logging`. All loggins is to `STDERR`,
nd the logging level can be set via the config file or on the command line.


* [TOML](https://toml.io)
* [Python logging](https://docs.python.org/3/library/logging.html)

---
