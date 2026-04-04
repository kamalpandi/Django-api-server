# [Django Multi-App API Server](https://vibi.pythonanywhere.com/)

This repository hosts a **Django REST API server** that powers a React frontend dashboard. The project has been migrated away from HTMX to a clean API-only architecture, with Django serving JSON endpoints and all UI handled by the [React frontend](https://django-frontend-two.vercel.app/).

## Features

- **Todo API**: Task management endpoints — create, list, and delete tasks.
- **Weather API**: Real-time weather data using OpenWeatherMap, supporting single city lookup, multi-city comparison, and full advanced reports.
- **Pic to ASCII API**: Converts uploaded images into ASCII art using Pillow.
- **Pure REST Architecture**: No templates or HTMX — Django serves only JSON responses.
- **JWT Authentication**: Token-based auth using `djangorestframework-simplejwt`.
- **Modular Structure**: Each app is self-contained with its own models, views, serializers, and URLs.

## Tech Stack

- **Backend**: Django 5.2, Python 3.13
- **API**: Django REST Framework
- **Auth**: JWT via djangorestframework-simplejwt
- **Database**: SQLite (development)
- **Deployment**: PythonAnywhere
- **Frontend**: React app on Vercel (separate repo)
- **Libraries**: Pillow, django-cors-headers, django-environ

## API Endpoints

### Todo
```
GET    /todo/get_todos/
POST   /todo/create_todo/
DELETE /todo/delete_todo/<id>/
```

### Weather
```
POST /weather/one_city/
POST /weather/weather_for_cities/
POST /weather/full_report/
GET  /weather/get_cities/
GET  /weather/get_essential_reports/
GET  /weather/get_full_report/
POST /weather/save_essential_report/
POST /weather/save_full_report/
```

### Pic to ASCII
```
POST /pic_to_ASCII/convert/
```

## Project Structure
```
Django-api-server/
├── todo/                  # Todo API app
│   ├── models.py
│   ├── views.py           # DRF API views
│   ├── serializers.py
│   └── urls.py
├── weather/               # Weather API app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── pic_to_ASCII/          # ASCII art API app
├── todo_site/             # Project settings and routing
│   ├── settings.py
│   ├── urls.py
│   └── auth_views.py      # JWT auth endpoints
├── db.sqlite3
├── manage.py
├── requirements.txt
└── pyproject.toml
```

## Getting Started

1. **Clone the repository:**
```bash
git clone https://github.com/kamalpandi/Django-api-server.git
cd Django-api-server
```

2. **Create and activate a virtual environment:**
```bash
python -m venv env
source env/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables** — create a `.env` file:
```
DEBUG=True
FRONTEND_URL=http://localhost:5173
```

5. **Run migrations:**
```bash
python manage.py migrate
```

6. **Start the development server:**
```bash
python manage.py runserver
```

The server runs at `http://127.0.0.1:8000/` and redirects the root URL to the React frontend.

---

## Frontend

The React frontend that consumes this API lives at:
- **Repo**: [Django-frontend](https://github.com/kamalpandi/Django-frontend)
- **Live**: [django-frontend-two.vercel.app](https://django-frontend-two.vercel.app/)

---

## Contributing

Contributions are welcome! Feel free to submit pull requests for bug fixes, feature enhancements, or new API endpoints.