# GitHub Copilot Custom Instructions

These instructions capture the **house style** and **best practices** observed in the `ai‑news‑updates` and `dew_agentic` Python projects. Copilot **must** follow them whenever it suggests or completes code inside this repository.
# GitHub Copilot Custom Instructions

These instructions capture the **house style** and **best practices** observed in the `ai‑news‑updates` and `dew_agentic` Python projects. Copilot **must** follow them whenever it suggests or completes code inside this repository.

---

## 1. General coding philosophy

* **Readable, maintainable, minimally clever.** Favour clarity over brevity; prefer the obvious implementation over “neat tricks”.
* Optimise for **testability** and **extensibility** (single‑responsibility functions, small modules).
* Keep modules **pure** where practical (no I/O in business‑logic functions).
* Treat data transformations as **pipelines** of pure functions.

---

## 2. Formatting

| Rule                                                                               | Example                                                            |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| 4‑space indentation, never tabs                                                    | `def func():\n    ...`                                             |
| Line length ≤ **88** characters (Black default)                                    | Break long expressions with implicit line continuation inside `()` |
| **Double quotes** for strings; single quotes only for apostrophes or nested quotes | `msg = "Hello world"`                                              |
| Use **f‑strings** for interpolation                                                | `f"Total: {total:,}"`                                              |
| Trailing commas in multi‑line literals                                             | `items = [\n    "a",\n    "b",\n]`                                 |

⚠️ Run **ruff** (`ruff check --fix .`) before committing.

---

## 3. Naming conventions

* `snake_case` for functions, variables, modules.
* `PascalCase` for classes & enums.
* `UPPER_SNAKE_CASE` for constants, config keys and SQL queries.
* Prefix private helpers with a leading underscore.
* Avoid ambiguous abbreviations; favour full UK‑English words (e.g. `colour`, `organisation`).

---

## 4. Imports

1. Standard library
2. Third‑party
3. Local packages (`from utils …`)

Separate each group with a blank line. Never use `import *`.

---

## 5. Docstrings

* Use **Google style** triple‑quoted docstrings (`"""Summary line.\n\nArgs: …\nReturns: …\nRaises: …"""`).
* First line is a short command‑style phrase (< 72 chars, ends with a full stop).
* Describe **units** (e.g., “seconds”), **side‑effects**, and **exceptions**.
* Write in UK English.

---

## 6. Type hints

* Add **PEP 484** type hints to **all** public functions, methods, and module‑level constants.
* Prefer `pathlib.Path` over `str` for file system paths.
* Use `typing.Optional`, `Union`, `Literal`, `TypedDict` where useful.
* Avoid `Any` unless unavoidable; document why.

---

## 7. Error handling & logging

* Always raise the **most specific** built‑in or custom exception.
* Group multiple exception types in a single `except` if the handling is identical.
* Log with the **`logging`** module (`logging.getLogger(__name__)`), not `print`.
* Use **structured, machine‑readable** log messages where possible.

---

## 8. I/O & resource management

* Use context managers (`with open(...) as f:`) for files, DB cursors and external resources.
* Isolate slow I/O behind **adapter** functions so they can be mocked in tests.
* Read and write text files using explicit `encoding="utf‑8"`.

---

## 9. Secrets & configuration

* Access secrets via **environment variables** or helper functions (`load_api_key()`).
* Keep file paths and toggles in **`config.yaml` / `toml`**; reference them through `utils.configloader`.
* Never commit credentials, tokens or personal data.

---

## 10. Testing

* Use **pytest**; place tests under `tests/` mirroring the source tree.
* Each test is a pure function starting with `test_`.
* Prefer **parameterised tests** (`@pytest.mark.parametrize`) over loops.
* Use **freezer** fixtures (`freezegun`) for date/time logic.
* Target **branch coverage ≥ 90 %**.

---

## 11. Third‑party libraries

| Scenario                 | Preferred library             |
| ------------------------ | ----------------------------- |
| Embeddings & chat models | `langchain‑openai`            |
| Vector store             | `qdrant‑client`               |
| Parsing feeds            | `feedparser`, `BeautifulSoup` |
| Data models              | `pydantic` v2                 |
| CLI                      | `typer`                       |

