# Application Tracker

A personal Django web application for managing university application process from one place.

Application Tracker is designed as a personal **application command center** rather than a collection of disconnected CRUD pages. It connects universities, programs, applications, scholarships, documents, contacts, tasks, and deadlines into one workflow so that important application-related actions are easy to see and manage.

## Why I Built This

Applying to universities involves tracking a large amount of related information:

* Universities and programs
* Applications and their current status
* Scholarships and deadlines
* Required and missing documents
* Professors and university contacts
* Follow-ups and tasks
* Application and scholarship deadlines

I built this project to centralize information and create a practical system that can be used throughout the application cycle.

The project is also an opportunity to practice building a complete Django application, including authentication, relational data modeling, validation, reusable components, query optimization, file handling, and dashboard design.

## Features

### Application Management

* Create, view, update, and delete applications
* Track application status throughout the application process
* Associate applications with universities, programs, and scholarships
* Track application and scholarship deadlines
* Store application portal URLs
* Track submission and decision dates
* Record application notes
* Track when an application's status was last changed

### University & Program Management

* Maintain a personal university database
* Store university information, rankings, websites, descriptions, and notes
* Manage programs offered by each university
* Store degree type, study language, duration, tuition, requirements, and descriptions
* Enforce program uniqueness within a university

### Scholarship Tracking

* Maintain a reusable scholarship database
* Track scholarship providers, types, deadlines, coverage, stipends, eligibility, and application URLs
* Associate scholarships with applications

### Document Management

* Maintain a reusable personal document library
* Upload documents such as transcripts, CVs, passports, study plans, recommendation letters, and language certificates
* Track issue and expiry dates
* Create application-specific document checklists
* Track document readiness and submission status
* Reuse documents across multiple applications

### Task Management

* Create application-specific or general tasks
* Track task status and priority
* Set due dates
* Identify overdue tasks
* Automatically manage task completion timestamps
* Filter tasks by status, priority, application, and overdue state

### Contact Management

* Track professors, admissions officers, coordinators, supervisors, and other university contacts
* Associate contacts with universities and optionally with applications
* Track communication status
* Record last-contacted and follow-up dates
* Store research areas, departments, and notes

### Dashboard

The dashboard provides a high-level view of the current application workload, including:

* Total applications
* Submitted applications
* Applications in progress
* Upcoming deadlines
* Pending and overdue tasks
* Document readiness
* Upcoming scholarship deadlines
* Application status distribution

The goal is to answer four questions quickly:

> **What is happening?**
> **What is due?**
> **What is missing?**
> **What should I do next?**

## Tech Stack

* **Python**
* **Django 5.2**
* **Django Templates**
* **HTML / CSS / JavaScript**
* **Django ORM**
* **SQLite** for development
* **PostgreSQL-ready** database design
* **Django Authentication**
* **python-dotenv** for environment configuration

The project intentionally avoids unnecessary complexity. It does not currently use React, Django REST Framework, Celery, Redis, Docker, or a separate frontend application.

## Architecture

The project uses a modular Django application structure:

* `accounts` — custom user model and authentication
* `universities` — universities and academic programs
* `applications` — application tracking and workflow
* `documents` — reusable documents and application document checklists
* `scholarships` — scholarship reference data
* `contacts` — university and professor contacts
* `tasks` — application-related and general tasks
* `dashboard` — application command center and aggregated statistics

### Entity Relationship Diagram
## Entity Relationship Diagram
The Diagram Demonstrates the relationships between various core entities in the program

![Application Tracker Entity Relationship Diagram](diagrams/erd.svg)

User-owned records are scoped to the authenticated user at the view/query level. Shared reference data such as universities, programs, and scholarships can be reused across the application workflow.

## Project Structure

```text
application_tracker/
├── manage.py
├── application_tracker/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── apps/
│   ├── accounts/
│   ├── universities/
│   ├── applications/
│   ├── documents/
│   ├── scholarships/
│   ├── contacts/
│   ├── tasks/
│   └── dashboard/
├── templates/
├── static/
│   └── css/
│       └── app.css
├── tests/
├── media/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

`media/` is used for local uploaded files and is intentionally excluded from version control.

## Getting Started

### 1. Clone the repository

```bash
git clone git@github.com:KCblama19/university-application-tracker.git
cd university-application-tracker
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env`.

**Windows PowerShell:**

```powershell
Copy-Item .env.example .env
```

**Linux / macOS:**

```bash
cp .env.example .env
```

Generate or replace `SECRET_KEY` with a real development secret and adjust the other values if necessary.

Example:

```env
SECRET_KEY=replace-this-with-a-real-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create an administrator account

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

Then open the local development server in your browser.

## Testing

Run Django's system checks:

```bash
python manage.py check
```

Run the test suite:

```bash
python manage.py test
```

The application has also been manually tested across the major workflows, including:

* Authentication
* University CRUD
* Program CRUD
* Scholarship CRUD
* Application CRUD
* Application validation
* Dynamic university/program selection
* Document management
* Application document checklists
* Task management
* Contact management
* Dashboard
* Application detail workflow

Manual browser testing is treated as an important part of development because passing framework checks alone does not verify the complete user workflow.

## AI-Assisted Development

This project was developed with significant assistance from AI coding tools.

AI was used as a development aid for areas such as:

* Architecture discussions
* Django implementation
* Debugging
* Refactoring
* Query optimization
* Validation design
* Documentation
* Reviewing implementation decisions

The development process remained iterative and human-directed. Requirements, product decisions, architectural choices, testing, evaluation of generated code, debugging, and final acceptance remained part of the development workflow.

The project is intentionally documented as **AI-assisted development** rather than presented as entirely hand-written code; this was done to test my use of AI tools to get certain urgent projects done fast, while ***supervising*** those tools with the current knowledge I have on the tech stacks used in this project.

## Future Improvements

Potential future improvements include:

* More comprehensive automated tests
* Advanced application and university search/filtering
* Improved dashboard prioritization
* Contact interaction history
* Follow-up reminders
* Deadline notifications
* Email and calendar integrations
* PostgreSQL deployment
* Responsive/mobile refinements
* Production deployment and security hardening

These features are intentionally deferred until the core application workflow is stable.

## License

This project is currently a personal learning project licensed under the MIT License.

See the LICENSE file for the full license text.