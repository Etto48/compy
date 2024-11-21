# Compy

Compy is a tool for initializing and managing Python projects.

## Installation

To install Compy, run the following command:

```sh
sh -c "$(curl -sSL https://raw.githubusercontent.com/Etto48/compy/main/install.sh)"
```

To uninstall Compy, run the following command:

```sh
sh -c "$(curl -sSL https://raw.githubusercontent.com/Etto48/compy/main/install.sh)" -- --uninstall
```

## Usage

To initialize a new Python project, run the following command:

```bash
compy init .
```

This will create a new Python project in the current directory.

To add a new dependency to the project, run the following command:

```bash
compy add <package>
```

This will add the specified package to the project in the current directory.