* Try to stay within the existing ecosystem before introducing new dependencies.

---

## 12. Project layout conventions

```text
<repo>/
 ├─ .github/copilot-instructions.md   ← **this file**
 ├─ pyproject.toml / requirements.txt
 ├─ src/
 │   └─ <package>/
 ├─ tests/
 ├─ data/                             ← large files → .gitignore
 └─ notebooks/                        ← exploratory, never imported
```

---

## 13. Commit etiquette

* Separate logical changes into atomic commits with clear, **imperative** summaries.
* Include “Closes #<issue>” where applicable.
* Run **pre‑commit** locally (ruff, black, isort) before pushing.

---

## 14. Generation tips for Copilot

* When completing a docstring, start with an **imperative verb** (“Return”, “Parse”, “Compute”).
* Use **typed dicts** or `dataclass` for structured data instead of naked tuples.
* Suggest **list comprehensions** or generator expressions where they improve readability.
* Offer **async** versions for I/O‑bound workflows but default to sync.
* Prefer **pathlib**, **datetime**, and **uuid** over legacy modules (`os.path`, `time`, `random`).
* Use \*\*contextlib.suppress`** or `ExitStack\` for complex cleanup scenarios.

---

## 15. Anti‑patterns to avoid

* `print()` debugging statements.
* Catch‑all `except Exception` without re‑raising.
* In‑line SQL build‑up with string concatenation — use **parameterised** queries.
* Hard‑coding file paths or magic numbers.
* Long, nested `if‑else` chains > 2 levels — extract helper functions.

---

*Last updated: 15 July 2025.*# GitHub Copilot Custom Instructions

These instructions capture the **house style** and **best practices** observed in the `ai‑news‑updates` and `dew_agentic` Python projects. Copilot **must** follow them whenever it suggests or completes code inside this repository.

---

## 1. General coding philosophy

* **Readable, maintainable, minimally clever.** Favour clarity over brevity; prefer the obvious implementation over “neat tricks”.
* Optimise for **testability** and **extensibility** (single‑responsibility functions, small modules).
* Keep modules **pure** where practical (no I/O in business‑logic functions).
* Treat data transformations as **pipelines** of pure functions.

---

## 2. Formatting

| Rule                                                                               | Example                                                            |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| 4‑space indentation, never tabs                                                    | `def func():\n    ...`                                             |
| Line length ≤ **88** characters (Black default)                                    | Break long expressions with implicit line continuation inside `()` |
| **Double quotes** for strings; single quotes only for apostrophes or nested quotes | `msg = "Hello world"`                                              |
| Use **f‑strings** for interpolation                                                | `f"Total: {total:,}"`                                              |
| Trailing commas in multi‑line literals                                             | `items = [\n    "a",\n    "b",\n]`                                 |

⚠️ Run **ruff** (`ruff check --fix .`) before committing.

---

## 3. Naming conventions

* `snake_case` for functions, variables, modules.
* `PascalCase` for classes & enums.
* `UPPER_SNAKE_CASE` for constants, config keys and SQL queries.
* Prefix private helpers with a leading underscore.
* Avoid ambiguous abbreviations; favour full UK‑English words (e.g. `colour`, `organisation`).

---

## 4. Imports

1. Standard library
2. Third‑party
3. Local packages (`from utils …`)

Separate each group with a blank line. Never use `import *`.

---

## 5. Docstrings

* Use **Google style** triple‑quoted docstrings (`"""Summary line.\n\nArgs: …\nReturns: …\nRaises: …"""`).
* First line is a short command‑style phrase (< 72 chars, ends with a full stop).
* Describe **units** (e.g., “seconds”), **side‑effects**, and **exceptions**.
* Write in UK English.

---

## 6. Type hints

* Add **PEP 484** type hints to **all** public functions, methods, and module‑level constants.
* Prefer `pathlib.Path` over `str` for file system paths.
* Use `typing.Optional`, `Union`, `Literal`, `TypedDict` where useful.
* Avoid `Any` unless unavoidable; document why.

---

## 7. Error handling & logging

* Always raise the **most specific** built‑in or custom exception.
* Group multiple exception types in a single `except` if the handling is identical.
* Log with the **`logging`** module (`logging.getLogger(__name__)`), not `print`.
* Use **structured, machine‑readable** log messages where possible.

---

## 8. I/O & resource management

* Use context managers (`with open(...) as f:`) for files, DB cursors and external resources.
* Isolate slow I/O behind **adapter** functions so they can be mocked in tests.
* Read and write text files using explicit `encoding="utf‑8"`.

---

## 9. Secrets & configuration

* Access secrets via **environment variables** or helper functions (`load_api_key()`).
* Keep file paths and toggles in **`config.yaml` / `toml`**; reference them through `utils.configloader`.
* Never commit credentials, tokens or personal data.

---

## 10. Testing

* Use **pytest**; place tests under `tests/` mirroring the source tree.
* Each test is a pure function starting with `test_`.
* Prefer **parameterised tests** (`@pytest.mark.parametrize`) over loops.
* Use **freezer** fixtures (`freezegun`) for date/time logic.
* Target **branch coverage ≥ 90 %**.

---

## 11. Third‑party libraries

| Scenario                 | Preferred library             |
| ------------------------ | ----------------------------- |
| Embeddings & chat models | `langchain‑openai`            |
| Vector store             | `qdrant‑client`               |
| Parsing feeds            | `feedparser`, `BeautifulSoup` |
| Data models              | `pydantic` v2                 |
| CLI                      | `typer`                       |

* Try to stay within the existing ecosystem before introducing new dependencies.

---

## 12. Project layout conventions

```text
<repo>/
 ├─ .github/copilot-instructions.md   ← **this file**
 ├─ pyproject.toml / requirements.txt
 ├─ src/
 │   └─ <package>/
 ├─ tests/
 ├─ data/                             ← large files → .gitignore
 └─ notebooks/                        ← exploratory, never imported
