#!/bin/sh

# Perform database migrations
flask db migrate
flask db upgrade

# Start the Flask application
flask run 
