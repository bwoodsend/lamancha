#!/usr/bin/env sh
set -e
set -x

OLD_CWD=$PWD
cd "$(dirname "$0")"

git clean -Xfdq tests/mock-distributions

python -m pip install -Uq pip setuptools wheel flit
pip install -qe .[test]

cd tests/mock-distributions

cd flit_symlink
flit install --pth-file

cd ../setuptools_dual_license
pip install -q .

cd ../setuptools_editable
pip install -qe .

cd ../setuptools_install
python setup.py -q install

cd ../setuptools_missing_license
pip install -q .

cd ../setuptools_wheel
pip install -q .

cd ../setuptools_zipped_egg
python setup.py -q install

cd ../pyproject_toml_editable
pip install -qe .

cd "$OLD_CWD"

echo 'import sys; sys.some_hack_pth_is_ran = True' > "$(python -c 'import site; print(site.getsitepackages()[0])')/some-hack.pth"
