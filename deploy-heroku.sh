#!/bin/bash

# Script to deploy the Healthcare Scheduling API to Heroku

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "Heroku CLI is not installed. Please install it first:"
    echo "https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if user is logged in to Heroku
heroku whoami &> /dev/null
if [ $? -ne 0 ]; then
    echo "You are not logged in to Heroku. Please login first:"
    heroku login
fi

# Ask for app name
read -p "Enter a name for your Heroku app (leave blank for random name): " APP_NAME

# Create Heroku app
if [ -z "$APP_NAME" ]; then
    echo "Creating Heroku app with random name..."
    heroku create
    APP_NAME=$(heroku apps:info | grep "=== " | cut -d' ' -f2)
else
    echo "Creating Heroku app: $APP_NAME..."
    heroku create $APP_NAME
fi

# Add PostgreSQL addon
echo "Adding PostgreSQL addon..."
heroku addons:create heroku-postgresql:mini --app $APP_NAME

# Deploy to Heroku
echo "Deploying to Heroku..."
git add .
git commit -m "Prepare for Heroku deployment" --allow-empty
git push heroku main

# Initialize the database
echo "Initializing the database..."
heroku run python -c "from database.database import init_db; init_db()" --app $APP_NAME

# Ask if user wants to seed the database
read -p "Do you want to seed the database with sample data? (y/n): " SEED_DB
if [ "$SEED_DB" = "y" ] || [ "$SEED_DB" = "Y" ]; then
    echo "Seeding the database..."
    heroku run "curl -X POST https://$APP_NAME.herokuapp.com/seed-database?patient_count=50&resource_count=10&days_ahead=30" --app $APP_NAME
fi

# Open the app
echo "Opening the app..."
heroku open --app $APP_NAME

echo "Deployment complete! Your app is running at: https://$APP_NAME.herokuapp.com"
echo "API documentation is available at: https://$APP_NAME.herokuapp.com/docs"