# Healthcare Scheduling Frontend

This is the frontend for the Healthcare Scheduling application, built with React, TypeScript, and Vite.

## Features

- **Patient Management**: View, create, edit, and delete patient records
- **Scheduling**: AI-powered scheduling of medical procedures
- **Appointments**: View and manage appointments
- **PWA Support**: Progressive Web App capabilities for offline access
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **React**: JavaScript library for building user interfaces
- **TypeScript**: Typed superset of JavaScript
- **Vite**: Next-generation frontend tooling
- **React Query**: Data fetching and caching library
- **React Router**: Routing library for React
- **Axios**: Promise-based HTTP client
- **PWA**: Progressive Web App capabilities

## Getting Started

### Prerequisites

- Node.js 18 or higher
- npm or yarn

### Installation

1. Install dependencies:
   ```
   npm install
   # or if you use yarn
   # yarn install
   ```

### Development

1. Start the development server:
   ```
   npm run dev
   # or if you use yarn
   # yarn dev
   ```
2. Open your browser and navigate to `http://localhost:5173`

### Building for Production

1. Build the application:
   ```
   npm run build
   # or if you use yarn
   # yarn build
   ```
2. The built files will be in the `dist` directory, which can be served by any static file server.

## Project Structure

- `src/`: Source code
  - `api/`: API client and related utilities
  - `components/`: Reusable UI components
  - `pages/`: Page components
  - `App.tsx`: Main application component
  - `main.tsx`: Entry point

## Backend Integration

This frontend is designed to work with the FastAPI backend. The API client is configured to communicate with the backend at `/api`, which is proxied to the backend server in development mode.

To test the connection to the backend, use the API Test component on the home page.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Submit a pull request