```

---

## 13. Commit etiquette

* Separate logical changes into atomic commits with clear, **imperative** summaries.
* Include “Closes #<issue>” where applicable.
* Run **pre‑commit** locally (ruff, black, isort) before pushing.

---

## 14. Generation tips for Copilot

* When completing a docstring, start with an **imperative verb** (“Return”, “Parse”, “Compute”).
* Use **typed dicts** or `dataclass` for structured data instead of naked tuples.
* Suggest **list comprehensions** or generator expressions where they improve readability.
* Offer **async** versions for I/O‑bound workflows but default to sync.
* Prefer **pathlib**, **datetime**, and **uuid** over legacy modules (`os.path`, `time`, `random`).
* Use \*\*contextlib.suppress`** or `ExitStack\` for complex cleanup scenarios.

---

## 15. Anti‑patterns to avoid

* `print()` debugging statements.
* Catch‑all `except Exception` without re‑raising.
* In‑line SQL build‑up with string concatenation — use **parameterised** queries.
* Hard‑coding file paths or magic numbers.
* Long, nested `if‑else` chains > 2 levels — extract helper functions.

---

*Last updated: 15 July 2025.*


---

## 1. General coding philosophy

* **Readable, maintainable, minimally clever.** Favour clarity over brevity; prefer the obvious implementation over “neat tricks”.
* Optimise for **testability** and **extensibility** (single‑responsibility functions, small modules).
* Keep modules **pure** where practical (no I/O in business‑logic functions).
* Treat data transformations as **pipelines** of pure functions.

---

## 2. Formatting

| Rule                                                                               | Example                                                            |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| 4‑space indentation, never tabs                                                    | `def func():\n    ...`                                             |
| Line length ≤ **88** characters (Black default)                                    | Break long expressions with implicit line continuation inside `()` |
| **Double quotes** for strings; single quotes only for apostrophes or nested quotes | `msg = "Hello world"`                                              |
| Use **f‑strings** for interpolation                                                | `f"Total: {total:,}"`                                              |
| Trailing commas in multi‑line literals                                             | `items = [\n    "a",\n    "b",\n]`                                 |

⚠️ Run **ruff** (`ruff check --fix .`) before committing.

---

## 3. Naming conventions

* `snake_case` for functions, variables, modules.
* `PascalCase` for classes & enums.
* `UPPER_SNAKE_CASE` for constants, config keys and SQL queries.
* Prefix private helpers with a leading underscore.
* Avoid ambiguous abbreviations; favour full UK‑English words (e.g. `colour`, `organisation`).

---

## 4. Imports

1. Standard library
2. Third‑party
3. Local packages (`from utils …`)

Separate each group with a blank line. Never use `import *`.

---

## 5. Docstrings

* Use **Google style** triple‑quoted docstrings (`"""Summary line.\n\nArgs: …\nReturns: …\nRaises: …"""`).
* First line is a short command‑style phrase (< 72 chars, ends with a full stop).
* Describe **units** (e.g., “seconds”), **side‑effects**, and **exceptions**.
* Write in UK English.

---

## 6. Type hints

* Add **PEP 484** type hints to **all** public functions, methods, and module‑level constants.
* Prefer `pathlib.Path` over `str` for file system paths.
* Use `typing.Optional`, `Union`, `Literal`, `TypedDict` where useful.
* Avoid `Any` unless unavoidable; document why.

---

## 7. Error handling & logging

* Always raise the **most specific** built‑in or custom exception.
* Group multiple exception types in a single `except` if the handling is identical.
* Log with the **`logging`** module (`logging.getLogger(__name__)`), not `print`.
* Use **structured, machine‑readable** log messages where possible.

---

## 8. I/O & resource management

* Use context managers (`with open(...) as f:`) for files, DB cursors and external resources.
* Isolate slow I/O behind **adapter** functions so they can be mocked in tests.
* Read and write text files using explicit `encoding="utf‑8"`.

---

## 9. Secrets & configuration

* Access secrets via **environment variables** or helper functions (`load_api_key()`).
* Keep file paths and toggles in **`config.yaml` / `toml`**; reference them through `utils.configloader`.
* Never commit credentials, tokens or personal data.

---

## 10. Testing

* Use **pytest**; place tests under `tests/` mirroring the source tree.
* Each test is a pure function starting with `test_`.
* Prefer **parameterised tests** (`@pytest.mark.parametrize`) over loops.
* Use **freezer** fixtures (`freezegun`) for date/time logic.
* Target **branch coverage ≥ 90 %**.

---

## 11. Third‑party libraries

| Scenario                 | Preferred library             |
| ------------------------ | ----------------------------- |
| Embeddings & chat models | `langchain‑openai`            |
| Vector store             | `qdrant‑client`               |
| Parsing feeds            | `feedparser`, `BeautifulSoup` |
| Data models              | `pydantic` v2                 |
| CLI                      | `typer`                       |

* Try to stay within the existing ecosystem before introducing new dependencies.

---

## 12. Project layout conventions

```text
<repo>/
 ├─ .github/copilot-instructions.md   ← **this file**
 ├─ pyproject.toml / requirements.txt
 ├─ src/
 │   └─ <package>/
 ├─ tests/
 ├─ data/                             ← large files → .gitignore
 └─ notebooks/                        ← exploratory, never imported
```

---

## 13. Commit etiquette

* Separate logical changes into atomic commits with clear, **imperative** summaries.
* Include “Closes #<issue>” where applicable.
* Run **pre‑commit** locally (ruff, black, isort) before pushing.

---

## 14. Generation tips for Copilot

* When completing a docstring, start with an **imperative verb** (“Return”, “Parse”, “Compute”).
* Use **typed dicts** or `dataclass` for structured data instead of naked tuples.
* Suggest **list comprehensions** or generator expressions where they improve readability.
* Offer **async** versions for I/O‑bound workflows but default to sync.
* Prefer **pathlib**, **datetime**, and **uuid** over legacy modules (`os.path`, `time`, `random`).
* Use \*\*contextlib.suppress`** or `ExitStack\` for complex cleanup scenarios.

---

## 15. Anti‑patterns to avoid

* `print()` debugging statements.
* Catch‑all `except Exception` without re‑raising.
* In‑line SQL build‑up with string concatenation — use **parameterised** queries.
* Hard‑coding file paths or magic numbers.
* Long, nested `if‑else` chains > 2 levels — extract helper functions.

---

*Last updated: 15 July 2025.*
