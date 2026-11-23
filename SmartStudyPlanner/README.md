# Smart Study Planner

## Intelligent Student Study Planning and Mental Fatigue Monitoring System

Smart Study Planner is a web-based productivity and study management system designed to help students organize their studies while monitoring study-related fatigue.

The system combines **Data Structures, intelligent scheduling, fatigue detection, revision planning, and analytics** into one web application.

---

## Project Objectives

The main objectives of Smart Study Planner are:

- Create personalized study schedules.
- Organize subjects and study topics.
- Prioritize difficult and important topics.
- Use data structures to manage study tasks.
- Calculate the student's fatigue score.
- Detect different levels of study fatigue.
- Automatically activate Health Maintenance Mode when required.
- Schedule revision using spaced repetition.
- Track study productivity.
- Display analytics through charts.
- Provide daily motivational quotes.
- Help students maintain a healthier and more balanced study routine.

---

## Main Features

### 1. Smart Study Planner

Students can enter:

- Subjects
- Topics
- Topic difficulty
- Estimated study time
- Topic priority
- Available study time

The system organizes these topics into an appropriate study schedule.

---

### 2. Data Structures

The project demonstrates several important data structures.

#### Queue

A queue is used to manage the study-task sequence.

The first task added is processed first.

```text
Study Topic 1
      ↓
Study Topic 2
      ↓
Study Topic 3
      ↓
Study Topic 4
```

This follows the **FIFO (First In, First Out)** principle.

---

#### Stack

A stack is used for revision management.

Recently completed topics can be placed on the revision stack.

The most recently added revision topic is handled first.

This follows the **LIFO (Last In, First Out)** principle.

---

#### Priority Queue

A priority queue is used to prioritize study topics.

Topics can be prioritized according to:

- Importance
- Difficulty
- Urgency
- Examination relevance

High-priority topics can therefore receive earlier scheduling.

---

#### Linked List

A linked list can be used to maintain dynamically changing study topics and revision items.

This allows topics to be inserted or removed without requiring a fixed-size structure.

---

## 3. Mental Health and Fatigue Detection

The system calculates a fatigue score using:

```text
Fatigue Score =
(H × 2)
+ (C × 1.5)
+ (D × 1)
- (B × 2)
- (S × 1.5)
```

Where:

- H = Hours studied
- C = Number of continuous sessions
- D = Difficulty level
- B = Number of breaks
- S = Sleep hours

The system uses four fatigue levels.

| Score | Level        |
| ----- | ------------ |
| 0–5   | Normal       |
| 6–10  | Mild fatigue |
| 11–15 | High fatigue |
| >15   | Critical     |

---

## 4. Health Maintenance Mode

When the student's fatigue becomes high or critical, the system can activate Health Maintenance Mode.

The system can then:

- Reduce the study workload.
- Move difficult topics to a later schedule.
- Add additional breaks.
- Allow only light revision.
- Add relaxation activities.
- Limit study time.
- Display calming messages.
- Provide motivational or supportive content.

The purpose is to prevent the study schedule from becoming excessively demanding.

---

## 5. Revision Management

Completed topics are added to the revision system.

The system can schedule revision cycles such as:

```text
Cycle 1 → Initial Revision
Cycle 2 → Later Revision
Cycle 3 → Reinforcement
Cycle 4 → Final Revision
```

This supports a spaced-repetition approach to learning.

---

## 6. Analytics Dashboard

The dashboard provides information about the student's study performance.

### Study Summary

The dashboard can display:

- Total study hours
- Subjects completed
- Topics completed
- Topics pending
- Productivity score

### Mental Health Insights

The system can display:

- Current fatigue score
- Fatigue level
- Fatigue trend
- Sleep information
- Study-performance relationship

### Revision Analytics

The dashboard can display:

- Topics revised
- Upcoming revisions
- Completed revision cycles

### Schedule Quality

The system can identify:

- Overloaded days
- Balanced study days
- Pending topics
- Suggested improvements

---

## 7. Charts

The analytics section can include:

- Study-hours bar chart
- Fatigue trend line chart
- Subject completion chart
- Revision timeline

These visualizations help students understand their study patterns.

---

## 8. Daily Motivation

The system provides motivational messages based on the student's current situation.

Possible categories include:

- Motivation
- Calming
- Confidence
- Consistency

Example messages:

> Small steps every day create big results.

> Your pace is perfect — just don't stop.

> You're learning, growing, and becoming stronger.

> Rest is also part of progress.

---

# System Workflow

The overall system works as follows:

