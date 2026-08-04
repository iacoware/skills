AGENTS := -a claude-code -a codex
INSTALL := npx -y skills add . -g $(AGENTS) -y

.PHONY: add add-skill list test

add:
	$(INSTALL)

add-skill:
	@test -n "$(SKILL)" || { echo "usage: make add-skill SKILL=<nome>"; exit 1; }
	$(INSTALL) -s $(SKILL)

list:
	npx -y skills add . -l

test:
	cd skills/plan-slices/scripts && python3 -m unittest
	cd evals/plan-slices/scripts && python3 -m unittest
