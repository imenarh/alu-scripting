# Verdikt

Verdikt is a rubric-first grading prototype. This implementation runs as a plain `HTML/CSS/JS` app with a tiny Node server, local JSON persistence, rubric parsing, grading threads, submission scoring, and result history.

## Run it

```bash
npm start
```

Then open [http://localhost:3000](http://localhost:3000).

## Optional envs

- `PORT`: server port, defaults to `3000`
- `AI_PROVIDER`: optional provider label for future AI wiring
- `AI_MODEL`: optional model label for future AI wiring

## Current behavior

- Auth is intentionally skipped in the preview for faster iteration
- Data is stored in `data/db.json`
- Rubric parsing is deterministic
- Grading is deterministic and criterion-based so you can preview the full UX without an API key

---

# Verdikt — Product Requirements Document

> A web-based AI harness for submission grading based on a predefined assignment rubric.
---

## Problem  

Getting AI to grade work is inconsistent. Without structure, the model has no constraints, no rubric context, and no memory of how it graded the last submission. Students and teachers who try this today need serious prompting knowledge to get useful results — and even then, results drift between sessions.

---

## Solution

Verdikt is a grading harness. It takes a rubric, locks it to a grading thread, and runs a focused AI evaluation against each criterion independently — returning consistent scores and feedback every time. The rubric is the harness. The AI is the engine.

---

## Who It's For

**V1 — Students**
Students who want structured feedback on their work before submitting. Verdikt tells them exactly where they stand against each criterion, not just a vague overall impression.

**Upcoming — Teachers**
Managing rubrics across classes, grading student submissions at scale, and tracking results over time.

---

## Core Concepts

### Rubric

A rubric is a set of named criteria, each with a description and a maximum point value. In Verdikt, a rubric is created by pasting raw rubric text — the AI parses it into structured criteria. The user reviews the parsed result before confirming. Once a thread is created with a rubric, the rubric is **permanently locked** — no editing, no exceptions. This ensures every submission in a thread is graded against the exact same criteria.

### Grading Thread

A grading thread is a persistent session tied to one locked rubric. Once open, any number of submissions can be graded inside it. All results are saved to the thread and accessible from a toggleable sidebar.

### Grading Result

Each submission added to a thread triggers one AI call per criterion. Each call returns a score and short feedback for that criterion only. The backend sums the scores into a total. The full breakdown is saved permanently to the thread.

---

## User Flows

### Auth

1. User visits the app
2. Registers with name, email, password — or logs in
3. JWT token issued and stored — all subsequent requests are authenticated
4. Each user's data is fully private and isolated

### Creating a Grading Thread

1. User clicks **New Thread**
2. Enters a thread name
3. Pastes raw rubric text into a textarea (copied from a document, course portal, etc.)
4. Clicks **Parse Rubric** — Gemini extracts criteria into structured JSON:
    
    ```
    { "criteria": [ { "name": "...", "description": "...", "max_points": number } ] }
    ```
    
5. User reviews the parsed criteria — can re-paste and re-parse if incorrect
6. Clicks **Confirm & Lock** — rubric is saved, thread is created, rubric is permanently locked

### Grading a Submission

1. User opens a thread
2. Pastes a student submission into the grading input
3. Clicks **Grade**
4. Backend runs one AI call per criterion sequentially:
    - Each call receives: full rubric context + target criterion + submission text
    - Each call returns: `{ "score": number, "feedback": "string" }`
5. Progress is shown per criterion as each call completes
6. Final result is displayed: per-criterion score + feedback + total score
7. Result is saved to the thread automatically

### Reviewing Past Gradings

1. User clicks **History** to open the sidebar
2. Sidebar lists all past results for the thread, most recent first
3. User clicks any result to expand the full per-criterion breakdown
4. Only one result is expanded at a time

---

## Features

### V1

- User registration and login with JWT auth
- Paste rubric text → AI parses into structured criteria → user reviews → locked on confirm
- Create grading threads tied to one locked rubric
- Paste submissions and trigger per-criterion AI grading
- Per-criterion score + short feedback + total score per result
- Toggleable sidebar with full grading history per thread
- All data scoped privately per user

### Out of Scope for V1

- File upload for submissions (`.txt`, `.pdf`, `.docx`)
- Teacher accounts and class management
- Exporting results as CSV
- Rubric versioning
- Admin roles

---

## Data Models

**User**

```
id, name, email, password_hash, created_at
```

**Thread**

```
id, user_id, name, created_at
rubric: {
  criteria: [ { id, name, description, max_points } ]
}
```

**Result**

```
id, thread_id, submission_text, total_score, max_total, graded_at
criteria_scores: [
  { criterion_id, criterion_name, score, max_points, feedback }
]
```

---

## API Routes

| Method | Route | Auth | Purpose |
| --- | --- | --- | --- |
| POST | `/api/auth/register` | No | Create account |
| POST | `/api/auth/login` | No | Login, receive JWT |
| POST | `/api/rubric/parse` | Yes | Parse raw rubric text into structured JSON |
| GET | `/api/threads` | Yes | List user's threads |
| POST | `/api/threads` | Yes | Create thread with locked rubric |
| GET | `/api/threads/:id` | Yes | Load thread, rubric, and all results |
| POST | `/api/threads/:id/grade` | Yes | Grade a submission |

---

## Grading Logic

1. Backend receives submission text and fetches the thread's locked rubric
2. For each criterion, a focused AI call is made with:
    - Full rubric context (all criteria for framing)
    - The specific criterion: name, description, max points
    - The student submission
3. Each call returns: `{ "score": number, "feedback": "string" }`
4. Backend sums scores into a total and saves the full result to the thread

One criterion per call ensures focused, consistent, auditable scoring.

---

## Constraints & Rules

- Rubrics are immutable after thread creation — no exceptions
- Grading threads cannot change their rubric
- Users can only access their own threads and results
- AI API key is server-side only — never exposed to the client
- Passwords are hashed before storage — never stored plain
