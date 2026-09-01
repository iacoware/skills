AGENTS := -a claude-code -a codex
INSTALL := npx -y skills add . -g $(AGENTS) -y

.PHONY: add add-skill list test test-roadmap test-evals validate-roadmap capture-transcript run-metrics capture-run \
	eval-cycle eval-run eval-review eval-improve eval-noise

add:
	$(INSTALL)

add-skill:
	@test -n "$(SKILL)" || { echo "usage: make add-skill SKILL=<nome>"; exit 1; }
	$(INSTALL) -s $(SKILL)

list:
	npx -y skills add . -l

test: test-roadmap test-evals

test-roadmap:
	node --test skills/roadmap/scripts/*.test.ts

test-evals:
	node --test evals/roadmap/scripts/*.test.ts

validate-roadmap:
	node skills/roadmap/scripts/validate_roadmap.ts $(ROADMAP)

capture-transcript:
	@test -n "$(RUN)" || { echo "usage: make capture-transcript RUN=<run directory>"; exit 1; }
	@test -d "$(RUN)" || { echo "$(RUN): not a directory"; exit 1; }
	@cp "$$(ls -t $(HOME)/.claude/projects/$$(pwd | sed 's|/|-|g')/*.jsonl | head -1)" "$(RUN)/TRANSCRIPT.jsonl"
	@echo "transcript -> $(RUN)/TRANSCRIPT.jsonl"

run-metrics:
	@test -n "$(RUN)" || { echo "usage: make run-metrics RUN=<run directory>"; exit 1; }
	@node evals/roadmap/scripts/run_metrics.ts "$(RUN)"

# Sequential by hand rather than as prerequisites: under -j make is free to reorder those, and the
# metrics would be read off whatever transcript the directory held before the run.
capture-run:
	@test -n "$(RUN)" || { echo "usage: make capture-run RUN=<run directory>"; exit 1; }
	@$(MAKE) --no-print-directory capture-transcript RUN="$(RUN)"
	@$(MAKE) --no-print-directory run-metrics RUN="$(RUN)"

MODEL ?= opus
EFFORT ?= high
CYCLE := node evals/roadmap/scripts/run_cycle.ts --model $(MODEL) --effort $(EFFORT)

# Il disegno, la sua review e le proposte, in tre sessioni a contesto vuoto. L'autorizzazione si
# chiede una volta sola davanti all'elenco dei tre passi, che è quel che `evals/AGENTS.md` richiede.
eval-cycle:
	@$(CYCLE) --step cycle

eval-run:
	@$(CYCLE) --step run

eval-review:
	@test -n "$(RUN)" || { echo "usage: make eval-review RUN=<run directory>"; exit 1; }
	@$(CYCLE) --step review --run "$(RUN)"

# Prezzamento del rumore (design/roadmap/EVAL-NOISE.md): genera i satelliti *mancanti* del run
# principale — B e C, gemelli su stessa skill, prompt, modello ed effort — poi scrive NOISE.md.
# Rilanciabile: se i satelliti ci sono, rigenera solo l'analisi.
eval-noise:
	@test -n "$(RUN)" || { echo "usage: make eval-noise RUN=<run directory del principale>"; exit 1; }
	@$(CYCLE) --step noise --run "$(RUN)"

# `eval-cycle` lo fa già come terzo passo: questo target serve a rifarlo su un run esistente, o a
# farlo girare su un run più vecchio dopo un cambiamento al prompt.
eval-improve:
	@test -n "$(RUN)" || { echo "usage: make eval-improve RUN=<run directory>"; exit 1; }
	@$(CYCLE) --step improve --run "$(RUN)"
