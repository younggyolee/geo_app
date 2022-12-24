# How to run

- Set up python virtual environment (for macOS)
  - If not macOS, please follow https://docs.djangoproject.com/en/4.1/ref/contrib/gis/install/ (follow `sqlite`)

```shell
brew install pyenv # if pyenv is not installed on the machine

# to fix SQLITE error (load_extension off error)
PYTHON_CONFIGURE_OPTS="--enable-loadable-sqlite-extensions" \
LDFLAGS="-L/usr/local/opt/sqlite/lib" \
CPPFLAGS="-I/usr/local/opt/sqlite/include" \
pyenv install 3.10.6

# If error on LDFLAGS or CPPFLAGS above,
# check sqlite directory using `brew info sqlite` or `which sqlite` or `which sqlite3`

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

- If you face an error (`django.db.utils.OperationalError: error in trigger ISO_metadata_reference_row_id_value_insert: no such column: rowid`) while running `python manage.py migrate`, run below and try again. ([reference](https://code.djangoproject.com/ticket/32935))

```shell
./manage.py shell -c "import django;django.db.connection.cursor().execute('SELECT InitSpatialMetaData(1);')";
```
