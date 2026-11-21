# Contribuindo

## Branches
- `main`: produção, protegida. `develop`: integração.
- `feature/<nome>` e `fix/<nome>` partem de `develop`.

## Commits
Conventional Commits: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`.
Exemplo: `feat(lancamentos): adiciona resumo mensal`.

## Proteção da `main` (GitHub: Settings > Branches > Rules)
- Exigir pull request com ao menos 1 aprovação de revisão.
- Exigir checks de CI verdes (ruff, black, mypy, pytest).
- Bloquear force push e exclusão da branch.

## Definição de Pronto (DoD)
Veja o template de PR. Toda consulta deve filtrar por `familia_id`.
