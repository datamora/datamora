deactivate
rm -rf *.pyc
tox -e dev "$@"
. .tox/dev/bin/activate
