# PromptShield — Frontend

## 1. Overview

The PromptShield frontend is a web-based dashboard developed using React and TypeScript.

It provides the user interface for authentication, request inspection, analytics, security-event monitoring and application settings.

The frontend communicates with the PromptShield FastAPI backend through REST API requests.

## 2. Technologies Used

- React
- TypeScript
- Vite
- HTML and CSS
- JavaScript
- Fetch API for backend communication

## 3. Main Features

### Login

Allows registered users to authenticate using their email address and password.

### Dashboard Overview

Displays security analytics and an overview of recorded inspection activity.

### Request Inspector

Allows authorized users to submit request content for security inspection and view the resulting decision, risk score and findings.

### Security Events

Displays recorded inspection events and their associated security information.

### Settings

Provides access to the application's settings interface.

### Role-Based Interface

The navigation and available operations reflect the authenticated user's assigned role. Backend authorization remains responsible for enforcing access permissions.

## 4. Project Structure

```text
frontend/
|
|-- public/
|
|-- src/
|   |-- App.tsx
|   |-- Login.tsx
|   |-- api.ts
|   |-- main.tsx
|   |-- components/
|   |-- assets/
|
|-- index.html
|-- package.json
|-- package-lock.json
|-- vite.config.ts
|-- tsconfig.json
|-- .env.example
|-- README.md
```

The structure above describes the main frontend files and may be extended as additional components are added.

## 5. Installation

### Prerequisites

- Node.js
- npm
- Access to the PromptShield backend API

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

## 6. Environment Configuration

Create a local `.env` file using `.env.example` as a reference.

Configure the backend base URL:

```env
VITE_API_URL=http://127.0.0.1:8000
```

For deployment, configure the corresponding deployed backend base URL.

The Vite environment variable prefix `VITE_` means the value is exposed to frontend code. Never place passwords, JWT secrets or database credentials in frontend environment variables.

## 7. Run Development Server

Start the Vite development server:

```bash
npm run dev
```

The frontend is generally available at:

```text
http://localhost:5173
```

## 8. Production Build

Create a production build:

```bash
npm run build
```

Vite generates the production output in the `dist/` directory.

## 9. Backend Integration

The frontend communicates with the FastAPI backend using the configured API base URL.

The backend provides authentication, inspection, analytics and security-event endpoints.

Authentication tokens are attached to protected API requests according to the frontend API implementation.

## 10. Deployment

The PromptShield frontend is deployed using Vercel.

The deployed frontend communicates with the Render-hosted FastAPI backend through HTTPS.

The backend must allow the deployed frontend origin through its CORS configuration.

## 11. Conclusion

The PromptShield frontend provides an interactive interface for application security inspection and monitoring. It integrates with the backend API to present authentication, risk evaluation and security-event information.