# Codex instructions

This repository is a FastAPI modular-monolith boilerplate.

## Work style

- Keep the app as a single deployable service.
- Organize new features under `app/modules/<feature>/`.
- Keep HTTP concerns in routers, business logic in services, and persistence behind repositories.
- Keep response shape consistent: `{ ok, data, requestId }` for success and `{ ok, error, requestId }` for errors.
- Add or update tests for each behavior change.

## Commands

```bash
make install
make check
make dev
```

## Before finishing a change

Run:

```bash
ruff check .
mypy app tests
pytest
```
