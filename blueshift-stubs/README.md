# blueshift-stubs

This is a stub-only package for the `blueshift` package for code completion/ intellisense support for 
blueshift strategy development on any modern IDE that support language server. This guides focuses on Visual Studio Code.

## How to use on VS Code

- clone the repo from GitHub and `cd` to the package root at `blueshift-developer-kit/blueshift-stubs`.
- run `python -m build` from the root of the directory to build the package.
- copy the source distribution `dist/blueshift_stubs-{version}.tar.gz` to your blueshift strategy development workspace root (e.g. `~/.blueshift/source`).
- in the blueshift strategy development workspace root, create a new venv and activate it.
- now install the package by running `pip install blueshift_stubs-5.0.0.tar.gz` in this new venv.
- **CAUTION**: do not install this if the original `blueshift` package is already installed. The original `blueshift` package will automatically provide type hints and auto-complete.
- launch VS Code, make sure the official Python extension is installed. Then in the command pallet invoke the `Python:Select Interpreter` and select the venv.
- Blueshift code completion should work now. If required, try `Developer:Reload Window` from the command pallete.

## How to trigger intellisense
Once the setup is done, start your strategy code by include the following 

```python
    from blueshift.types import *
    ...
```
This fetches types and enables code completion and type hints. The `blueshift` package version older than `5.0.0` does not support type hints. You need to comment it out (and other type hints) before running the strategy if you are using an earlier version.

## More tips

- copy the `pyrightconfig.json` from `blueshift-developer-kit/vs-code` to your blueshift strategy development workspace root to suppress errors from pylance/pyright if you do not have the original `blueshift` package installed.
- optionally, copy the entire `blueshift-code-extension` folder from the `blueshift-developer-kit/vs-code` to your `~/.vscode/extension` directory to enable completion snippets.