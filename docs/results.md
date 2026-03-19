# Results Summary

## Model and setup

- Model: `nvidia/Cosmos-Reason2-2B`
- Evaluator: `lmms_eval`
- Backend path: `qwen3_vl`
- GPU: NVIDIA GeForce RTX 4090 24 GB
- Python: `3.10.18`
- `lmms-eval` commit: `88b23e2`

## Final scores

| Benchmark | Task | Metric | Exact score | Table value |
| --- | --- | --- | ---: | ---: |
| TextVQA | `textvqa_val` | `exact_match` | `0.7598200000000049` | `75.98` |
| DocVQA | `docvqa_val` | `anls` | `0.9117385941613753` | `91.17` |
| MMBench | `mmbench_en_dev` | `gpt_eval_score` | `74.65635738831615` | `74.7` |

## Short interpretation

- `DocVQA` is the standout result for this model.
- `TextVQA` is strong and competitive with other small-to-mid-size VLMs, but not an extreme outlier.
- `MMBench` is also strong, but sits in the top tier rather than far above the field.

## Practical takeaway

The overall pattern is not "the model dominates every benchmark." A more accurate summary is:

`Cosmos-Reason2-2B` is especially strong on document-style visual QA, while remaining competitive on general VQA and MMBench.
