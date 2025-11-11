# Recruitment Assistant Agentic System

## Objective
Design an agentic system that automates candidate screening, interview scheduling, and feedback collection while ensuring safety, fairness, and human oversight.

## Evaluation Criteria
Your submission will be evaluated on:
- **Conceptual Understanding**: clear architecture, orchestration design, state & memory handling, safety mechanisms.
- **Tooling Awareness**: appropriate use or justification of frameworks such as LangGraph & LangChain.
- **Design Thinking**: balance between autonomy and human-in-the-loop (HIL) collaboration.
- **Evaluation & Monitoring**: edge-case handling, testing plan, metrics, limitations, and optimization strategies.

## System Requirements

### Core Functions
- Parse resumes → shortlist qualified candidates.
- Schedule interviews (via Calendar API or simulated).
- Collect and summarize interviewer feedback.
- **Agents (example)**: Resume Parser, Qualification Agent, Scheduler, Notification, Feedback Collector, and HIL Gateway.
- **Memory & Safety**: define what data is stored, retention policies, and rollback/fail-safe design.
- **Edge Cases**: handle parsing errors, scheduling conflicts, API downtime, and duplicate candidates.
- **Monitoring & Metrics**: measure success rate, time-to-schedule, feedback completion, bias indicators, and SLA reliability.

## Functional Requirements

### Resume Parsing
- Parse resumes (PDF, DOCX)
- Extract structured data (candidate details, skills, experience, education)

### Candidate Screening
- Match candidate profile with JD
- Generate shortlisted candidates with score/rank and justifications

### Interview Scheduling
- Check interviewer and candidate availability and fix interview slot
- Send calendar invites
- Support rescheduling and cancellations if needed

### Feedback Management
- Collect feedback from interviewers post-interview
- If multiple rounds, track and summarize all feedbacks

### Human-in-the-Loop
- Send to human for final candidate approval/decisions
- Can override agent decisions if needed

### Notifications & Communication
- Send status update to candidates
- Remind interviewers on upcoming interviews and to share feedback
- Keep HR in the loop about candidate interview status

## Non-Functional Requirements
- Resume parsing < 30 sec
- Shortlisting batch of 100 resumes < 5 mins
- 1000+ candidates per job
- 99.9% uptime
- Scalability
- Security
- Observability & monitoring

## High Level Agentic System Design
![High Level Design](Recruitment%20Agent-Page-2.drawio.png)