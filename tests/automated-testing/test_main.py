import json
import pytest
from httpx import AsyncClient

from main import app

# Get GraphQL Operations
with open('client/main.graphql', 'r') as f:
    GRAPHQL = f.read()

# Create Client
async def client(operationName: str, variables: dict | None = None):
    """Create Client"""
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        the_query = {"query": GRAPHQL, "operationName": operationName}
        if variables:
            the_query["variables"] = variables
        response = await ac.post("/graphql", json=the_query)
    return response

def check_output(expected, actual):
    """Check Output"""
    return json.dumps(actual, sort_keys = True, indent=0) == json.dumps(expected, sort_keys = True, indent=0)

@pytest.mark.asyncio
async def test_all_tasks():

    # API Request
    response = await client("AllTasks")

    # Expected Output
    expected_output = {'data': {'search': {'edges': [
        {
          "node": {
            "id": "Mjo6M2VmOWFiYmI1ZGY1YjY0MQ==",
            "title": "Post Tutorial",
            "description": "post the example app.",
            "status": "open"
          }
        },
        {
          "node": {
            "id": "MTo6YTU1ZTUzMmVhYjAyOGI0Mg==",
            "title": "First App",
            "description": "create an example app.",
            "status": "close"
          }
        }
    ]}}}
    
    # Assert
    assert response.status_code == 200
    assert check_output(response.json(), expected_output)
    

@pytest.mark.asyncio
async def test_search():

    # API Request
    variables = {"status": "open"}
    response = await client("SearchTask", variables)

    # Expected Output
    expected_output = {'data': {'search': {'edges': [
        {
            "node": {
            "id": "Mjo6M2VmOWFiYmI1ZGY1YjY0MQ==",
            "title": "Post Tutorial",
            "description": "post the example app.",
            "status": "open"
            }
        },
    ]}}}

    # Assert
    assert response.status_code == 200
    assert check_output(response.json(), expected_output)
    