# PromptShield — Cloud-Native Application Security Gateway

## 1. Project Abstract

PromptShield is a cloud-native application security gateway prototype developed to demonstrate how application-layer security threats can be identified and evaluated using rule-based detection techniques.

The application analyzes submitted request content for suspicious patterns associated with SQL injection, Cross-Site Scripting (XSS), path traversal, command injection, prompt injection, and selected sensitive-data exposure.

A risk-scoring mechanism assigns weights to detected security findings. The resulting score is capped at 100. Requests are blocked when a critical finding is detected or when the risk score reaches the configured threshold. Otherwise, the request is allowed according to the implemented decision logic.

PromptShield provides a web-based dashboard for authentication, request inspection, security-event monitoring, and analytics. It uses React and TypeScript for the frontend, Python FastAPI for the backend, and Azure SQL Database for persistent storage.

The application is deployed using Vercel, Render, and Microsoft Azure SQL Database.

## 2. Problem Statement

Web applications receive user input that may contain malicious or suspicious content. Common application-layer threats include SQL injection, Cross-Site Scripting, path traversal, command injection, and attempts to manipulate AI-based systems through prompt injection.

Developers need ways to identify suspicious request content, assess its potential risk, and maintain records of security-related activity.

PromptShield addresses this problem by providing a centralized request-inspection prototype that applies predefined detection rules, calculates risk scores, produces Allow or Block decisions, and records security events for review.

## 3. Project Objectives

The main objectives are:

1. Develop a web-based application security gateway prototype.
2. Implement rule-based detection for selected application-layer threats.
3. Calculate risk scores using configurable detection-rule weights.
4. Apply Allow and Block decisions based on risk scores and critical findings.
5. Implement secure user authentication using password hashing and JWT access tokens.
6. Apply role-based access control to protected application features.
7. Store security events and related findings in a relational database.
8. Provide a dashboard for request inspection, analytics, and security-event monitoring.
9. Deploy the application using cloud hosting services.
10. Demonstrate concepts from System Design, Project-Based Learning, Cloud Security, and Database Management Systems.

## 4. Project Scope

### Included in the MVP

- User login and authentication.
- Role-based access for Admin, Analyst, and Viewer users.
- Request inspection through the PromptShield API.
- Rule-based detection of selected security patterns.
- Risk scoring and Allow/Block decisions.
- Security-event and threat-finding storage.
- Dashboard analytics and event viewing.
- Login-attempt rate limiting.
- Cloud deployment of the frontend, backend, and database.

### Outside the Current MVP Scope

- Automatic interception of all application traffic.
- A fully functioning reverse-proxy or inline Web Application Firewall.
- Forwarding to arbitrary user-provided URLs.
- Distributed rate limiting across multiple backend instances.
- Comprehensive machine-learning-based threat detection.
- Production-grade protection against every application-layer attack.

## 5. Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React, TypeScript |
| Backend | Python, FastAPI |
| Database | Microsoft Azure SQL Database |
| Database connectivity | pyodbc, ODBC Driver 18 |
| Authentication | Password hashing, JWT |
| Frontend hosting | Vercel |
| Backend hosting | Render |
| Version control | Git and GitHub |
| API testing | FastAPI Swagger UI and automated tests |

## 6. Deployment Overview

PromptShield uses a three-tier deployment arrangement:

1. **Presentation layer:** The React frontend is hosted on Vercel.
2. **Application layer:** The FastAPI backend is hosted on Render.
3. **Data layer:** Azure SQL Database stores users, application configuration, detection rules, security events, threat findings, and audit records.

The frontend communicates with the backend through HTTPS-based API requests. The backend connects to Azure SQL Database using configured environment variables and database firewall restrictions.

## 7. Expected Outcomes

The completed MVP demonstrates:

- Detection of selected suspicious request patterns.
- Risk-based security decisions.
- Authenticated and role-restricted dashboard access.
- Persistent storage of inspection results.
- Visualization of security events and analytics.
- Successful deployment of a multi-tier cloud application.

## 8. Project Limitations

PromptShield uses rule-based heuristics. Therefore, it may produce false positives and false negatives and cannot guarantee detection of every attack.

The current deployment uses a free Render hosting plan, whose outbound IP address is not guaranteed to remain static. Azure SQL firewall configuration may require updating if the backend's outbound IP changes.

PromptShield is an academic prototype and should not be considered a replacement for a production Web Application Firewall or secure application development practices.

## 9. Conclusion

PromptShield demonstrates the design, development, database integration, security evaluation, and cloud deployment of an application security gateway prototype. It brings together concepts from System Design, Project-Based Learning, Cloud Security, and DBMS in one working application.