# Event Management System

A modern event management web application built with Django and Tailwind CSS.

## Features

- **Event Management**: Create, update, and delete events with detailed information
- **Category Organization**: Organize events into categories for easy navigation
- **Participant Registration**: Manage participant information and event registrations
- **Search & Filter**: Advanced search and filtering options for events
- **Responsive Design**: Mobile-friendly interface using Tailwind CSS
- **Query Optimization**: Optimized database queries to prevent N+1 problems

## Tech Stack

- **Backend**: Django 6.0.1
- **Database**: PostgreSQL
- **Frontend**: Tailwind CSS 3.4.16
- **Dependencies**: 
  - psycopg2 (PostgreSQL adapter)
  - Faker (data generation)
  - Pillow (image processing)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ripro805/Event-Management-Website.git
cd event_management
```

2. Create and activate virtual environment:
```bash
python -m venv event_env
event_env\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install django psycopg2-binary pillow faker
npm install
```

4. Configure database in `event_management/settings.py`

5. Run migrations:
```bash
python manage.py migrate
```

6. Build Tailwind CSS:
```bash
npm run build:tailwind
```

7. Run the development server:
```bash
python manage.py runserver
```

## Usage

- Access the application at `http://127.0.0.1:8000`
- Create categories, events, and manage participants
- Use search and filter options to find specific events
- All CRUD operations are fully functional with database persistence

## Project Structure

```
event_management/
├── events/              # Main application
│   ├── templates/       # HTML templates
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── forms.py         # Form classes
│   └── urls.py          # URL patterns
├── static/              # Static files (CSS, JS, images)
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

## License

This project is open source and available for educational purposes.

## Author

Developed as part of Phitron Software Development Track - Django Course
