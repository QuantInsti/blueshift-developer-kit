# VS Code Configuration for Blueshift Development

This directory contains configurations and extensions to enhance the development experience for Blueshift strategies in VS Code, providing code snippets and improved type checking.

## Blueshift Code Extension

The `blueshift-code-extension` provides useful code snippets for common Blueshift callback functions, accelerating development by reducing boilerplate.

### Installation

To install this extension:

1.  Copy the `blueshift-code-extension` directory into your VS Code extensions folder (typically `~/.vscode/extensions/`).
2.  Restart VS Code.

### Usage

Once installed, you can trigger snippets by typing their prefixes in a Python file. For example, typing `def initialize` will suggest the `initialize` function snippet.

Available snippets include:
- `def initialize`: Creates the `initialize` function.
- `def before_trading_start`: Creates the `before_trading_start` callback function.
- `def handle_data`: Creates the `handle_data` callback function.
- `def on_data`: Creates the `on_data` callback function.
- `def on_trade`: Creates the `on_trade` callback function.
- `def on_stoploss`: Creates the `on_stoploss` callback function.
- `def on_takeprofit`: Creates the `on_takeprofit` callback function.
- `def on_update`: Creates the `on_update` callback function.

You can also use built-in templates to get you started. Start typing `template` and click the suggestions.

Available templates are:
- `sma crossover`: A modular technical indicator based strategy with periodic signal check.
- `intraday option`: A simple option selling strategy highlighiting realtime response, option symbology, and stoploss use.
- `large universe (pipeline)`: A ersion of time-series momentum strategy demonstrating the advanced pipeline APIs for handling large universe.

## Pyright Configuration

The `pyrightconfig.json` file provides configuration for Pyright, a static type checker for Python. This configuration helps suppress some errors in vs code/ pylance case you are developing Blueshift strategies with only the stub package for type hints and do not have the full package installed.

### Installation

To use this configuration:

1.  Copy the `pyrightconfig.json` file to the root of your Blueshift strategy development workspace.
2.  Ensure you have the official Python extension installed in VS Code.

### Usage

With `pyrightconfig.json` in your workspace root, Pyright will automatically pick up the configuration, which includes:
- `"extraPaths": "."`: Adds the current directory to the paths Pyright searches for modules.
- `"reportMissingModuleSource": false`: Suppresses errors for missing module sources.
- `"reportAttributeAccessIssue": false`: Suppresses errors for attribute access issues.
- `"reportWildcardImportFromLibrary":false`: Suppresses errors for wildcard imports from libraries.

These settings are tailored to work well with the `blueshift-stubs` package, ensuring that type hints and autocompletion function correctly without unnecessary warnings or errors.
