#!/bin/sh

if [ ! -d venv ]
then
    virtualenv venv
    virtualenv -p /usr/bin/python3.4 venv
fi

echo "Reminder :"
echo "Activation    source venv/bin/activate"
echo "Deactivation  deactivate"
echo "Running test  python -m unittest discover ."
