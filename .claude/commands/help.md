---
disable-model-invocation: true
---

# /forge:help

Show all available forge commands, skills, and agents.

## When to Use

- You're new to forge and want to see what's available
- You need a quick reference for available commands
- You want to understand the forge ecosystem

## Arguments

None.

## Process

1. Display the forge overview:

## Commands (23)

### Pipeline
| Command | Description |
|---------|-------------|
| `/forge:build` | Full 11-phase SDLC pipeline for greenfield apps |
| `/forge:add-feature` | Feature SDLC pipeline for existing apps |
| `/forge:resume` | Resume pipeline from last checkpoint |
| `/forge:design` | Spec interview only (no implementation) |
| `/forge:design-product` | Product spec design workflow |
| `/forge:design-architecture` | Architecture design workflow |

### Implementation
| Command | Description |
|---------|-------------|
| `/forge:just-do-it` | Quick build without spec ceremony |
| `/forge:build-unplanned` | Lightweight build with brief |
| `/forge:work-on` | Work on a specific task/story (TDD) |
| `/forge:work-on-next` | Pick next unblocked story |
| `/forge:create-tasks` | Create tasks from stories |

### Quality
| Command | Description |
|---------|-------------|
| `/forge:review` | 8-agent parallel gating review |
| `/forge:validate` | Full verification suite |
| `/forge:check` | 3-dimension alignment checks |

### Reverse Engineering
| Command | Description |
|---------|-------------|
| `/forge:source-architecture` | Architecture docs from code |
| `/forge:source-specs` | Specs from existing code |
| `/forge:spec-sync` | Bidirectional spec-code sync |

### Utilities
| Command | Description |
|---------|-------------|
| `/forge:init` | Scaffold project structure |
| `/forge:debug` | 5-phase debugging workflow |
| `/forge:refactor` | Targeted debt reduction |
| `/forge:create-pr` | Structured PR with story commits |
| `/forge:skills` | List all available skills |
| `/forge:help` | This help message |

2. Display agents summary (20 agents)
3. Display skills summary (22 skills)
4. Mention: "Run `/forge:skills` for detailed skill descriptions"
