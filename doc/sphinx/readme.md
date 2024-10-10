# Sphinx docs:

The following files exist to document the T-Route package using Sphinx and the PyData template

To build these docs locally, you can run the following commands

```shell
pip install -e .[doc]
```
- Installs all packages required for building documentation

```shell 
make html
```
- Builds the docs into html files (See `doc/sphinx/build` for the output

```shell
cd build/html
python -m http.server
```
- Runs the docs locally on port 8000

# Information on contributing to the docs

See here: https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html# for information on the pydata sphinx theme and how RST works in sphinx
