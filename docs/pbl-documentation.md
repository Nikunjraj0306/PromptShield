# PromptShield — Project-Based Learning (PBL) Documentation

## 1. Introduction

Project-Based Learning (PBL) is an educational approach in which students acquire knowledge and practical skills by working on a real-world problem and developing a solution.

PromptShield was developed using this approach. The project applies software development, application security, database management and cloud computing concepts to create a working application security gateway prototype.

## 2. Problem Identification

Modern web applications receive user input through different interfaces and APIs. Some requests may contain malicious patterns intended to exploit application vulnerabilities.

Examples include:

- SQL Injection
- Cross-Site Scripting (XSS)
- Path Traversal
- Command Injection
- Prompt Injection
- Sensitive Data Exposure

The project addresses the problem of identifying suspicious request content and evaluating its potential security risk through a centralized inspection application.

## 3. Project Objectives

The project aims to:

1. Understand common application-layer security threats.
2. Design a system capable of inspecting submitted request content.
3. Implement rule-based detection mechanisms.
4. Develop a risk-scoring and decision-making mechanism.
5. Integrate user authentication and authorization.
6. Store security events in a relational database.
7. Develop a dashboard for monitoring inspection results.
8. Deploy the application using cloud services.
9. Demonstrate practical implementation of concepts from four academic subjects.

## 4. Project Planning

The project was divided into the following development phases.

| Phase | Activities |
|---|---|
| Phase 1: Problem identification | Identify application security challenges and define project objectives |
| Phase 2: Requirement analysis | Identify functional and non-functional requirements |
| Phase 3: System design | Design application architecture, database entities and API structure |
| Phase 4: Backend development | Develop FastAPI services, authentication and detection logic |
| Phase 5: Frontend development | Develop React dashboard and user interfaces |
| Phase 6: Database integration | Create Azure SQL tables, relationships and seed data |
| Phase 7: Testing | Test authentication, detection, risk scoring and application functionality |
| Phase 8: Deployment | Deploy frontend, backend and database using cloud platforms |

## 5. Development Methodology

An iterative development approach was followed.

The application was developed in smaller modules. Each module was implemented and tested before integrating it with the remaining components.

The major development activities included:

### 5.1 Backend Development

Python FastAPI was used to implement:

- Authentication endpoints.
- JWT token validation.
- Role-based authorization.
- Request-inspection APIs.
- Rule-based threat detection.
- Risk-scoring and decision logic.
- Analytics and security-event APIs.

### 5.2 Frontend Development

React and TypeScript were used to create:

- Login interface.
- Dashboard overview.
- Request Inspector.
- Security Events page.
- Settings page.
- Role-aware navigation and access interfaces.

### 5.3 Database Development

Microsoft Azure SQL Database was used for persistent storage.

The database implementation includes eight main entities:

- Users
- Applications
- Endpoints
- DetectionRules
- SecurityPolicies
- SecurityEvents
- ThreatFindings
- AuditLogs

### 5.4 Cloud Deployment

The application was deployed using:

- Vercel for frontend hosting.
- Render for backend hosting.
- Microsoft Azure SQL Database for data storage.

Deployment involved configuring environment variables, API communication, CORS restrictions and Azure SQL firewall rules.

## 6. Testing and Validation

Testing was conducted to verify the functionality of the application.

The following scenarios were evaluated:

| Test scenario | Expected result |
|---|---|
| Normal request | ALLOW |
| SQL injection pattern | Detect suspicious pattern |
| XSS pattern | Detect suspicious pattern |
| Path traversal pattern | Detect suspicious pattern |
| Prompt injection pattern | Detect suspicious pattern |
| Command injection (`rm -rf /`) | BLOCK |
| Multiple suspicious patterns | High risk score and BLOCK |
| Unauthorized access | Reject protected API request |
| Valid login | Authenticate user |
| Invalid login | Reject authentication |

Automated backend tests were also executed using pytest.

The backend test suite completed successfully with 25 passing tests during the development process.

The frontend production build was also verified successfully.

The deployed application was subsequently tested through its public interface.

## 7. Challenges Encountered and Solutions

### 7.1 Database Connectivity

**Challenge:** The backend initially encountered database connectivity problems during cloud deployment.

**Solution:** Configured Azure SQL connection settings, installed the required Microsoft ODBC Driver 18 and corrected the Azure SQL firewall configuration.

### 7.2 Cross-Origin Resource Sharing

**Challenge:** The browser initially blocked communication between the Vercel frontend and Render backend because the frontend origin was not permitted.

**Solution:** Configured the backend CORS allowed-origin settings with the deployed frontend domains.

### 7.3 Cloud Database Firewall

**Challenge:** Azure SQL rejected connections from the Render outbound IP address.

**Solution:** Added the observed Render IP address to the Azure SQL firewall rules.

### 7.4 Threat Detection Accuracy

**Challenge:** Initial detection rules did not identify every test pattern, including certain command-injection examples.

**Solution:** Improved the detection patterns and added regression tests to verify the expected behavior.

## 8. Learning Outcomes

Through this project, the following practical skills were developed:

- Designing a multi-tier software architecture.
- Developing REST APIs using FastAPI.
- Building frontend applications using React and TypeScript.
- Implementing authentication and role-based authorization.
- Understanding application-layer security threats.
- Designing relational databases and SQL relationships.
- Integrating a cloud-hosted backend with Azure SQL Database.
- Deploying applications using cloud platforms.
- Debugging deployment and network connectivity issues.
- Testing application functionality and maintaining code through GitHub.

## 9. Project Demonstration

PromptShield provides a working web interface through which users can:

1. Authenticate using their assigned account.
2. View dashboard analytics.
3. Submit request content for inspection.
4. Review Allow or Block decisions.
5. View detected security findings and risk scores.
6. Monitor recorded security events.

The application is publicly deployed, allowing the project to be demonstrated through its hosted interface.

## 10. Future Enhancements

Possible future improvements include:

- Automatic traffic interception through a reverse proxy.
- Integration with real application traffic.
- Advanced threat-detection mechanisms.
- Distributed rate limiting.
- Stable cloud networking.
- More advanced monitoring and alerting.
- Expanded policy-management functionality.

## 11. Conclusion

The PromptShield project demonstrates the practical application of Project-Based Learning through the identification of a real-world application security problem and the development of a working cloud-hosted solution.

It provided practical experience in planning, designing, developing, testing, debugging and deploying a software application while integrating concepts from System Design, Cloud Security and Database Management Systems.