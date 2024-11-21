#!/bin/sh

UNINSTALL=0
EDITABLE=0

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
        EDITABLE=1
        shift
        ;;
    esac
done


# Create a directory for the installation
INSTALL_DIR=$HOME/.local/share/compy

uninstall() {
    # Remove the installation directory
    rm -rf $INSTALL_DIR

    # Remove the symbolic link
    rm $HOME/.local/bin/compy -f

    echo "Uninstallation complete"
}

install() {
    mkdir -p $INSTALL_DIR

    # Create a virtual environment
    python3 -m venv $INSTALL_DIR

    # Install the package
    if [ $EDITABLE -eq 0 ]; then
        $INSTALL_DIR/bin/pip install git+https://github.com/Etto48/compy
    else
        $INSTALL_DIR/bin/pip install -e .
    fi

    # Create a symbolic link to the executable
    mkdir -p $HOME/.local/bin
    SCRIPT_PATH=$INSTALL_DIR/bin/compy
    ln -s $SCRIPT_PATH $HOME/.local/bin/compy

    echo "Installation complete"
}

if [ $UNINSTALL -eq 1 ]; then
    uninstall    
else
    install
fi
