# Contributing Code
Thak you for considering to help with the development of this project.

To ensure smooth collaboration, please read this guideline.

## Do One Thing
Each pull request should be kept to the necessary changes to address one issue or add one feature.

## Test Your Changes
Test your changes before submitting a PR, preferrably with the most recent Anki release.
Include the Anki version you tested with in the PR.

## Code Style
### Names
For python code use CapitalCase for class names and snake_case for function and method names.

### PEP 8
Do it. I recommend [black](https://black.readthedocs.io/en/stable/index.html) to lint.

### Type Hints
Add or update PEP 484 type hints for any function you introduce or change.
Collection types must be capitalized and imported from the typing module to ensure compatibility with Python 3.8 and earlier.

### Docstrings
Docstrings may be added to provide a short overview of a function's purpose.
Because type hints are required, specification of the argument and return types is not required in docstrings.
Use the [reST](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#field-lists) format for docstrings.
