# Application Tracker — Database Design

## Overview

Application Tracker uses a relational database through Django's ORM.

SQLite is used for development, while the model design is intended to remain compatible with PostgreSQL for future deployment.

The database is organized around the application workflow rather than treating each feature as an isolated CRUD module.

## Core Entities

```text
User
University
Program
Application
Scholarship
Document
ApplicationDocument
Task
Contact
```

## Relationships

### User → Application

```text
User 1 ──── * Application
```

A user can have multiple university applications.

Each application belongs to one user.

### University → Program

```text
University 1 ──── * Program
```

A university can offer multiple programs.

Each program belongs to one university.

Programs are uniquely identified within their university and degree type.

### University → Application

```text
University 1 ──── * Application
```

A university can have multiple applications associated with it.

Applications protect the university relationship from accidental deletion.

### Program → Application

```text
Program 1 ──── * Application
```

A program can be associated with multiple applications.

The application validates that the selected program belongs to the selected university.

### Scholarship → Application

```text
Scholarship 1 ──── * Application
```

A scholarship can be associated with multiple applications.

The relationship is optional because an application may not have a scholarship.

Deleting a scholarship does not delete applications; the relationship can be set to null.

### Application → ApplicationDocument

```text
Application 1 ──── * ApplicationDocument
```

An application can have multiple required or optional document checklist entries.

### Document → ApplicationDocument

```text
Document 1 ──── * ApplicationDocument
```

A reusable personal document can be associated with multiple application checklists.

This prevents unnecessary duplication of the same uploaded file.

### Application → Task

```text
Application 1 ──── * Task
```

Tasks can optionally belong to an application.

This allows both application-specific tasks and general tasks.

### University → Contact

```text
University 1 ──── * Contact
```

A university can have multiple contacts.

A contact may optionally be associated with a particular application.

### User → Document

```text
User 1 ──── * Document
```

Documents are owned by the authenticated user.

### User → Task

```text
User 1 ──── * Task
```

Tasks are owned by the authenticated user.

### User → Contact

```text
User 1 ──── * Contact
```

Contacts are owned by the authenticated user.

## Entity Summary

### User

Custom Django authentication model.

Important fields include:

* `email`
* `created_at`
* `updated_at`

### University

Stores reference information about universities.

Important fields include:

* `name`
* `country`
* `city`
* `website`
* `ranking`
* `description`
* `notes`

### Program

Stores academic programs belonging to universities.

Important fields include:

* `university`
* `name`
* `degree_type`
* `study_language`
* `duration`
* `tuition_fee`
* `description`
* `requirements`

### Application

Central workflow entity.

Important fields include:

* `user`
* `university`
* `program`
* `scholarship`
* `status`
* `status_updated_at`
* `application_deadline`
* `scholarship_deadline`
* `portal_url`
* `submitted_at`
* `decision_at`
* `notes`

### Scholarship

Reusable scholarship reference data.

Important fields include:

* `name`
* `provider`
* `scholarship_type`
* `deadline`
* `coverage`
* `stipend`
* `eligibility`
* `application_url`
* `notes`

### Document

Reusable personal document library.

Important fields include:

* `user`
* `name`
* `document_type`
* `file`
* `issue_date`
* `expiry_date`
* `notes`

### ApplicationDocument

Application-specific document requirement/checklist.

Important fields include:

* `application`
* `document`
* `document_type`
* `required`
* `status`
* `submitted_at`
* `notes`

A checklist item can exist without an attached file. This allows missing-document tracking before the actual document is uploaded.

### Task

Stores actionable work.

Important fields include:

* `user`
* `application`
* `title`
* `description`
* `due_date`
* `priority`
* `status`
* `completed_at`

### Contact

Stores university-related people.

Important fields include:

* `user`
* `university`
* `application`
* `name`
* `position`
* `department`
* `email`
* `research_area`
* `status`
* `last_contacted`
* `follow_up_date`
* `notes`

## Delete Behavior

Relationships intentionally use different deletion behaviors depending on the importance of the relationship.

```text
University → Application       PROTECT
Program → Application          PROTECT
Scholarship → Application      SET_NULL
Application → Task             CASCADE
Application → ApplicationDocument
                               CASCADE
Application → Contact          SET_NULL
Document → ApplicationDocument PROTECT
```

The goal is to prevent accidental deletion of important reference data while allowing dependent workflow records to disappear when their parent application is intentionally deleted.

## Uniqueness

Applications use conditional uniqueness rules.

An application with a scholarship is uniquely identified by:

```text
user + university + program + scholarship
```

An application without a scholarship is uniquely identified by:

```text
user + university + program
```

This prevents duplicate applications while still allowing the same university/program combination to exist once with a specific scholarship association where appropriate.

## Data Integrity

The application relies on the database and Django validation together.

Important integrity rules include:

* Programs must belong to their selected university.
* Application records belong to an authenticated user.
* User-owned objects are filtered by owner.
* Required application document states require an appropriate document.
* Application dates must remain logically consistent.
* Duplicate application combinations are prevented.

## Future Database Extensions

Potential future entities include:

```text
ContactInteraction
Notification
DeadlineReminder
ApplicationEvent
```

These are deliberately not part of the current schema because the current workflow does not yet require them.

They should only be introduced when the corresponding feature provides enough value to justify the additional data model complexity.
