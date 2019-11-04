# The source files

The source folder contains the source code that we used in order to perform the
teaching.

## Initializing the environment

In order to initialize the environment one has to get the __virtualenv__ package,
and python version 3.6+. Do not forget to clone the submodules as well.

```bash
git submodule update
```

In order to install the virtual environment, use the following script. If
the components are already installed, only activation is necessary.

```bash
virtualenv -p python3.6 .venv # Use your python3.6+ executable (3.6, 3.7 or 3.8)
source .venv/bin/activate
pip install -r requirements.txt
ipython kernel install --user --name=duckietales
```

Now you can start the jupyter notebook server from the virtualenv.
Within the notebook you should switch the kernel to the duckietales one.

Note sometimes the kernel is not able to load the installed libraries, I don't
know why.

## Creating the datasets

This notebook describes the
