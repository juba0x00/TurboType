rm -r dist/

pip install --upgrade pip --break-system-packages
pip install build --break-system-packages
pip install twine --break-system-packages 
python setup.py sdist


pip install dist/*.gz --break-system-packages
