AGENTS := -a claude-code -a codex
INSTALL := npx -y skills add . -g $(AGENTS) -y

.PHONY: add add-skill list test test-plan-slices test-roadmap validate validate-roadmap

add:
	$(INSTALL)

add-skill:
	@test -n "$(SKILL)" || { echo "usage: make add-skill SKILL=<nome>"; exit 1; }
	$(INSTALL) -s $(SKILL)

list:
	npx -y skills add . -l

test: test-plan-slices test-roadmap

test-plan-slices:
	cd skills/plan-slices/scripts && python3 -m unittest

test-roadmap:
	node --test skills/roadmap/scripts/validate_roadmap.test.ts

validate:
	@test -n "$(PLAN)" || { echo "usage: make validate PLAN=<plan.md>"; exit 2; }
	python3 skills/plan-slices/scripts/validate_plan.py $(PLAN)

validate-roadmap:
	node skills/roadmap/scripts/validate_roadmap.ts $(ROADMAP)
