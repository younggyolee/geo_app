# How to run

- Set up python virtual environment (for macOS)
  - Other than macOS, please follow https://docs.djangoproject.com/en/4.1/ref/contrib/gis/install/
  - 
```shell
brew install pyenv # if pyenv is not installed on the machine

# check sqlite directory using `brew info sqlite`
PYTHON_CONFIGURE_OPTS="--enable-loadable-sqlite-extensions" \
LDFLAGS="-L/usr/local/opt/sqlite/lib" \
CPPFLAGS="-I/usr/local/opt/sqlite/include" \
pyenv install 3.10.6 

pyenv local 3.10.6
python -m venv venv
source venv/bin/activate
```

- Install required packages
```shell
pip install --upgrade pip
pip install -r requirements.txt

brew install gdal
brew install libgeoip
brew install spatialite-tools
```

- Run server
```shell
python manage.py migrate
python manage.py runserver
```

