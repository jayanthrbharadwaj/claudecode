<!-- AGENT: Do not read during exploration. This template is used only when creating specs. Read .claude/docs/scaffold-overview.md instead. -->
# App Spec: [Project Name]

**Status**: [draft | review | approved]

## Overview

What this application does in 2-3 sentences. What problem it solves and who it's for.

## Technology Stack

### Frontend
- **Framework**: [e.g., React with Vite, Next.js, SvelteKit]
- **Styling**: [e.g., Tailwind CSS, CSS Modules]
- **State management**: [e.g., React hooks + context, Zustand, Redux]
- **Routing**: [e.g., React Router, file-based routing]

### Backend
- **Runtime**: [e.g., Python/FastAPI, Node.js/Express]
- **Database**: [e.g., PostgreSQL, SQLite, MongoDB]
- **API style**: [e.g., REST, GraphQL]
- **Authentication**: [e.g., JWT, session-based, OAuth]

### External Services
- [Service name] — [purpose, e.g., "Anthropic API — chat completions"]
- [Service name] — [purpose]

### Infrastructure
- **Hosting**: [e.g., Azure App Service (default), AWS ECS, Vercel, GCP Cloud Run]
- **CI/CD**: [e.g., GitHub Actions (default)]
- **Containerization**: [e.g., Docker (default)]
- **Database hosting**: [e.g., Azure Database for PostgreSQL, AWS RDS, local SQLite]
- **Secrets management**: [e.g., Azure Key Vault, AWS Secrets Manager, .env files]
- **Deployment strategy**:
  - Environments: [e.g., staging + production]
  - Triggers: [e.g., push to main → staging, manual approval → production]
  - Zero-downtime: [e.g., rolling deployment, blue-green, slot swap]

## Core Features

Group features by domain area. Each group becomes a candidate for a feature spec.

### [Feature Group 1: e.g., Chat Interface]
- [Feature with enough detail for an agent to implement]
- [Feature]
- [Feature]

### [Feature Group 2: e.g., Conversation Management]
- [Feature]
- [Feature]

### [Feature Group 3: e.g., User Settings]
- [Feature]
- [Feature]

> Add as many feature groups as needed. Each group should be cohesive — implementable as one unit.

## Database Schema

Define every table, column, type, and constraint. The agent writes migrations directly from this.

### [table_name]
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `INTEGER` | `PRIMARY KEY` | |
| `name` | `TEXT` | `NOT NULL` | Max 100 chars |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT NOW()` | |

### [table_name]
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| | | | |

> Add one table per entity. Include foreign keys, indexes, and enum value sets.

## API Endpoints

Organize by resource. Include method, path, and brief description.

### [Resource: e.g., Conversations]
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/conversations` | List all conversations |
| `POST` | `/api/conversations` | Create a new conversation |
| `GET` | `/api/conversations/:id` | Get conversation by ID |
| `PUT` | `/api/conversations/:id` | Update conversation |
| `DELETE` | `/api/conversations/:id` | Delete conversation |

### [Resource: e.g., Messages]
| Method | Path | Description |
|--------|------|-------------|
| | | |

> For key endpoints, add request/response body examples below the table.

## UI Layout

### Main Structure
Describe the overall layout (e.g., sidebar + main content + panel).

### [Section: e.g., Sidebar]
- [Element and behavior]
- [Element and behavior]

### [Section: e.g., Main Content Area]
- [Element and behavior]
- [Element and behavior]

### Key Modals / Overlays
- [Modal name] — [trigger and purpose]

## Design System

### Colors
- **Primary**: [hex and usage]
- **Background**: [light mode / dark mode values]
- **Text**: [light mode / dark mode values]

### Typography
- **Font family**: [e.g., Inter, system-ui]
- **Body text**: [size, weight, line-height]
- **Code**: [monospace font]

### Component Patterns
- **Buttons**: [primary, secondary, icon — describe style]
- **Inputs**: [style, states]
- **Cards**: [style, spacing]

## Key Interaction Flows

### [Flow 1: e.g., Send a Message]
1. [Step]
2. [Step]
3. [Step]

### [Flow 2: e.g., Create a Project]
1. [Step]
2. [Step]

## Implementation Phases

Break the build into phases. Each phase should produce a working (if incomplete) application.

### Phase 1: [Foundation]
- [Task]
- [Task]
- **Milestone**: [What works after this phase]

### Phase 2: [Core Feature]
- [Task]
- [Task]
- **Milestone**: [What works after this phase]

### Phase 3: [Secondary Features]
- [Task]
- [Task]
- **Milestone**: [What works after this phase]

> Each phase maps to one or more feature specs that will be generated from this app spec.

## Success Criteria

### Functional
- [ ] [Core flow works end-to-end]
- [ ] [All CRUD operations functional]
- [ ] [Error handling covers major failure modes]

### User Experience
- [ ] [Responsive on mobile and desktop]
- [ ] [Fast response times]
- [ ] [Intuitive navigation]

### Technical
- [ ] [Clean architecture — layers respected]
- [ ] [Test coverage >= 80%]
- [ ] [All linters pass]
- [ ] [No hardcoded secrets]

## Non-Functional Requirements

- **Performance**: [e.g., page load < 2s, API response < 200ms]
- **Security**: [e.g., input validation, auth on all endpoints, CORS configured]
- **Scalability**: [e.g., pagination on all list endpoints]
- **Accessibility**: [e.g., keyboard navigation, screen reader support]

## Open Questions

- [ ] [Any unresolved architecture decisions]
- [ ] [Any unclear requirements]
