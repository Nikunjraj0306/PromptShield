# PromptShield — Cloud-Native Application Security Gateway

![Project Status](https://img.shields.io/badge/Status-Deployed-success)
![Frontend](https://img.shields.io/badge/Frontend-React%20%7C%20TypeScript-blue)
![Backend](https://img.shields.io/badge/Backend-FastAPI-green)
![Database](https://img.shields.io/badge/Database-Azure%20SQL-blue)

## 1. Project Overview

PromptShield is a cloud-native application security gateway prototype designed to identify suspicious request patterns, evaluate security risks and make Allow or Block decisions.

The project demonstrates the practical implementation of application security, authentication, database management, system architecture and cloud deployment.

It was developed as an academic project integrating concepts from:

- System Design
- Project-Based Learning (PBL)
- Cloud Security
- Database Management Systems (DBMS)

## 2. Live Application

**Frontend:** https://promptshield-eta-roan.vercel.app

**Backend:** https://promptshield-api-jw6d.onrender.com

**API Documentation:** https://promptshield-api-jw6d.onrender.com/docs

The backend is hosted on Render, the frontend on Vercel and the database on Microsoft Azure SQL Database.

Note: The Render Free service may take some time to respond after periods of inactivity.

## 3. Key Features

- User authentication using email and password.
- JWT-based authentication.
- Role-based access control.
- Request inspection through a web dashboard.
- Rule-based detection of selected application-layer threats.
- Risk scoring and Allow/Block decisions.
- Security-event recording.
- Dashboard analytics.
- Login-attempt rate limiting.
- Cloud-hosted relational database.

## 4. Security Threat Categories

PromptShield includes rule-based detection for:

1. SQL Injection
2. Cross-Site Scripting (XSS)
3. Path Traversal
4. Command Injection
5. Prompt Injection
6. Sensitive Data Exposure

The detection engine evaluates submitted text against enabled rules and generates security findings.

## 5. Risk Scoring Mechanism

Each detection rule has an associated risk weight and severity.

The overall risk score is capped at 100.

The decision mechanism follows these rules:

- A critical finding results in a Block decision.
- A score equal to or greater than the configured risk threshold results in a Block decision.
- Otherwise, the request is allowed.

The default risk threshold is 50.

## 6. Technology Stack

| Component | Technology |
|---|---|
| Frontend | React |
| Programming language | TypeScript |
| Backend | Python |
| API framework | FastAPI |
| Database | Microsoft Azure SQL Database |
| Database connectivity | pyodbc |
| Authentication | JWT |
| Frontend hosting | Vercel |
| Backend hosting | Render |
| Version control | Git and GitHub |

## 7. System Architecture

PromptShield follows a three-tier architecture.

```text
             USER / BROWSER
                    |
                    v
        REACT + TYPESCRIPT FRONTEND
                 (VERCEL)
                    |
                 HTTPS
                    |
                    v
             FASTAPI BACKEND
                 (RENDER)
                    |
          +---------+----------+
          |         |          |
          v         v          v
      AUTH/RBAC  DETECTION  RISK EVALUATION
          |         |          |
          +---------+----------+
                    |
                    v
           AZURE SQL DATABASE
             (PERSISTENCE)
```

The frontend communicates with the backend through REST APIs. The backend processes requests and interacts with Azure SQL Database for persistent storage.

## 8. User Roles

| Role | Access |
|---|---|
| Admin | Administrative access |
| Analyst | Request inspection, analytics and security events |
| Viewer | Read-only analytics and security events |

The backend enforces authorization for protected operations.

## 9. Database Design

PromptShield uses a relational database containing eight main tables:

1. Users
2. Applications
3. Endpoints
4. DetectionRules
5. SecurityPolicies
6. SecurityEvents
7. ThreatFindings
8. AuditLogs

The database uses primary keys, foreign keys, constraints and indexes to maintain data integrity.

## 10. Project Structure

```text
PromptShield/
|
|-- backend/
|   |-- app/
|   |-- tests/
|   |-- requirements.txt
|   |-- Dockerfile
|   |-- startup.txt
|   |-- .env.example
|
|-- frontend/
|   |-- src/
|   |-- public/
|   |-- package.json
|   |-- .env.example
|
|-- database/
|   |-- 001_initial_schema.sql
|   |-- migrations and seed scripts
|
|-- docs/
|   |-- project-overview.md
|   |-- requirements.md
|   |-- architecture.md
|   |-- pbl-documentation.md
|   |-- cloud-security.md
|   |-- dbms-documentation.md
|   |-- database-schema.md
|   |-- er-diagram.md
|   |-- er-diagram.mmd
|   |-- threat-model.md
|
|-- README.md
```

## 11. Local Setup

### Prerequisites

- Python 3.11 or a compatible supported Python version.
- Node.js and npm.
- Microsoft ODBC Driver 18 for SQL Server.
- Access to a configured SQL Server or Azure SQL Database.

### Backend Setup

Open a terminal in the project directory.

```bash
cd backend
python -m venv venv
```

Activate the virtual environment.

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` file using `.env.example` as a reference and configure the required database and JWT settings.

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend API documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
```

Create a local `.env` file using `.env.example` as a reference.

Set `VITE_API_URL` to the backend base URL, for example:

```env
VITE_API_URL=http://127.0.0.1:8000
```

Start the frontend:

```bash
npm run dev
```

The frontend is available at:

```text
http://localhost:5173
```

## 12. Testing

The backend uses pytest for automated testing.

Run the backend test suite:

```bash
cd backend
python -m pytest -v
```

The development test suite previously completed with 25 passing tests.

Build the frontend:

```bash
cd frontend
npm run build
```

Manual testing includes normal request inspection, suspicious input detection, risk-based decisions, authentication and security-event viewing.

## 13. Documentation

Additional project documentation is available in the `docs/` directory.

| Document | Description |
|---|---|
| project-overview.md | Project introduction, objectives and scope |
| requirements.md | Functional and non-functional requirements |
| architecture.md | System architecture and component design |
| pbl-documentation.md | Project planning and development process |
| cloud-security.md | Cloud deployment and security controls |
| dbms-documentation.md | DBMS concepts and implementation |
| database-schema.md | Implemented database schema |
| er-diagram.md | Entity relationship explanation |
| er-diagram.mmd | Mermaid ER diagram source |
| threat-model.md | Security threats and mitigations |

## 14. Academic Subject Mapping

| Subject | Concepts demonstrated |
|---|---|
| System Design | Three-tier architecture, modular design, REST APIs and data flow |
| PBL | Problem identification, planning, implementation, testing and deployment |
| Cloud Security | JWT, RBAC, CORS, database firewall and cloud deployment |
| DBMS | Relational modelling, keys, relationships, constraints and indexing |

## 15. Limitations

PromptShield is an academic prototype using rule-based detection.

It is not a complete reverse-proxy-based Web Application Firewall and does not automatically intercept all traffic to external applications.

Its detection rules may produce false positives and false negatives. The login rate limiter is in-memory and is not distributed across backend instances.

The current Render Free deployment does not guarantee a permanent outbound IP address.

## 16. Future Enhancements

- Automatic traffic interception through a reverse proxy.
- More advanced threat detection.
- Distributed rate limiting.
- Stable cloud networking.
- Centralized security monitoring.
- Enhanced policy-management capabilities.
- Additional security testing.

## 17. Conclusion

PromptShield demonstrates how application security, system design, relational database management and cloud computing can be integrated into a working software application.

The project provides practical experience in developing, testing and deploying a cloud-hosted application security gateway prototype.