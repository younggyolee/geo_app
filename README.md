# Tasks
- [x] Decide on the format => GeoJSON
- [x] Implement API endpoints
- [x] Support pagination for GET list endpoints
- [x] Document commands to launch, stop and test the application
- [x] Document architecture of the application
- [x] Design of data model
- [x] Document API endpoints

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

# Data model
- It has `id` field which is automatically added from Django side. 
- It has `data` field which is a GEOSGeometry object.
- `api/models.py`
```python
from django.contrib.gis.db import models

class Point(models.Model):
    data = models.PointField()

class Contour(models.Model):
    data = models.PolygonField()
```

# Architecture of the app
- It basically uses 3 packages: `Django` + `Django-rest-framework` + `djangorestframework-gis`

### Django
- `geo_app`: boilerplate app. It has `settings.py` for the configuration of the whole app.
- `api`: All the business logics reside here.

### Django-rest-framework
- DRF(Django-rest-framework) was implemented since it reduces lots of code duplication on common API endpoint functionalities, serialization and validation.
- [Concrete View Class](https://www.django-rest-framework.org/api-guide/generic-views/#concrete-view-classes) functionality was used to drastically reduce the amount of code.

### djangorestframework-gis
- `djangorestframework-gis` was applied to handle input/output data in GeoJSON format.
- Without `djangorestframework-gis`, GEOSGeometry object is returned like this
```json
{
    "id": 1,
    "data": "SRID=4326;POINT (9.999 9.999)"
}
```

- With `djangorestframework-gis`,
```json
{
    "id": 1,
    "data": {
        "type": "Point",
        "coordinates": [
            9.999,
            9.999
        ]
    }
}
```

# Sample request & response

### [GET] `/points`

</a>

<details><summary>Response</summary>

```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "data": {
                "type": "Point",
                "coordinates": [
                    9.999,
                    9.999
                ]
            }
        },
        {
            "id": 2,
            "data": {
                "type": "Point",
                "coordinates": [
                    1.0,
                    2.0
                ]
            }
        }
    ]
}
```
</details>

Returns the list of points stored in database with JSON format described as above.
A paginated query should be supported to limit the count of results.

### [GET] `/points/<id>`

<details><summary>Response</summary>

```json
{
    "id": 1,
    "data": {
        "type": "Point",
        "coordinates": [
            9.999,
            9.999
        ]
    }
}
```
</details>

Returns a point matching to the identifier with the JSON format described above.

<a name="/contours">

### [GET] `/contours`

</a>

<details><summary>Response</summary>

```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "data": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            1.0,
                            2.0
                        ],
                        [
                            -5.0,
                            2.0
                        ],
                        [
                            -5.0,
                            -5.0
                        ],
                        [
                            2.0,
                            -5.0
                        ],
                        [
                            2.0,
                            1.0
                        ],
                        [
                            0.0,
                            -1.0
                        ],
                        [
                            -1.0,
                            0.0
                        ],
                        [
                            1.0,
                            2.0
                        ]
                    ]
                ]
            }
        },
        {
            "id": 2,
            "data": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            0.0,
                            0.0
                        ],
                        [
                            10.0,
                            0.0
                        ],
                        [
                            10.0,
                            10.0
                        ],
                        [
                            0.0,
                            10.0
                        ],
                        [
                            0.0,
                            0.0
                        ]
                    ]
                ]
            }
        }
    ]
}
```
</details>

Returns the list of contours stored in database with JSON format described above.
A paginated query should be supported to limit the count of results.

### [GET] `/contours/<id>`

<details><summary>Response</summary>

```json
{
    "id": 1,
    "data": {
        "type": "Polygon",
        "coordinates": [
            [
                [
                    1.0,
                    2.0
                ],
                [
                    -5.0,
                    2.0
                ],
                [
                    -5.0,
                    -5.0
                ],
                [
                    2.0,
                    -5.0
                ],
                [
                    2.0,
                    1.0
                ],
                [
                    0.0,
                    -1.0
                ],
                [
                    -1.0,
                    0.0
                ],
                [
                    1.0,
                    2.0
                ]
            ]
        ]
    }
}
```
</details>

Returns a contour matching the identifier with the JSON format described as above.

### [POST] `/points`

<details><summary>Request Body</summary>

```json
{
  "data": {
    "type": "Point",
    "coordinates": [1, 2]
  }
}
```
</details>

<details><summary>Response</summary>

```json
{
    "id": 3,
    "data": {
        "type": "Point",
        "coordinates": [
            1.0,
            2.0
        ]
    }
}
```
</details>

Create a point with the format described as above.

### [POST] `/contours`

<details><summary>Request Body</summary>

```json
{
  "data": {
    "type": "Polygon",
    "coordinates": [
        [
            [0,0], [10,0], [10,10], [0,10], [0,0]
        ]
    ]
  }
}
```
</details>

<details><summary>Response</summary>

```json
{
    "id": 2,
    "data": {
        "type": "Polygon",
        "coordinates": [
            [
                [
                    0.0,
                    0.0
                ],
                [
                    10.0,
                    0.0
                ],
                [
                    10.0,
                    10.0
                ],
                [
                    0.0,
                    10.0
                ],
                [
                    0.0,
                    0.0
                ]
            ]
        ]
    }
}
```
</details>

Create a contour with the format described as above.

### [PATCH] `/points/<id>`

<details><summary>Request Body</summary>

```json
{
  "data": {
    "type": "Point",
    "coordinates": [2, 4]
  }
}
```
</details>

<details><summary>Response</summary>

```json
{
    "id": 3,
    "data": {
        "type": "Point",
        "coordinates": [
            2.0,
            4.0
        ]
    }
}
```
</details>

Update a point matching to the identifier with the format described as above.

### [PATCH] `/contours/<id>`

<details><summary>Request Body</summary>

```json
{
  "data": {
    "type": "Polygon",
    "coordinates": [
        [
            [0,0], [1,1], [3,0], [0,0]
        ]
    ]
  }
}
```
</details>

<details><summary>Response</summary>

```json
{
    "id": 3,
    "data": {
        "type": "Polygon",
        "coordinates": [
            [
                [
                    0.0,
                    0.0
                ],
                [
                    1.0,
                    1.0
                ],
                [
                    3.0,
                    0.0
                ],
                [
                    0.0,
                    0.0
                ]
            ]
        ]
    }
}
```
</details>

Update a contour matching to the identifier with the format described as above.

### [DELETE] `/points/<id>`

Delete a single point matching the identifier. You can return either the deleted data or no content with status 204.

### [DELETE] `/contours/<id>`

Delete a single contour matching the identifier. You can return either the deleted data or no content with status 204.

---

## Advanced API Requirements

### [GET] `/points?contour=<id>`

  - When the query parameter `contour` is appended to [[GET]/points](#/points) API, it should return points within the inner area of the contour specified by `id`.
  - You should return appropriate validation error if there is no contour matched by `id`.

<details><summary>Response</summary>

```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "data": {
                "type": "Point",
                "coordinates": [
                    9.999,
                    9.999
                ]
            }
        },
        {
            "id": 3,
            "data": {
                "type": "Point",
                "coordinates": [
                    2.0,
                    4.0
                ]
            }
        }
    ]
}
```
</details>

### [GET] `/contours/<id1>/intersections?contour=<id2>`

This API calculates the contours of intersection area between contour `id1` and `id2`, and returns the results with following JSON format.

<details><summary>Response</summary>

Example 1

```json
{
    "type": "MultiPolygon",
    "coordinates": [
        [
            [
                [
                    1.0,
                    2.0
                ],
                [
                    0.0,
                    1.0
                ],
                [
                    0.0,
                    2.0
                ],
                [
                    1.0,
                    2.0
                ]
            ]
        ],
        [
            [
                [
                    2.0,
                    1.0
                ],
                [
                    2.0,
                    0.0
                ],
                [
                    1.0,
                    0.0
                ],
                [
                    2.0,
                    1.0
                ]
            ]
        ]
    ]
}
```

Example 2
```json
{
    "type": "Polygon",
    "coordinates": [
        [
            [
                0.0,
                0.0
            ],
            [
                0.0,
                5.0
            ],
            [
                5.0,
                5.0
            ],
            [
                5.0,
                0.0
            ],
            [
                0.0,
                0.0
            ]
        ]
    ]
}
```

</details>
