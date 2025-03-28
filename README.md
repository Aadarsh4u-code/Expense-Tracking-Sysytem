# Expense Management System

This project is an expense management system that consists of a Streamlit frontend application and a FastAPI backend server connected with MySql Database.


# Screenshot of UI

Dashboard For Expenses
![HomepageUI](./screenshot/Expense%20Tracking%20System%20Dashboard%20-1.png)
![HomepageUI](./screenshot/Expense%20Tracking%20System%20Dashboard%20-2.png)
![HomepageUI](./screenshot/Expense%20Tracking%20System%20Dashboard%20-3.png)

Expenses List and Delete
![HomepageUI](./screenshot/Expenses%20List:%20Delete.png)

Add Expenses
![HomepageUI](./screenshot/Add%20Expenses.png)

Update Expenses
![HomepageUI](./screenshot/Update%20Expenses.png)

PostMan API Test
![HomepageUI](./screenshot/GET%20expense%20between%20date%20range.png)
![HomepageUI](./screenshot/Delete%20expense%20.png)
![HomepageUI](./screenshot/postman-%20POST%20request.png)



## Project Structure

- **frontend/**: Contains the Streamlit application code.
- **backend/**: Contains the FastAPI backend server code.
- **tests/**: Contains the test cases for both frontend and backend.
- **logger/**: Contains the logging code for both frontend and backend.
- **logs/**: Contains the log file based on data versioning control.
- **exception/**: Contains the exception handling for both frontend and backend.
- **requirements.txt**: Lists the required Python packages.
- **README.md**: Provides an overview and instructions for the project.


## How to run?
```bash
conda create -n exp_venv python=3.12 -y
```
```bash
conda activate exp_venv
```

```bash
pip install -r requirements.txt
```

#### Insert all install packages with its version at requirement.txt

```bash
pip list
pip freeze > requirements.txt
```


## Pydantic
- Data validation and parsing using Python type hints.

- ***Use Case: Ensures clean and structured input data for ML models.***

## FastApi
- High-performance web framework for building APIs.
- ***Use Case: Deploys ML models as REST APIs for real-time inference.***

```bash
cd expense_tracking/backend
uvicorn expense_api:app --reload
```
## Database Interaction
- Handling structured data storage and retrieval.

-***Use Case: Stores and queries preprocessed datasets in MySql***

## Pytest
- Framework for unit and integration testing in Python.

-***Use Case: Automates testing of data preprocessing pipelines.***

## API call with Requests
- Fetching data from external sources like database via HTTP.

-***Use Case: Create, Read, Update, Delete Operation***

## Logging
- Tracks events and errors in applications.

-***Use Case: Logs data pipeline failures for debugging in production.***

## Context Manager
- Manages resources efficiently using with statements.

-***Use Case: Handles file I/O operations during large dataset processing.***


## Streamlit
- IU Framework for building interactive data apps.

-***Use Case: Creates dashboards for visualizing model predictions.***

```bash
cd expense_tracking/frontend
streamlit run app.py
```

