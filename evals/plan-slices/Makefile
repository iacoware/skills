SCENARIO ?= recipe-app
PLAN ?=
GRADER ?= codex
MODEL ?=
CODEX_MODEL ?=
CLAUDE_MODEL ?=
GRADE_TIMEOUT ?= 900
GRADE ?= $(patsubst %.md,%.$(GRADER).GRADE.json,$(PLAN))
SCORE ?= $(patsubst %.md,%.$(GRADER).SCORE.json,$(PLAN))
PROMPT ?= $(patsubst %.md,%.GRADE-PROMPT.md,$(PLAN))

ROOT := ../..
SCENARIO_DIR := $(SCENARIO)
RESULTS_DIR := $(SCENARIO_DIR)/results
REFERENCE := $(SCENARIO_DIR)/REFERENCE-PLAN.md
EXPECTATIONS := $(SCENARIO_DIR)/expectations.json
SOURCES := \
	$(SCENARIO_DIR)/sources/goal.md \
	$(SCENARIO_DIR)/sources/concepts.md \
	$(SCENARIO_DIR)/sources/arch-choices.md \
	$(SCENARIO_DIR)/sources/tech-choices.md
VALIDATOR := $(ROOT)/skills/plan-slices/scripts/validate_plan.py
EXPECTATIONS_TOOL := scripts/derive_expectations.py
GRADER_TOOL := scripts/grade_plan.py
RUBRIC := grader-rubric.json
MODEL_ARG := $(if $(strip $(MODEL)),--model "$(MODEL)",)

.PHONY: help test validate validate-structure expectations-check expectations-generate \
	grade grade-all grader-prompt grader-score require-plan require-grade

help:
	@echo "Plan-slices eval commands (SCENARIO defaults to recipe-app):"
	@echo "  make test"
	@echo "  make validate PLAN=PLAN-CX-CON-4.md"
	@echo "  make validate-structure PLAN=PLAN-CX-CON-4.md"
	@echo "  make expectations-check"
	@echo "  make expectations-generate"
	@echo "  make grade PLAN=PLAN-CX-CON-4.md GRADER=codex"
	@echo "  make grade PLAN=PLAN-CX-CON-4.md GRADER=claude"
	@echo "  make grade-all PLAN=PLAN-CX-CON-4.md"
	@echo "  make grader-prompt PLAN=PLAN-CX-CON-4.md"
	@echo "  make grader-score GRADE=PLAN-CX-CON-4.GRADE.json"

test:
	cd $(ROOT)/skills/plan-slices/scripts && python3 -m unittest
	cd scripts && python3 -m unittest
	$(MAKE) expectations-check

validate: require-plan expectations-check
	python3 $(VALIDATOR) $(RESULTS_DIR)/$(PLAN) --expectations $(EXPECTATIONS)

validate-structure: require-plan
	python3 $(VALIDATOR) $(RESULTS_DIR)/$(PLAN)

expectations-check:
	python3 $(EXPECTATIONS_TOOL) $(REFERENCE) $(EXPECTATIONS) --check

expectations-generate:
	python3 $(EXPECTATIONS_TOOL) $(REFERENCE) $(EXPECTATIONS)

grade: require-plan validate-structure
	python3 $(GRADER_TOOL) run \
		--provider $(GRADER) \
		--rubric $(RUBRIC) \
		--reference $(REFERENCE) \
		--plan $(RESULTS_DIR)/$(PLAN) \
		--sources $(SOURCES) \
		--grade-output $(RESULTS_DIR)/$(GRADE) \
		--score-output $(RESULTS_DIR)/$(SCORE) \
		--timeout $(GRADE_TIMEOUT) $(MODEL_ARG)

grade-all: require-plan
	$(MAKE) grade PLAN=$(PLAN) GRADER=codex MODEL="$(CODEX_MODEL)"
	$(MAKE) grade PLAN=$(PLAN) GRADER=claude MODEL="$(CLAUDE_MODEL)"

grader-prompt: require-plan
	@python3 $(GRADER_TOOL) prompt \
		--rubric $(RUBRIC) \
		--reference $(REFERENCE) \
		--plan $(RESULTS_DIR)/$(PLAN) \
		--sources $(SOURCES) > $(RESULTS_DIR)/$(PROMPT)
	@echo "WROTE: $(RESULTS_DIR)/$(PROMPT)"

grader-score: require-grade
	python3 $(GRADER_TOOL) score --rubric $(RUBRIC) $(RESULTS_DIR)/$(GRADE)

require-plan:
	@test -n "$(PLAN)" || { echo "usage: make <target> PLAN=<plan.md>"; exit 2; }

require-grade:
	@test -n "$(GRADE)" || { echo "usage: make grader-score GRADE=<grade.json>"; exit 2; }