```text
Student
   ↓
Enter Subjects and Topics
   ↓
Create Study Queue
   ↓
Prioritize Topics
   ↓
Generate Study Schedule
   ↓
Study Session
   ↓
Collect Study Information
   ↓
Calculate Fatigue Score
   ↓
Determine Fatigue Level
   ↓
 ┌─────────────────────────────┐
 │                             │
Normal / Mild             High / Critical
 │                             │
 ↓                             ↓
Normal Schedule          Health Maintenance
 │                             │
 └──────────────┬──────────────┘
                ↓
        Complete Topic
                ↓
        Revision Stack
                ↓
      Spaced Revision
                ↓
        Update Analytics
                ↓
      Display Motivation
```

---

# Technology Stack

## Frontend

- HTML
- CSS
- JavaScript

## Backend

- Python
- Flask

## Database

- SQLite

## Data Structures

- Queue
- Stack
- Priority Queue
- Linked List

## Testing

- pytest

## Data Visualization

- Matplotlib

## Development Environment

- Visual Studio Code

---

# Project Structure

```text
SmartStudyPlanner/
│
├── .vscode/
│   ├── settings.json
│   ├── launch.json
│   └── tasks.json
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── config.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── planner.html
│   │   ├── analytics.html
│   │   ├── health_mode.html
│   │   ├── revision.html
│   │   └── profile.html
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── datastructures/
│   │   ├── queue.py
│   │   ├── stack.py
│   │   ├── priority_queue.py
│   │   └── linked_list.py
│   │
│   ├── scheduler/
│   │   ├── study_scheduler.py
│   │   ├── revision_scheduler.py
│   │   ├── fatigue_calculator.py
│   │   └── health_mode.py
│   │
│   ├── analytics/
│   │   ├── analytics.py
│   │   ├── productivity.py
│   │   └── charts.py
│   │
│   ├── utils/
│   │   ├── helpers.py
│   │   ├── validators.py
│   │   ├── quotes.py
│   │   └── constants.py
│   │
│   └── database/
│       └── database.py
│
├── instance/
│   └── studyplanner.db
│
├── docs/
│   ├── ER_Diagram.png
│   ├── UseCaseDiagram.png
│   ├── Flowchart.png
│   └── Project_Report.pdf
│
├── tests/
│   ├── test_queue.py
│   ├── test_stack.py
│   ├── test_scheduler.py
│   └── test_fatigue.py
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

---

# Installation

## 1. Install Python

Install Python 3.10 or newer.

Check the installation using:

```bash
python --version
```

---

## 2. Open the Project

Open the `SmartStudyPlanner` folder in Visual Studio Code.

---

## 3. Create a Virtual Environment

Open the VS Code terminal and run:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

---

## 4. Install Dependencies

Install the packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

# Running the Application

After the project is completely configured, run:

```bash
python app.py
```

The Flask development server will then provide a local website address.

Open the displayed address in a web browser.

---

# Testing

The project uses pytest for automated testing.

Run:

```bash
pytest
```

The tests verify important components such as:

- Queue
- Stack
- Scheduler
- Fatigue calculation

---

# Fatigue Detection Example

For example, if a student enters:

```text
Hours studied = 6
Continuous sessions = 4
Difficulty = 3
Breaks = 1
Sleep = 5
```

The system calculates the fatigue score using the defined formula.

The resulting score is then mapped to a fatigue level.

If the score reaches a high or critical level, the system can activate Health Maintenance Mode.

---

# Project Outcome

The final system is intended to provide a complete intelligent study-management environment where:

```text
Study Planning
      +
Data Structures
      +
Fatigue Detection
      +
Health Maintenance
      +
Revision Scheduling
      +
Analytics
      +
Motivation
      =
Smart Study Planner
```

The project demonstrates how fundamental data structures and Python programming can be applied to a practical student productivity problem.

---

# Academic Relevance

This project is particularly suitable for a **Data Structures and Algorithms** course because the core scheduling system demonstrates practical applications of:

- Queue
- Stack
- Priority Queue
- Linked List
- Searching
- Sorting
- Scheduling algorithms

The web interface provides a practical way to interact with these data structures rather than presenting them only as console-based programs.

---

# Future Enhancements

Possible future improvements include:

- Machine-learning-based fatigue prediction.
- Personalized study recommendations.
- Calendar integration.
- Mobile application support.
- Cloud database integration.
- Notification system.
- More advanced spaced-repetition algorithms.
- AI-based study recommendations.
- Real-time productivity monitoring.

---

# Project Status

**Development in progress**

The project is being developed incrementally using Python, Flask, HTML, CSS, JavaScript, SQLite, and fundamental data structures.
