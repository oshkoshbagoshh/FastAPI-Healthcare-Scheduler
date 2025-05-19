# Healthcare Scheduling API

An AI-powered healthcare scheduling system for outpatient procedures.

## Overview

This application uses machine learning techniques to optimize the scheduling of outpatient procedures based on patient diagnoses, CPT codes, resource availability, and other factors. It provides a comprehensive API for managing patients, medical data, resources, and scheduling.

## Features

- **Patient Management**: Create, retrieve, update, and delete patient records
- **Medical Data Management**: Manage diagnoses (ICD-10 codes), procedures (CPT codes), and patient-specific medical data
- **Resource Management**: Manage resources like rooms and equipment, along with their availability
- **AI-Powered Scheduling**: Optimize scheduling of procedures based on various factors:
  - Procedure priority and duration
  - Patient diagnosis severity
  - Resource requirements
  - Time constraints
  - Patient preferences

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation and settings management
- **Scikit-learn**: Machine learning library for scheduling optimization
- **Faker**: Library for generating fake data for testing and demonstration

### Frontend
- **React**: JavaScript library for building user interfaces
- **TypeScript**: Typed superset of JavaScript
- **Vite**: Next-generation frontend tooling
- **React Query**: Data fetching and caching library
- **React Router**: Routing library for React
- **Axios**: Promise-based HTTP client
- **PWA**: Progressive Web App capabilities

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Poetry (for backend dependency management)
- Node.js 18 or higher
- npm or yarn (for frontend dependency management)

### Installation

1. Clone the repository
2. Install backend dependencies:
   ```
   cd /path/to/repository
   poetry install
   ```
3. Install frontend dependencies:
   ```
   cd frontend
   npm install
   # or if you use yarn
   # yarn install
   ```

### Running the Application

#### Backend

##### Option 1: Using the run script (recommended)

1. Make the script executable:
   ```
   chmod +x run.sh
   ```
2. Run the script:
   ```
   ./run.sh
   ```

The script will automatically check if the database exists, seed it if necessary, and start the server.

##### Option 2: Manual steps

1. Start the server:
   ```
   poetry run uvicorn main:app --reload
   ```
2. Seed the database with fake data (optional):
   ```
   curl -X POST "http://localhost:8000/seed-database?patient_count=50&resource_count=10&days_ahead=30"
   ```
3. Access the API documentation at `http://localhost:8000/docs`

#### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```
2. Start the development server:
   ```
   npm run dev
   # or if you use yarn
   # yarn dev
   ```
3. Access the frontend application at `http://localhost:5173`

#### Building for Production

1. Build the frontend:
   ```
   cd frontend
   npm run build
   # or if you use yarn
   # yarn build
   ```
2. The built files will be in the `frontend/dist` directory, which can be served by any static file server.

## API Documentation

The API is fully documented using OpenAPI (Swagger). You can access the interactive documentation at `/docs` when the server is running.

### Main Endpoints

#### Patients

- `GET /patients/`: List all patients
- `POST /patients/`: Create a new patient
- `GET /patients/{patient_id}`: Get a specific patient
- `PUT /patients/{patient_id}`: Update a patient
- `DELETE /patients/{patient_id}`: Delete a patient

#### Medical Data

- `GET /medical/diagnoses/`: List all diagnoses
- `POST /medical/diagnoses/`: Create a new diagnosis
- `GET /medical/cpt-codes/`: List all CPT codes
- `POST /medical/cpt-codes/`: Create a new CPT code
- `GET /medical/patient-diagnoses/`: List patient diagnoses
- `POST /medical/patient-diagnoses/`: Create a patient diagnosis
- `GET /medical/patient-procedures/`: List patient procedures
- `POST /medical/patient-procedures/`: Create a patient procedure

#### Resources

- `GET /resources/`: List all resources
- `POST /resources/`: Create a new resource
- `GET /resources/{resource_id}/time-slots/`: List time slots for a resource
- `POST /resources/{resource_id}/time-slots/`: Create a time slot for a resource

#### Scheduling

- `POST /scheduling/optimize/`: Optimize the schedule based on provided parameters
- `GET /scheduling/appointments/`: List all appointments
- `GET /scheduling/appointments/{appointment_id}`: Get a specific appointment
- `PUT /scheduling/appointments/{appointment_id}/cancel`: Cancel an appointment

## Scheduling Algorithm

The scheduling algorithm uses machine learning techniques to optimize the scheduling of procedures:

1. **Feature Engineering**: Creates rich representations of procedures and time slots
2. **Similarity Matching**: Uses cosine similarity to find the best slot for each procedure
3. **Priority-Based Scheduling**: Handles conflicts based on procedure priority
4. **Constraint Satisfaction**: Ensures all constraints (duration, resource requirements, etc.) are met

## Deployment to Heroku

Follow these steps to deploy the application to Heroku:

### Prerequisites

- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
- Heroku account
- Git repository initialized (`git init`)

### Files for Heroku Deployment

The repository includes the following files specifically for Heroku deployment:

- `Procfile`: Tells Heroku how to run the application
- `runtime.txt`: Specifies the Python version for Heroku
- `requirements.txt`: Lists all dependencies for pip installation

The database configuration in `database/database.py` automatically detects whether to use SQLite (local development) or PostgreSQL (Heroku) based on the presence of the `DATABASE_URL` environment variable.

### Deployment Steps

#### Option 1: Using the deployment script (recommended)

1. Make the script executable:
   ```bash
   chmod +x deploy-heroku.sh
   ```

2. Run the script:
   ```bash
   ./deploy-heroku.sh
   ```

The script will guide you through the entire deployment process, including:
- Creating a Heroku app
- Adding PostgreSQL
- Deploying the application
- Initializing the database
- Optionally seeding the database
- Opening the application in your browser

#### Option 2: Manual deployment

1. **Login to Heroku**

   ```bash
   heroku login
   ```

2. **Create a new Heroku app**

   ```bash
   heroku create your-app-name
   ```

   Replace `your-app-name` with a unique name for your application.

3. **Add Heroku PostgreSQL (optional but recommended for production)**

   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Configure environment variables (if needed)**

   ```bash
   heroku config:set VARIABLE_NAME=value
   ```

5. **Deploy the application**

   ```bash
   git add .
   git commit -m "Ready for Heroku deployment"
   git push heroku main
   ```

   If you're on a different branch, use:
   ```bash
   git push heroku your-branch:main
   ```

6. **Initialize the database**

   ```bash
   heroku run python -c "from database.database import init_db; init_db()"
   ```

7. **Seed the database (optional)**

   ```bash
   heroku run curl -X POST "https://your-app-name.herokuapp.com/seed-database?patient_count=50&resource_count=10&days_ahead=30"
   ```

   Or use the Heroku dashboard to make a POST request to the `/seed-database` endpoint.

8. **Open the application**

   ```bash
   heroku open
   ```

### Monitoring and Maintenance

- View logs: `heroku logs --tail`
- Restart the app: `heroku restart`
- Run a one-off dyno: `heroku run bash`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- This project was created as a demonstration of AI/ML applications in healthcare scheduling.
- The sample medical data (ICD-10 codes, CPT codes) is based on common medical conditions and procedures.
