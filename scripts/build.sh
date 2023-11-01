#!/bin/bash

# Basic script to build a fresh installation of ThreatIngestor locally.
# NOTE: This wipes all data from state.db and artifacts.* from the local directory. This is only here to quickly build and install a fresh version locally outside of Docker.

function does_pip_exist() {
    if type "pip3" > /dev/null
    then
        return 0
    else
        return 1
    fi
}

function build() {
    if does_pip_exist
    then
        pip3 uninstall threatingestor -y

        rm -r dist/ threatingestor.egg-info/
        rm artifacts.csv output.csv artifacts.db output.db state.db

        python3 -m build
        pip3 install dist/threatingestor-*.whl
    else
        echo "Missing pip"
        exit 1
    fi
}

build
