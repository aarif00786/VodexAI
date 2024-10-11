# VodexAI

## Project Overview
This project is a web application built using FastAPI and MongoDB, designed to manage Items and User Clock-In Records. The application provides a set of RESTful APIs that allow users to perform CRUD (Create, Read, Update, Delete) operations on these entities. and app deployed in production using render.

## deployment swagger doc link

https://vodexai.onrender.com/docs

## project setup

# FastAPI Application

This project is built using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python 3.8+.


## Requirements

Python 3.8+ installed on your machine
Virtual Environment Tool (venv)
Uvicorn for running the FastAPI app

## Project Setup

Follow these instructions to set up and run the application locally.

## Clone the Repository

Start by cloning the repository to your local machine:
git clone https://github.com/aarif00786/VodexAI

## Create and Activate a Virtual Environment
It is recommended to create a virtual environment before installing the project's dependencies.

# Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# Windows:
python -m venv venv
.\venv\Scripts\activate

## Install the Dependencies

pip install -r requirements.txt

## Run the Application

You can now start the FastAPI application using Uvicorn:
uvicorn main:app --reload

## Access the API Documentation
FastAPI automatically generates interactive API documentation for you. You can view the following:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc


## API EXPLANATIONS
## Items API:

## POST /item/create/: Create a new item with the following input:
Input:
Name
Email
Item Name
Quantity
Expiry Date (YYYY-MM-DD)
The Insert Date is automatically recorded upon creation.

## GET /item/items/<id>: Retrieve an item by its unique ID.

## GET /item/filter?email=1233@yopmail.com: Filter items based on the following criteria:

Email (exact match)
Expiry Date (filter items expiring after the provided date)
Insert Date (filter items inserted after the provided date)
Quantity (items with quantity greater than or equal to the provided number using a gte filter)

## DELETE /item/delete/<id>: Delete an item based on its ID.

## PUT/item/update/<id>: Update an item’s details by ID (excluding the Insert Date).

## Clock-In Records API:

## POST /record/create/: Create a new clock-in entry with the following input:

Input:
Email
Location
The Insert DateTime is automatically added during clock-in.

## GET /record/records/<id>: Retrieve a clock-in record by its unique ID.

## GET /record/filter?email=1233@yopmail.com: Filter clock-in records based on:

Email (exact match)
Location (exact match)
Insert DateTime (clock-ins after the provided date)

## DELETE /record/delete/<id>: Delete a clock-in record based on its ID.

## PUT /record/update/<id>: Update a clock-in record by ID (excluding Insert DateTime).