# Deed Real Estate Platform

Deed is a production-ready real estate web platform built with FastAPI, PostgreSQL, SQLAlchemy, Jinja2, and deployed on Ubuntu VPS using Nginx and Gunicorn.

## Project Overview

This project is designed for a real estate company to showcase projects, project details, banners, awards, business information, and customer-facing content through a fast and scalable web application.

## Key Features

* FastAPI backend
* PostgreSQL database
* SQLAlchemy ORM
* Jinja2 server-side templates
* Dynamic project listing
* Project detail pages
* Banner and award display
* Static image and media handling
* Contact and information pages
* Production deployment on Ubuntu VPS
* Nginx reverse proxy
* Gunicorn + Uvicorn workers
* SSL-enabled domain deployment

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Jinja2
* HTML
* CSS
* JavaScript
* Nginx
* Gunicorn
* Uvicorn
* Ubuntu VPS

## Production Deployment

The application is deployed on a Linux VPS using this architecture:

```text
Nginx → Gunicorn → Uvicorn → FastAPI → PostgreSQL
```

## Local Setup

```bash
git clone https://github.com/anisjkb/deed.git
cd deed

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/deeddb
SECRET_KEY=your-secret-key
```

Run the application:

```bash
uvicorn src.backend.app:app --reload
```

Visit:

[https://deedpl.com/]

## Suggested Screenshots

Add screenshots here:

```text
docs/screenshots/homepage.png
docs/screenshots/projects.png
docs/screenshots/project-detail.png
```

## Future Improvements

* API documentation page
* Docker support
* Automated testing
* CI/CD pipeline
* Advanced search and filtering
* Performance monitoring

## Author

Developed by [Anis](https://github.com/anisjkb)
