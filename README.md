# Product catalog project

## Install dependencies
```
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install -r requirements.txt
```

## Run migrations

```
$ cd src
$ python3 manage.py migrate
```

## Run project
```
$ python3 manage.py runserver
```

## Run celery worker (windows)
```
$ celery -A productCatalog worker -l info -E --pool=solo
```

## Run celery worker (linux)
```
$ celery -A productCatalog worker -l info -E
```

## Products API basic explanation

## Authentication
### POST /api/v1/auth/token/
Use this endpoint to get a json web token to use the private products API: (POST, PUT, DELETE) operations
- Request body:
```
{
    "username": "rsegurac",
    "password": "AngryCat#69"
}
```
- Add header: *Authorization: Bearer {{yourAccessToken}}*

### POST /api/v1/products/
- This endpoint is used to create a product, you need to send the authorization header to use it.
- If you send visible = true, the product will be visible for anonymous users (default is visible = false)
- Example request body
```
{
    "sku": "123",
    "name": "test",
    "price": 20.0,
    "brand": "Test",
    "visible": false
}
```
- Example response body
```
{
    "id": "73c56fe6-0b43-4f4b-a15d-cfadb3adf90b",
    "sku": "123",
    "name": "test",
    "price": 20.0,
    "brand": "Test",
    "visible": false
}
```

### PUT /api/v1/products/{{product_id}}/
- Update a product by id
- All the admin users will be notified if you call this endpoint
- There is a celery worker that performs the async logic of sending a notification
- Request body: POST endpoint properties

### GET /api/v1/products/?page=1
- List products
- Includes pagination parameter: page (numeric pagination)
- If a product is not visible, it won't be returned to the anonymous users
- This endpoint call an async task to save visualization metrics

### DELETE /api/v1/products/{{product_id}}/
- Delete a product by id