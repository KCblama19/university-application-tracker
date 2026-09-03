# AI-Assisted Development

## Overview

Application Tracker was developed with significant assistance from AI coding tools.

The project is intentionally presented as **AI-assisted development** rather than as a completely hand-written project.

The purpose was not to delegate the entire development process to AI. Instead, AI tools were used as development assistants while the project requirements, decisions, evaluation, testing, and final acceptance remained human-directed.

## Why AI Was Used

The project was partly built as an opportunity to evaluate how effectively AI-assisted development can accelerate a real software project, based on my current knowledge of the tech stack used and my Al usage capability, while using it as an opportunity to learn why and how AI tools make decisions that are based on a fast, iterative process.

This was built entirely with the ChatGPT free tier; I didn't use coding agents such as Codex, Claude, or other AI tools because they have free-tier limitations on code generation, and I needed full supervision of the code provided.

AI tools were useful for reducing the time required for:

* Repetitive implementation
* Exploring Django approaches
* Debugging errors
* Refactoring
* Documentation
* Reviewing design decisions
* Query optimization
* Generating implementation starting points
* Identifying potential edge cases

This allowed more time to be spent evaluating whether the resulting implementation actually fit the requirements.

## Areas Where AI Assisted

AI assistance was used across several parts of the project.

### Architecture

AI was used to discuss:

* Application boundaries
* Data relationships
* Ownership rules
* Delete behavior
* Validation responsibilities
* Query optimization
* Future extensibility

Architectural suggestions were reviewed before implementation rather than accepted automatically.

### Django Implementation

AI assisted with implementation and explanation of:

* Models
* Forms
* Views
* URLs
* Templates
* Authentication
* Querysets
* Validation
* File uploads
* Dashboard aggregation

### Debugging

AI was also used during debugging.

When an implementation produced an error, the development process involved:

```text
Error
  ↓
Understand the cause
  ↓
Identify possible solutions
  ↓
Implement a fix
  ↓
Test the result
  ↓
Evaluate whether the fix introduced another problem
```

The objective was not simply to remove error messages but to understand why the error occurred.

### Refactoring

AI assistance was used to identify opportunities for:

* Cleaner code
* Better query patterns
* Improved validation
* Reduced duplication
* More maintainable templates
* Better documentation

Refactoring decisions were evaluated against the project's actual requirements.

## Human Responsibility

I remained responsible for:

* Defining requirements
* Choosing the application's scope
* Making architectural and design decisions
* Evaluating AI-generated suggestions
* Reviewing implementation
* Testing workflows
* Identifying incorrect assumptions
* Debugging when generated solutions were insufficient
* Deciding which features to postpone
* Accepting or rejecting generated code
* Fixing and Debugging Errors

AI output was treated as a proposal rather than an unquestioned implementation.

## Verification

The project uses several forms of verification.

### Django system checks

```bash
python manage.py check
```

### Automated tests

```bash
python manage.py test
```

Automated test coverage is still being expanded.

### Manual testing

The major application workflows were tested through the browser.

This included:

* Authentication
* University management
* Program management
* Scholarship management
* Application management
* Application validation
* Document management
* Application document checklists
* Task management
* Contact management
* Dashboard
* Application detail workflow

Manual testing is important because framework-level checks cannot verify whether a complete user workflow behaves correctly.

## What AI Does Not Replace

Using AI does not eliminate the need to understand the resulting code.

For this project, particular attention was given to understanding:

* Django model relationships
* Querysets
* `select_related()` and `prefetch_related()`
* Forms and validation
* Authentication
* Object ownership
* Database constraints
* File handling
* HTTP request/response flow
* Template rendering

The goal is to use AI to accelerate development while continuing to build the technical understanding required to maintain the project.

## Lessons From AI-Assisted Development

Several principles emerged from the development process:

### 1. AI can produce working code that is still architecturally wrong

A solution can fix an immediate error while introducing a poor long-term design.

The implementation therefore has to be evaluated beyond whether it runs.

### 2. Context matters

AI-generated solutions become significantly more useful when the project's existing architecture, requirements, and constraints are clearly defined.

### 3. Testing remains essential

Generated code should not be considered correct simply because it looks reasonable.

It needs to be executed and tested.

### 4. Simpler is often better

AI tools can easily suggest additional frameworks, abstractions, or services.

The project intentionally avoids introducing technologies that do not solve an actual problem.

### 5. Understanding matters more than generation

The purpose of AI-assisted development is not merely to generate more code.

It is to increase development speed while improving the ability to reason about architecture, implementation, and trade-offs.

## Transparency

This repository documents its AI-assisted development process intentionally.

The project is not presented as an example of entirely manual programming.

Instead, it demonstrates a workflow in which AI tools were used substantially while I remained responsible for direction, supervision, evaluation, testing, and final decisions.
