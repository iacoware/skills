AGENTS := -a claude-code -a codex
INSTALL := npx -y skills add . -g $(AGENTS) -y

.PHONY: add add-skill list test validate

add:
	$(INSTALL)

add-skill:
	@test -n "$(SKILL)" || { echo "usage: make add-skill SKILL=<nome>"; exit 1; }
	$(INSTALL) -s $(SKILL)

list:
	npx -y skills add . -l

test:
	cd skills/plan-slices/scripts && python3 -m unittest

validate:
	@test -n "$(PLAN)" || { echo "usage: make validate PLAN=<plan.md>"; exit 2; }
	python3 skills/plan-slices/scripts/validate_plan.py $(PLAN)
