AGENTS := -a claude-code -a codex
INSTALL := npx -y skills add . -g $(AGENTS) -y

.PHONY: add add-skill list test test-roadmap validate-roadmap capture-transcript

add:
	$(INSTALL)

add-skill:
	@test -n "$(SKILL)" || { echo "usage: make add-skill SKILL=<nome>"; exit 1; }
	$(INSTALL) -s $(SKILL)

list:
	npx -y skills add . -l

test: test-roadmap

test-roadmap:
	node --test skills/roadmap/scripts/*.test.ts

validate-roadmap:
	node skills/roadmap/scripts/validate_roadmap.ts $(ROADMAP)

capture-transcript:
	@test -n "$(RUN)" || { echo "usage: make capture-transcript RUN=<run directory>"; exit 1; }
	@test -d "$(RUN)" || { echo "$(RUN): not a directory"; exit 1; }
	@cp "$$(ls -t $(HOME)/.claude/projects/$$(pwd | sed 's|/|-|g')/*.jsonl | head -1)" "$(RUN)/TRANSCRIPT.jsonl"
	@echo "transcript -> $(RUN)/TRANSCRIPT.jsonl"
