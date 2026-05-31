#Secure Multi-Container Web Architecture

A secure, containerized mini-backend system designed with DevOps and security best practices. This project demonstrates a production-ready infrastructure layout isolating a web framework behind an Nginx reverse proxy.

#Architecture Overview

User --> Nginx (Port 80) --> [Private Docker Network] --> Flask App (Port 5000) --> SQLite

#Security Implementation

**Reverse Proxy Shielding:** The Flask application backend is completely hidden from the public internet. All outside traffic must negotiate with Nginx.

**Cryptographic Password Hashing:** User passwords are secured using 'scrypt' hashing via Werkzeug before storage.

**HTTP Hardening Headers:** Nginx is explicitly configured to inject defensive security headers:
	*'X-Frame-Options: DENY' (Anti-Clickjacking)
	*'X-Content-Type-Options: nosniff' (MIME-sniffing protection)
	*'Content-Security-Policy' (Mitigates XSS risks)

**Runtime Secret Injection:** No application secrets or database strings are hardcoded. All configurations use environment variables injected at runtime via Docker Compose.

#How to Run
1. Clone the repository
2. Run 'docker compose up --build'
3. Access the web application at 'http://localhost'
