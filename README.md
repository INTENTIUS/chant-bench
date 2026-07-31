# chant-bench

Benchmarks for agentic infrastructure — how much does the tool an agent is
holding help it answer questions about the estate it built?

A static docs site. Results are generated from the published result sets rather
than written by hand.

```sh
uv tool install mkdocs --with mkdocs-material   # once
python3 scripts/validate_results.py             # results satisfy the contract
python3 scripts/build_pages.py                  # regenerate the results pages
mkdocs serve                                    # preview
```

- `results/` — one JSON per run, the contract everything else derives from
- `briefings/` — the exact prompt each arm's agent receives, published verbatim
- `scripts/` — validation and page generation
- `PLAN.md` — the design, and why each decision was made

Benchmarks and scenarios are not ours: [aws-bench](https://github.com/aws-bench/aws-bench)
defines the estates, questions, reference answers and judge.
