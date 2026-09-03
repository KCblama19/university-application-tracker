# Application Tracker — Development Guide

## Development Environment

The project is developed using:

* Python
* Django 5.2
* SQLite
* HTML
* CSS
* JavaScript
* Django Templates
* Django ORM
* python-dotenv

The development environment does not currently require Docker, Redis, Celery, React, or a separate API service.

## Project Setup

Clone the repository:

```bash
git clone git@github.com:KCblama19/university-application-tracker.git
cd university-application-tracker
```

Create a virtual environment.

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the environment file:

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

Apply migrations:

```bash
python manage.py migrate
```

Create an administrator:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

## Environment Configuration

Environment-specific values are stored in `.env`.

Example:

```env
SECRET_KEY=replace-this-with-a-real-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

The `.env` file must not be committed to Git.

`.env.example` is committed as a template.

## Django Checks

Before committing changes, run:

```bash
python manage.py check
```

This verifies that Django can load the project and identifies common configuration problems.

## Database Changes

When modifying models:

```bash
python manage.py makemigrations
```

Review the generated migration before applying it.

Then:

```bash
python manage.py migrate
```

Migration files are committed to Git because they are part of the application's database history.

## Testing

The project uses multiple levels of testing.

### Framework checks

```bash
python manage.py check
```

### Automated tests

```bash
python manage.py test
```

Automated test coverage is still being expanded.

### Manual browser testing

Manual browser testing is currently an important part of the development process.

Major workflows that have been manually tested include:

* Registration
* Login
* Logout
* University CRUD
* Program CRUD
* Scholarship CRUD
* Application CRUD
* Application validation
* University/program dynamic selection
* Document management
* Application document checklists
* Task management
* Contact management
* Dashboard
* Application detail workflow

Passing `manage.py check` is not considered equivalent to testing the complete user workflow.

## Ownership Testing

Whenever a view accesses a user-owned object, verify that the object is scoped to the authenticated user.

For example:

```python
Application.objects.get(
    id=application_id,
    user=request.user,
)
```

Do not rely only on the URL containing an object ID.

Object ownership must be enforced at the query level.

## Form Validation

Server-side validation must remain authoritative.

Client-side JavaScript can improve usability, such as dynamically loading programs after selecting a university, but it must not replace server-side validation.

Important examples include:

* Program/university consistency
* Application uniqueness
* Required dates for submitted/decision statuses
* Document ownership
* Document type matching
* Contact/application university consistency

## Query Optimization

Use `select_related()` for single-valued relationships and `prefetch_related()` for collections.

Example:

```python
Application.objects.select_related(
    "university",
    "program",
    "scholarship",
).prefetch_related(
    "application_documents__document",
    "tasks",
    "contacts",
)
```

Optimization should be driven by actual query patterns rather than adding relationship prefetching everywhere.

## Git Workflow

The project uses `main` as the primary branch.

Typical workflow:

```bash
git status
git add .
git commit -m "Describe the change"
git push
```

Before committing:

1. Review changed files.
2. Confirm no secrets are staged.
3. Run Django checks.
4. Run available automated tests.
5. Manually test important UI changes.
6. Review the Git diff.

Useful commands:

```bash
git status
git diff
git diff --cached
git log --oneline --graph --decorate --all
```

## Commit Guidelines

Commits should describe meaningful changes.

Examples:

```text
Add application detail workflow
Fix application document query
Improve dashboard deadline handling
Add architecture documentation
Update README license information
```

Avoid meaningless commit messages such as:

```text
update
changes
fix stuff
AI generated
```

## Pull Requests

Pull requests are not required for every local change while the project is maintained as a personal repository.

They become useful if:

* External contributors are involved.
* Experimental features are developed separately.
* A larger feature needs review before merging.

## Production Considerations

Before production deployment, review:

* `DEBUG=False`
* Strong production `SECRET_KEY`
* `ALLOWED_HOSTS`
* HTTPS
* Secure cookies
* CSRF configuration
* Static files
* Media storage
* Database configuration
* PostgreSQL deployment
* Error logging
* Backup strategy
* File upload security

The current development configuration should not automatically be treated as production-ready.

## Development Philosophy

The project favors incremental development.

A feature should generally move through:

```text
Requirement
    ↓
Data model
    ↓
Validation
    ↓
View
    ↓
Template
    ↓
Manual testing
    ↓
Refinement
    ↓
Documentation
```

Complexity should be introduced only when the application's actual requirements justify it.
