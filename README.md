# Path of Exile RESTful API

This is a very simple RESTful API for getting which Divination Cards can drop from which map (and vice versa) in the game Path of Exile.

This was mainly created as a learning project.

You can find the API docs at: https://poecardsapi.onrender.com/docs
It is using the free product tier at [Render](https://render.com/). so it might take **a few seconds** to load the first time.

## Setup

1. Clone the repository
2. Create a virtual environment

```
$ python3 -m venv venv
```

3. Activate the virtual environment

```
$ source venv/bin/activate
```

4. Install the requirements

```
(venv)$ pip install -r requirements.txt
```

5. Create .env file with the following content (more info: https://supabase.com/docs/reference/python/initializing):

```
SUPABASE_URL=<YOUR_SUPABASE_URL>
SUPABASE_KEY=<YOUR_SUPABASE_KEY>
```

6. Run the server

```
(venv)$ python3 main.py
```

7. By default, the server will run on `http://0.0.0.0` on port `8000`. You can change this in the `main.py` file.

8. Go to `http://0.0.0.0/8000/docs` to see the API documentation.

## Technologies used

- FastAPI with uvicorn to run the server
- Supabase (free tier) for the database
- Pydantic (comes with FastAPI) for schema and data validation
- Docker for containerization & deploying to Render

## Data source

The data provided from this API is obtained form multiple sources and is not guaranteed to be accurate as it relies on external sources.

- POE Wiki via Cargo Query. (Item, Map, Zone)
- POE Ninja Item price information and Divination Card Art URL.
- POE Official API to get current league information.
