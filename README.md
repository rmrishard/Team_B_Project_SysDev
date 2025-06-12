<h1>Yalla Habibi</h1>


<h2>All in one Lebanese shopping experience in Montreal.</h2>

Built with FastAPI backend and a static frontend served by Nginx, fully containerized using Docker Compose for easy local development and deployment.

________________________________________

<h3>Table of Contents</h3>

* 	[Project Overview](#project-overview)
* 	[Components](#components)
* 	[System Flow](#system-flow)
* 	[Setup & Running](#setup--running)
* 	[Backend Structure](#backend-structure)
* 	[Frontend Structure](#frontend-structure)
* 	[CI/CD](#cicd)
* 	Key Points / Summary
________________________________________

<h4 id="project-overview">Project Overview</h4>

Yalla Habibi is a small full-stack web application featuring:
* 	A **FastAPI** backend serving REST APIs for products, suppliers, orders, users, product reviews, and more, with a **PostgreSQL** database.
* 	A static **frontend** built with HTML, CSS , and JavaScript.
* 	A **Nginx** server serving frontend assets and acting as a reverse proxy forwarding API requests to the backend.
* 	Fully containerized with **Docker Compose** to simplify local development and deployment.
* 	Automated deployment via GitHub Actions.
________________________________________

<h4 id="components">Components</h4>

| Service    | Description                                      | Notes                                           |
|------------|--------------------------------------------------|-------------------------------------------------|
| postgres   | PostgreSQL database storing all app data         | Credentials provided through Docker secrets     |
| backend    | FastAPI application    | Reads config from .env and secrets              |
| web        | Nginx serving static files and  /api/v1/ to backend | Serves front-end assets and API requests |


<h4 id="system-flow">System Flow</h4>

* Static content is served directly by Nginx.
* API requests are exchanged by Nginx to the FastAPI backend.
* Backend communicates with the PostgreSQL database


<h4 id="setup--running">Setup & Running</h4>

Prerequisites
* Docker Desktop installed and running.
* Initial Setup
1.	Create the following secret files inside the secrets/ directory:
* pg_user.txt – contains your PostgreSQL username.
* pg_pw.txt – contains your PostgreSQL password.

2.	From the project root directory, run:
* bash
* Copy
* docker compose up

3.	Access the application:
* Frontend web pages at: http://localhost:8777
* API endpoints at: http://51.222.106.12:8777/api/v1/documentation# 


<h4 id="backend-structure">Backend Structure</h4>

<h4 id="frontend-structure">Frontend Structure</h4>

* HTML, CSS and JS are in the frontend/Web
* Bootstrap for responsive design
* Custom CSS and JavScript to handle features

<h4 id="cicd">CI / CD</h4>

*	GitHub Actions workflow located at .github/workflows/deploy.yml.
*	Automatically deploys the updated stack to a VPS on every push to the main branch.
*	Uses SSH to run Docker commands remotely on the server.
