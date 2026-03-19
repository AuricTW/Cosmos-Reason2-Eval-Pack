# Cosmos-Reason2-2B Eval Pack

This folder is a sanitized export of the local evaluation work for `nvidia/Cosmos-Reason2-2B`.

## Final scores

| Benchmark | Metric | Exact | Table value |
| --- | --- | ---: | ---: |
| TextVQA | exact_match | `0.7598200000000049` | `75.98` |
| DocVQA | ANLS | `0.9117385941613753` | `91.17` |
| MMBench (`mmbench_en_dev`) | gpt_eval_score | `74.65635738831615` | `74.7` |

## Repo layout

- `docs/reproduction.md`: environment, commands, and run notes
- `docs/results.md`: final results summary and interpretation
- `scripts/load_vlm_probe.py`: direct `transformers` load probe for Qwen3-VL-compatible models
- `patches/lmms_eval_public_dataset_token_fix.patch`: patch used to make public MMBench/DocVQA datasets load without forcing HF token
- `patches/lmms_eval_qwen3_vl_oom_retry_experiment.patch`: experimental OOM fallback patch explored during DocVQA work

## Important note

The final official `DocVQA` score was produced with `batch_size=1` for stability on a single RTX 4090 24 GB card. The OOM retry patch is included for traceability, but it was not the final stability mechanism used for the official `DocVQA` number.
