# [Django Multi-App Dashboard](https://vibi.pythonanywhere.com/)

This [repository](https://vibi.pythonanywhere.com/) hosts a **Django project** featuring multiple interactive web applications built with **HTMX** for a dynamic frontend experience. The project is designed to showcase mostly backend and little frontend capabilities, with clean modular architecture and scalable app structure.

## Features

* **ToDo App**: A task management application with CRUD functionality to add, edit, and delete tasks.
* **Weather App**: Provides real-time weather information using external APIs, allowing users to check the current conditions for any city.
* **Pic to ASCII App**: Converts uploaded images into ASCII art (optional app), demonstrating file handling and image processing in Django.
* **Centralized Homepage**: Serves as a landing page with navigation to all included apps.
* **HTMX Integration**: Enhances user experience by enabling dynamic content updates without full page reloads.
* **Modular Architecture**: Each app is self-contained with its own models, views, templates, and static files for maintainability and scalability.

## Tech Stack

* **Backend**: Django, Python 3.14
* **Frontend**: HTML, CSS, HTMX
* **Database**: SQLite (default for development)
* **Deployment**: PythonAnywhere
* **Tools & Libraries**: HTMX, Requests (for API calls), Pillow (for image handling)

## Project Structure

```
Django-api-server/
├── todo/                  # ToDo app
├── weather/               # Weather app
├── pic_to_ASCII/          # Pic to ASCII app
├── todo_site/             # Django project settings and routing
├── db.sqlite3             # Development database
├── manage.py              # Django management script
└── requirements.txt       # Dependencies
```

## Getting Started

1. **Clone the repository:**

```bash
git clone https://github.com/kamalpandi/Django-api-server.git
cd Django-api-server
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run migrations:**

```bash
python manage.py migrate
```

4. **Start the development server:**

```bash
python manage.py runserver
```

5. **Visit the apps:**

* ToDo App: `http://localhost:8000/todo/`
* Weather App: `http://localhost:8000/weather/`
* Pic to ASCII App: `http://localhost:8000/pic-to-ascii/` (if enabled)

---

## Contributing

Contributions are welcome! Feel free to submit pull requests for bug fixes, feature enhancements, or new apps.

---
