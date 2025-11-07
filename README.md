<div align="center">
  <img src="./assets/Blueshift logo 50-50 (text).png" alt="Blueshift Logo" width="150"/>
</div>

<h1 align="center">Blueshift Developer Kit</h1>

<p align="center">
  A collection of tools to supercharge trading strategy development on the Blueshift platform.
</p>

---

This repository contains a set of utilities designed to enhance the development experience for traders and programmers building on Blueshift. These tools provide better auto-completion, faster coding with templates, and AI-powered strategy generation.

## Features

| Directory                               | Description                                                                                                                                 |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| [`blueshift-stubs/`](./blueshift-stubs)   | A **PEP 561 stub package** that provides full type hints for the Blueshift API, enabling static analysis and superior editor auto-completion. |
| [`vs-code/`](./vs-code)                 | A **VS Code extension** with code snippets for all major Blueshift callbacks and strategy templates to accelerate development.                |
| [`llm-guides/`](./llm-guides)             | **LLM prompt-engineering guides** to help AI models like GPT and Gemini generate accurate and robust Blueshift trading strategies from text. |

## 1. Blueshift Stubs (`blueshift-stubs`)

This directory contains a stub package (`.pyi` files) that describes the complete public API of the `blueshift` library. Modern editors like VS Code (with Pyright/Pylance) and PyCharm use these files to provide real-time type checking and intelligent auto-completion.

### Installation

To get the benefit of the stubs, install the package in your development environment from this directory:

```bash
pip install ./blueshift-stubs
```

Once installed, your editor will automatically detect the type hints for the `blueshift` library.

## 2. VS Code Extension & Snippets (`vs-code`)

This folder contains two key resources for VS Code users:

*   **Pyright Configuration (`pyrightconfig.json`):** A pre-configured setup for the Pyright type checker to ensure it works seamlessly with the `blueshift-stubs` package.
*   **Snippet Extension (`blueshift-code-extension`):** A lightweight extension that provides powerful code snippets. Simply start typing a Blueshift function name (e.g., `initialize`, `handle_data`) or a template name (e.g., `template:sma crossover`) to quickly insert boilerplate code.

### Installation

To use the snippets, copy the `blueshift-code-extension` directory into your VS Code extensions folder and restart the editor. The typical locations are:
*   **Windows:** `%USERPROFILE%\.vscode\extensions`
*   **macOS/Linux:** `~/.vscode/extensions`

## 3. LLM Guides (`llm-guides`)

Leverage the power of Large Language Models (LLMs) to write your trading strategies. This directory contains comprehensive guides to be used as context for models like ChatGPT, Claude, or Gemini. These guides provide the LLM with the necessary knowledge of the Blueshift API, best practices, and code structure.

### Usage

Refer to the [`README.md` in the `llm-guides` directory](./llm-guides/README.md) for detailed instructions on how to effectively use these guides and for expert prompt engineering tips.

## Getting Started

To make the most of this toolkit:

1.  **Install the stubs** to enable type-checking and auto-complete in your editor.
2.  **Set up your VS Code** with the provided Pyright configuration and install the snippet extension.
3.  **Explore the LLM guides** to learn how to rapidly prototype strategies using natural language.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/your-username/your-repository-name/issues) (once you create the repository).
