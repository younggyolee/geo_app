# Backend Engineer Technical Interview

In this interview, you have to implement a simple REST API service to handle geographic data.

---

## Data Type

The service handles two data types: **points** and **contours**.  
A point represents a 2D coordinate which consists of x and y values, or longitude and latitude.  
A contour represents a single closed curve which consists of multiple (at least 3) points. For the simplicity, we consider only [simple polygons](https://en.wikipedia.org/wiki/Simple_polygon), which means there are no intersecting lines or holes within a contour.

Assuming it's geographic data, the x value(longitude) is a floating point in range of -180 to 180, and the y value(latitude) is a floating point in range of -90 to 90.

It is up to you to decide which data format to use in your internal codes or database, but your API should use one of the following data formats for input and output.

- [WKT format](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry)
- [GeoJSON](https://geojson.org/)

For example, if you decided to use WKT format, then the API should be able to handle data as below.

```
POINT (1.0 2.0)
POLYGON ((30.0 10.0, 40.0 40.0, 20.0 40.0, 10.0 20.0, 30.0 10.0))
```

On the other hand, GeoJson should be able to handle data as below.
```json
{
    "type": "Point",
    "coordinates": [1.0, 2.0]
}
{
    "type": "Polygon",
    "coordinates": [
      [30.0, 10.0], [40.0, 40.0], [20.0, 40.0], [10.0, 20.0], [30.0, 10.0]
    ]
}
```

Each point and contour should have a unique identifier which is either an auto-incremented value or UUID.

---

## Basic CRUD API Requirements

<a name="/points">

### [GET] `/points`

</a>

<details><summary>Response</summary>

```json
[
  {
    "id": 1,
    "data": "YOUR POINT REPRESENTATION"
  },
  {
    "id": 2,
    "data": "YOUR POINT REPRESENTATION"
  },
  ...
]
```
</details>

Returns the list of points stored in database with JSON format described as above.
A paginated query should be supported to limit the count of results.

### [GET] `/points/<id>`

<details><summary>Response</summary>

```json
{
  "id": 1,
  "data": "YOUR POINT REPRESENTATION"
}
```
</details>

Returns a point matching to the identifier with the JSON format described above.

<a name="/contours">

### [GET] `/contours`

</a>

<details><summary>Response</summary>

```json
[
  {
    "id": 1,
    "data": "YOUR CONTOUR REPRESENTATION"
  },
  {
    "id": 2,
    "data": "YOUR CONTOUR REPRESENTATION"
  },
  ...
]
```
</details>

Returns the list of contours stored in database with JSON format described above.
A paginated query should be supported to limit the count of results.

### [GET] `/contours/<id>`

<details><summary>Response</summary>

```json
{
  "id": 1,
  "data": "YOUR CONTOUR REPRESENTATION"
}
```
</details>

Returns a contour matching the identifier with the JSON format described as above.

### [POST] `/points`

<details><summary>Request Body</summary>

```json
{
  "data": "YOUR POINT REPRESENTATION"
}
```
</details>

<details><summary>Response</summary>

```json
{
  "id": 3,
  "data": "YOUR POINT REPRESENTATION"
}
```
</details>

Create a point with the format described as above.

### [POST] `/contours`

<details><summary>Request Body</summary>

```json
{
  "data": "YOUR CONTOUR REPRESENTATION"
}
```
</details>

<details><summary>Response</summary>

```json
{
  "id": 3,
  "data": "YOUR CONTOUR REPRESENTATION"
}
```
</details>

Create a contour with the format described as above.

### [PATCH] `/points/<id>`

<details><summary>Request Body</summary>

```json
{
  "data": "YOUR POINT REPRESENTATION"
}
```
</details>

<details><summary>Response</summary>

```json
{
  "id": 1,
  "data": "YOUR POINT REPRESENTATION"
}
```
</details>

Update a point matching to the identifier with the format described as above.

### [PATCH] `/contours/<id>`

<details><summary>Request Body</summary>

```json
{
  "data": "YOUR CONTOUR REPRESENTATION"
}
```
</details>

<details><summary>Response</summary>

```json
{
  "id": 1,
  "data": "YOUR CONTOUR REPRESENTATION"
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

### [GET] `/contours/<id1>/intersections?contour=<id2>`

This API calculates the contours of intersection area between contour `id1` and `id2`, and returns the results with following JSON format.

<details><summary>Response</summary>

```json
[
  "YOUR CONTOUR REPRESENTATION 1",
  "YOUR CONTOUR REPRESENTATION 2",
  ...
]
```
</details>

Note that there might be multiple contours of intersection area if the target contours are not convex.

<details><summary>Example</summary>
  <img src="https://www.researchgate.net/profile/Timothy_Schaerf/publication/251867052/figure/fig5/AS:669439477436420@1536618217313/An-example-of-crossing-contours-where-the-area-of-intersection-of-the-two-contours-is.png" width="300" height="300" />
</details>

You should return appropriate validation error if there is no contour matched by `id2`.

---

## Notes

- There is no restriction on the programming language or framework used.
Using appropriate libraries is recommended for quick and clear implementation.

- The environment setup and execution should be as simple as possible.
For the simplicity, we recommend using Docker, but it's also okay not to use it if you provide clear commands for setup or execution.

- You should prepare detailed documentation, including the architecture of your application, the design of your data model and API, the commands to launch, stop and test your application, and so on.
We recommend to use sufficient time on making your documentation as professional as possible.

- You can use any kind of database including RDBMS or NoSQL.

- Don't push yourself too hard. You can request to extend the deadline if you need more time.

- We'll evaluate every process of the interview including implementation, documentation and feedbacks after submission.

  

