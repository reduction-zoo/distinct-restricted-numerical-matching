# Research instructions

Read the [fixed question](campaigns/distinct-restricted-numerical-matching/question.md), [prior state](campaigns/distinct-restricted-numerical-matching/state.md) and [preparation notes](campaigns/distinct-restricted-numerical-matching/work/preparation.md). The fixed [test corpus](campaigns/distinct-restricted-numerical-matching/work/cases.json) and [verifier](campaigns/distinct-restricted-numerical-matching/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/distinct-restricted-numerical-matching/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
