# Flask Todo App

## Overview

This is a Flask Todo App - a simple web application for managing todo items with user authentication.

## Key Features

- User registration and login system
- Create, read, and delete todo items
- User-specific todo lists (each user sees only their own todos)

## Tech Stack

- Backend: Flask with SQLAlchemy ORM
- Database: PostgreSQL
- Authentication: Flask-Login
- Frontend: Bootstrap 5 with Jinja2 templates
- Package Management: uv (modern Python package manager)

## Architecture

- Uses Flask application factory pattern in `todo/__init__.py`
- Blueprint-based routing (`auth.py` for authentication, `views.py` for todo operations)
- Two main models: `User` and `Todo` with foreign key relationship
- Instance-based configuration for database credentials

## Setup

Requires Python 3.13, PostgreSQL, and uses `uv` for dependency management. The app runs via `flask run` command.
