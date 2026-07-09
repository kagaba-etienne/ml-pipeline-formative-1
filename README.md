# ML Pipeline Formative 1
This project uses FastAPI, PostgreSQL, and MongoDB. Follow these steps to get the project up and running.

## 1. Set up MongoDB Atlas

1. Create an account on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Create a new cluster (the free tier works fine).
3. Under "Database Access", create a new database user and save the credentials.
4. Under "Network Access", add your IP address (or `0.0.0.0/0` to allow all).
5. Click "Connect", select "Connect your application", and copy your connection string.
6. Create a `.env` file in the root of the project (you can use `.env.example` as a template) and add your connection string.

## 2. Install MongoDB Atlas CLI (mongosh)

One of the setup scripts relies on the MongoDB Shell (`mongosh`). You can find installation instructions for your specific operating system in the [official MongoDB documentation](https://www.mongodb.com/docs/mongodb-shell/install/).

## 3. Install Pipenv

If you don't have Pipenv installed, you can install it globally via pip:

```bash
pip install --user pipenv
```

## 4. Install Project Dependencies

Install all the required dependencies using Pipenv:

```bash
pipenv install
```

Then, activate the virtual environment:

```bash
pipenv shell
```

## 5. Run the Setup Script

Execute the main setup script to initialize your databases (make sure your `.env` is configured correctly first with Postgres and MongoDB variables):

```bash
pipenv run setup-all
```

## 6. Test Database Connections

You can test the connections and ensure data is loaded into both PostgreSQL and MongoDB using the provided query scripts:

```bash
pipenv run query-postgres
pipenv run query-mongo
```

## 7. Start the Project

Finally, start the FastAPI development server:

```bash
pipenv run start
```

The server will start running (usually at `http://127.0.0.1:8000`) and reload on code changes.

## 8. Access API Documentation

Once the server is running, FastAPI automatically generates interactive documentation for your API endpoints. You can access it at:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

You can use the Swagger UI to view all available endpoints and test them (like the `/api/predict/` endpoint) directly from your browser.
