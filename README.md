# Publishing Manager

A small publishing management CLI, built live to connect three weeks of material:

```text
Python objects -> object relationships -> application modules -> CLI -> external service
```

An author writes many books.
A book can have many authors.
The `Contract` between them carries a royalty percentage, which is a fact about the agreement rather than about either side.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m publishing_app.cli
```

The app runs with no API key and no network connection.

## What is in here

| Path | What it is |
|---|---|
| `publishing_app/` | The application. Three functions are left as `TODO` stubs and get written during the session. |
| `demos/` | Four standalone scripts covering one-to-many, many-to-many, association metadata, and where relationship logic belongs. |
| `AGENDA.md` | The 90-minute session plan. |
| `FACILITATOR.md` | The runsheet: what to type, when, and how to recover. |

## Branches

| Branch | `publishing_app/` contains |
|---|---|
| `main` | The starter, with three `TODO` stubs. This is the branch you build on. |
| `solution` | The finished application, plus the 33 tests that cover it. |

To keep the finished version on disk without it showing up in the folder you are working in:

```bash
git worktree add ../publishing-solution solution

cd ../publishing-solution
python -m publishing_app.cli
pytest -q
```

Or read one file from the branch without checking anything out:

```bash
git show solution:publishing_app/cli.py
```

## The three layers

```text
                 +--------------+
                 | External API |
                 +------^-------+
                        |
                  services.py
                        ^
                        |
User --> cli.py --> models.py
```

**`models.py`** owns the domain.
It knows how authors, books, publishers and contracts relate, and it enforces the rules that must hold no matter who creates an object.
A royalty is validated here because contracts also get created by seed data, scripts and tests, not only by the menu.

**`cli.py`** owns the conversation with the user.
It numbers lists, reads input, turns `"3"` into an object, and prints results.
It never loops over `Contract.all` to work out a relationship for itself.

**`services.py`** owns the boundary with the outside world.
It is the only module that imports `anthropic`, and every way a call can fail arrives back as a single `AIServiceError`.

## Running things

```bash
python -m publishing_app.cli     # the app
python demos/01_one_to_many.py   # concept demos
```

## AI briefs

Menu option 4 generates a publishing brief for the selected author.

With no `ANTHROPIC_API_KEY` set, `services.build_ai_client` returns an `AIClient` wrapping `EchoBackend`, which produces a canned brief offline.
Set a key to switch to the real API:

```bash
cp .env.example .env
# add your key to .env
pip install anthropic
```

Nothing else in the application changes.
That is the argument for the wrapper.

## Installing it as a command

The project is also packaged, which is the Pip/PyPI/scripting lab in miniature:

```bash
pip install -e .
publishing
```
