# Cosmos-Reason2 Evaluation Pack

This repository documents a reproducible evaluation workflow for `nvidia/Cosmos-Reason2-2B` and `nvidia/Cosmos-Reason2-8B` using `lmms-eval` and the `Qwen3-VL` model interface.

The repository name retains the original `2B` label for continuity, but the documentation now covers both evaluated model variants.

The focus of this project is practical reproducibility: it records the environment, patches, model-loading path, benchmark commands, and final scores needed to understand and reproduce the evaluation without shipping a large artifact dump.

## Overview

- Models: `nvidia/Cosmos-Reason2-2B`, `nvidia/Cosmos-Reason2-8B`
- Evaluation framework: `lmms-eval`
- Backend path: `qwen3_vl`
- Hardware used: 1x NVIDIA RTX 4090 24 GB
- Main outcome: both models load successfully through the `Qwen3-VL` interface, and the 8B variant improves over the 2B variant on `TextVQA`, `DocVQA`, and `MMBench`

## Final results

| Model | TextVQA | DocVQA | MMBench |
| --- | ---: | ---: | ---: |
| `Cosmos-Reason2-2B` | `75.98` | `91.17` | `74.7` |
| `Cosmos-Reason2-8B` | `79.47` | `94.26` | `83.4` |
| `8B - 2B` delta | `+3.49` | `+3.09` | `+8.76` |

Deltas are computed from the exact scores before the displayed table values are rounded.

## Key observations

- Both `Cosmos-Reason2-2B` and `Cosmos-Reason2-8B` load successfully through the `Qwen3-VL` interface in direct `transformers` probing and in `lmms-eval`.
- `DocVQA` is the strongest benchmark for both variants in this evaluation setup.
- `Cosmos-Reason2-8B` improves on every reported benchmark, with the largest gain appearing on `MMBench`.
- The 8B `MMBench` gains are concentrated in OCR, structured image-text understanding, spatial reasoning, and relation-heavy categories rather than only in already-strong recognition categories.

## Repository guide

- [docs/results.md](docs/results.md)
  Cross-model benchmark summary comparing 2B and 8B.
- [docs/results_2b.md](docs/results_2b.md)
  Dedicated benchmark report for `nvidia/Cosmos-Reason2-2B`.
- [docs/results_8b.md](docs/results_8b.md)
  Dedicated benchmark report for `nvidia/Cosmos-Reason2-8B`.
- [docs/reproduction.md](docs/reproduction.md)
  Technical appendix with environment details, installation steps, patches, and rerun commands for both variants.
- [docs/mmbench_breakdown.md](docs/mmbench_breakdown.md)
  Category-level `MMBench` comparison between 2B and 8B.
- [docs/scores.json](docs/scores.json)
  Machine-readable score summary for downstream reuse.
- [scripts/load_vlm_probe.py](scripts/load_vlm_probe.py)
  Minimal `transformers`-based probe script for testing Qwen3-VL-compatible model loading.
- [patches/lmms_eval_public_dataset_token_fix.patch](patches/lmms_eval_public_dataset_token_fix.patch)
  Local `lmms-eval` task patch for public MMBench and DocVQA dataset access.
- [patches/lmms_eval_qwen3_vl_oom_retry_experiment.patch](patches/lmms_eval_qwen3_vl_oom_retry_experiment.patch)
  Experimental OOM fallback patch kept for traceability.

## Reproduction quick start

```bash
git clone https://github.com/AuricTW/Cosmos-Reason2-2B-Eval-Pack.git
cd Cosmos-Reason2-2B-Eval-Pack
```

Recommended reading order:

1. Start with [docs/results.md](docs/results.md) for the cross-model outcome and interpretation.
2. Use [docs/results_8b.md](docs/results_8b.md) or [docs/results_2b.md](docs/results_2b.md) for variant-specific details.
3. Refer to [docs/reproduction.md](docs/reproduction.md) for environment setup and rerun commands.
4. Refer to [docs/mmbench_breakdown.md](docs/mmbench_breakdown.md) for category-level comparison.

## Scope and limitations

- This repository is a reproducible evaluation pack, not a full raw artifact dump.
- Raw `samples.jsonl`, full terminal logs, local caches, and cloned third-party source trees are intentionally omitted to keep the repo lightweight and easier to share.
- The official full runs reported here were executed on a single RTX 4090 24 GB GPU with conservative settings. The 8B runs used `batch_size=1` throughout, and the 2B `DocVQA` run also used `batch_size=1` as the stable setting.
- The public-dataset token patch is part of the documented setup and should be treated as part of the reproduced evaluation environment.
- Cross-model comparisons are strongest when competing models are evaluated with the same task splits, prompts, backends, and software versions.
