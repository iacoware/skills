SCENARIO ?= recipe-app
PLAN ?=
PLANS ?=
BEFORE ?=
AFTER ?=
PROVIDER ?= both
CODEX_MODEL ?= gpt-5.6-sol
CODEX_EFFORT ?= high
CLAUDE_MODEL ?= claude-opus-5
CLAUDE_EFFORT ?= high
TIMEOUT ?= 900
DRY_RUN ?=
RESUME ?=
CONFIRM_SEND ?=
SKILL_COMMITS ?=
SHARD_COUNT ?=
SHARD_INDEX ?=

ROOT := ../..
SCENARIO_DIR := $(SCENARIO)
RESULTS_DIR := $(SCENARIO_DIR)/results
V3_RESULTS_DIR := $(RESULTS_DIR)/calibration-v3
BRIEF := $(SCENARIO_DIR)/EVALUATION-BRIEF.md
SOURCES := \
	$(SCENARIO_DIR)/sources/goal.md \
	$(SCENARIO_DIR)/sources/concepts.md \
	$(SCENARIO_DIR)/sources/arch-choices.md \
	$(SCENARIO_DIR)/sources/tech-choices.md
RUBRIC := grader-rubric.v3.json
FIXTURE_MANIFEST ?= fixtures/manifest.v3.json
CALIBRATION_REPORT ?= $(V3_RESULTS_DIR)/CALIBRATION.v3.json
CRITICAL_CALIBRATION_REPORT ?= $(V3_RESULTS_DIR)/CALIBRATION-CRITICAL.v3.json

VALIDATOR := $(ROOT)/skills/plan-slices/scripts/validate_plan.py
IMPROVEMENT_VALIDATOR := scripts/consensus/validate_improvement.py
CLAUSE_MAP_TOOL := scripts/consensus/extract_clause_map.py
ORCHESTRATOR_TOOL := scripts/orchestrate_grading.py
IMPROVEMENT ?=

ENABLED_VALUES := 1 true yes
DRY_RUN_ARG = $(if $(filter $(ENABLED_VALUES),$(DRY_RUN)),--dry-run,)
RESUME_ARG = $(if $(filter $(ENABLED_VALUES),$(RESUME)),--resume,)
CONFIRM_SEND_ARG = $(if $(filter $(ENABLED_VALUES),$(CONFIRM_SEND)),--confirm-send,)
SKILL_COMMIT_ARGS = $(foreach commit,$(SKILL_COMMITS),--candidate-skill-commit "$(commit)")
COMMON_ARGS = \
	$(foreach source,$(SOURCES),--source "$(source)") \
	--brief "$(BRIEF)" \
	--rubric "$(RUBRIC)" \
	--output-dir "$(V3_RESULTS_DIR)" \
	--codex-model "$(CODEX_MODEL)" \
	--codex-effort "$(CODEX_EFFORT)" \
	--claude-model "$(CLAUDE_MODEL)" \
	--claude-effort "$(CLAUDE_EFFORT)" \
	--timeout "$(TIMEOUT)" \
	$(SKILL_COMMIT_ARGS) \
	$(DRY_RUN_ARG) \
	$(RESUME_ARG) \
	$(CONFIRM_SEND_ARG)

.PHONY: help test validate validate-improvement clause-map \
	grade compare calibrate calibrate-critical calibrate-critical-report \
	require-orchestrator require-plan require-plans require-comparison require-improvement

help:
	@echo "Plan-slices evaluation commands (SCENARIO defaults to recipe-app):"
	@echo "  make grade PLANS='PLAN-CX-5.md PLAN-CC-5.md' DRY_RUN=1"
	@echo "  make compare BEFORE=PLAN-CX-5.md AFTER=PLAN-CX-6.md DRY_RUN=1"
	@echo "  make calibrate DRY_RUN=1"
	@echo "  make calibrate-critical DRY_RUN=1  # 36 absolute calls; no paired/adjudication"
	@echo "  make calibrate-critical DRY_RUN=1 SHARD_COUNT=4 SHARD_INDEX=1"
	@echo "  make calibrate-critical-report  # offline join; requires all 36 raw artifacts"
	@echo "  Add RESUME=1 to verify and reuse existing artifacts."
	@echo "  Add CONFIRM_SEND=1 only after reviewing dry-run output."
	@echo "  make validate PLAN=PLAN-CX-5.md"
	@echo "  make validate-improvement IMPROVEMENT=PLAN-CC-CON-6.IMPROVEMENT.md"
	@echo "  make clause-map  # regenerate support/clause-row-map.tsv from the map"
	@echo "  make test"

test:
	cd $(ROOT)/skills/plan-slices/scripts && python3 -m unittest
	cd scripts && python3 -m unittest

validate: require-plan
	python3 $(VALIDATOR) $(RESULTS_DIR)/$(PLAN)

validate-improvement: require-improvement
	python3 $(IMPROVEMENT_VALIDATOR) $(RESULTS_DIR)/$(IMPROVEMENT)

clause-map:
	python3 $(CLAUSE_MAP_TOOL)

grade: require-orchestrator require-plans
	python3 $(ORCHESTRATOR_TOOL) grade \
		$(addprefix $(RESULTS_DIR)/,$(PLANS)) \
		--provider "$(PROVIDER)" \
		$(COMMON_ARGS)

compare: require-orchestrator require-comparison
	python3 $(ORCHESTRATOR_TOOL) compare \
		"$(RESULTS_DIR)/$(BEFORE)" \
		"$(RESULTS_DIR)/$(AFTER)" \
		--provider "$(PROVIDER)" \
		$(COMMON_ARGS)

calibrate: require-orchestrator
	python3 $(ORCHESTRATOR_TOOL) calibrate \
		--manifest "$(FIXTURE_MANIFEST)" \
		--report-output "$(CALIBRATION_REPORT)" \
		$(COMMON_ARGS)

calibrate-critical: require-orchestrator
	python3 $(ORCHESTRATOR_TOOL) calibrate \
		--manifest "$(FIXTURE_MANIFEST)" \
		--report-output "$(CRITICAL_CALIBRATION_REPORT)" \
		--critical-subset \
		$(if $(SHARD_COUNT),--shard-count "$(SHARD_COUNT)",) \
		$(if $(SHARD_INDEX),--shard-index "$(SHARD_INDEX)",) \
		$(COMMON_ARGS)

calibrate-critical-report: require-orchestrator
	python3 $(ORCHESTRATOR_TOOL) calibrate \
		--manifest "$(FIXTURE_MANIFEST)" \
		--report-output "$(CRITICAL_CALIBRATION_REPORT)" \
		--critical-subset \
		--report-only \
		--resume \
		$(filter-out --resume,$(COMMON_ARGS))

require-orchestrator:
	@test -f "$(ORCHESTRATOR_TOOL)" || { \
		echo "ERROR: $(ORCHESTRATOR_TOOL) is not implemented yet"; \
		exit 2; \
	}

require-plan:
	@test -n "$(PLAN)" || { echo "usage: make validate PLAN=<plan.md>"; exit 2; }

require-improvement:
	@test -n "$(IMPROVEMENT)" || { \
		echo "usage: make validate-improvement IMPROVEMENT=<plan.IMPROVEMENT.md>"; \
		exit 2; \
	}

require-plans:
	@test -n "$(PLANS)" || { echo "usage: make grade PLANS='<plan.md> [plan.md ...]'"; exit 2; }

require-comparison:
	@test -n "$(BEFORE)" && test -n "$(AFTER)" || { \
		echo "usage: make compare BEFORE=<before.md> AFTER=<after.md>"; \
		exit 2; \
	}
