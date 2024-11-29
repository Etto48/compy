#!/bin/bash

UNINSTALL=0
INSTALL_MODE=git

# Parse command line arguments
for arg in "$@"; do
    case $arg in
        -h | --help)
        echo "Usage: ./install.sh [OPTIONS]"
        echo "Options:"
        echo "  -h, --help      Display this help message"
        echo "  -u, --uninstall Uninstall the package"
        echo "  -e, --editable  Install the package in editable mode from the current directory"
        exit 0
        ;;
        -u | --uninstall)
        UNINSTALL=1
        shift
        ;;
        -e | --editable)
        INSTALL_MODE=editable
        shift
        ;;
        -l | --local)
        INSTALL_MODE=local
        shift
        ;;
    esac
done


# Create a directory for the installation
INSTALL_DIR=$HOME/.local/share/compy

uninstall() {
    echo "Uninstalling compy..."
    # Remove the installation directory
    rm -rf $INSTALL_DIR

    # Remove the symbolic link
    rm $HOME/.local/bin/compy -f

    echo "Uninstallation complete"
}

install() {
    mkdir -p $INSTALL_DIR

    # Check if python3 is installed
    if ! command -v python3 > /dev/null; then
        echo "Python3 is not installed"
        exit 1
    fi

    # Check if venv is installed
    if ! python3 -m venv --help > /dev/null; then
        echo "The venv module is not installed"
        exit 1
    fi

    # Check if git is installed
    if [ $INSTALL_MODE == "git" ] && ! command -v git > /dev/null; then
        echo "Git is not installed"
        exit 1
    fi

    echo "Installing compy..."
    # Create a virtual environment
    python3 -m venv $INSTALL_DIR > /dev/null

    # Install the package
    case $INSTALL_MODE in
        git)
            $INSTALL_DIR/bin/pip install git+https://github.com/Etto48/compy > /dev/null
            ;;
        local)
            $INSTALL_DIR/bin/pip install . > /dev/null
            ;;
        editable)
            $INSTALL_DIR/bin/pip install -e . > /dev/null
            ;;
    esac

    # Create a symbolic link to the executable
    mkdir -p $HOME/.local/bin
    SCRIPT_PATH=$INSTALL_DIR/bin/compy
    ln -fs $SCRIPT_PATH $HOME/.local/bin/compy

    # check if .local/bin is in PATH
    if [[ ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
        echo "~/.local/bin is already in PATH"
    else
        if [[ "$SHELL" == "/bin/zsh" ]]; then
            echo "Add the following line in ~/.zshrc:"
        elif [[ "$SHELL" == "/bin/bash" ]]; then
            echo "Add the following line in ~/.bashrc:"
        else
            echo "Add the following line to your shell configuration file:"
        fi
        echo "export PATH=\$HOME/.local/bin:\$PATH"
    fi

    echo "Installation complete"
}

if [ $UNINSTALL -eq 1 ]; then
    uninstall    
else
    install
fi
