# Recipe app — Restructuring fixture

- **Sources:** Recipe-app goals and concepts.
- **Current state:** Greenfield.

## Ordering criteria

- Ship all add modes together because they write Recipe.

## Themes

| Theme | Desired outcome | First validation |
|---|---|---|
| Recipe capture | Members save recipes from URL, pasted text, or manual entry. | 1 |

## Cross-functional concerns

- **Authorization:** Cookbook membership scopes writes.
- **Validation and errors:** Validate extraction output.
- **Operability:** Log provider failures.
- **Accessibility and security:** Forms are keyboard accessible.
- **Data integrity and recovery:** Edit regenerates derived data.

## NOW

### 1. Every recipe input and recovery path *(Theme: Recipe capture)*

---

**Includes**

- Add URL extraction, pasted-text fallback, manual form, multiple photos, edit, and cover selection in one slice.

**Verification**

- Independently demonstrate URL, paywall fallback, manual entry, photo failure, correction, and cover changes.

**Learning / risk**

- Extraction quality, fallback demand, manual-form usability, and photo reliability change separate decisions.

**Outcome**

- Members can capture and correct recipes through every MVP mode.

## LATER

- None identified.

## OUT-OF-SCOPE

- **Ingredient parsing** — Sources deliberately retain free text.

