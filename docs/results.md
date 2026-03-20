# Benchmark Summary

## Executive summary

This repository now records two end-to-end evaluations:

- `nvidia/Cosmos-Reason2-2B`
- `nvidia/Cosmos-Reason2-8B`

Both were evaluated through `lmms-eval` using the `qwen3_vl` backend path on the same single-GPU machine. The purpose of this summary is to show the common setup, the final benchmark matrix, and the main performance differences between the two variants.

The high-level pattern is consistent across all reported results:

- both models load successfully through the `Qwen3-VL` interface,
- both complete `TextVQA`, `DocVQA`, and `MMBench`,
- the 8B model improves over the 2B model on all three benchmarks, and
- `DocVQA` is the strongest benchmark for both variants in this setup.

## Common evaluation setup

| Item | Value |
| --- | --- |
| Evaluator | `lmms_eval` |
| Backend path | `qwen3_vl` |
| GPU | `NVIDIA GeForce RTX 4090 24 GB` |
| Python | `3.10.18` |
| `lmms-eval` commit | `88b23e2` |
| Common model args pattern | `pretrained=<MODEL_ID>,device_map=auto,attn_implementation=sdpa` |

Additional environment details, setup commands, and local patch information are documented in [reproduction.md](reproduction.md).

## Final benchmark matrix

| Model | TextVQA exact | TextVQA table | DocVQA exact | DocVQA table | MMBench exact | MMBench table |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `Cosmos-Reason2-2B` | `0.7598200000000049` | `75.98` | `0.9117385941613753` | `91.17` | `74.65635738831615` | `74.7` |
| `Cosmos-Reason2-8B` | `0.7946800000000042` | `79.47` | `0.9425976346348114` | `94.26` | `83.4192439862543` | `83.4` |

## Effective sample counts

| Model | TextVQA | DocVQA | MMBench |
| --- | ---: | ---: | ---: |
| `Cosmos-Reason2-2B` | `5000` | `5349` | `4329` |
| `Cosmos-Reason2-8B` | `5000` | `5349` | `4329` |

## Throughput summary

| Model | Benchmark | Total output tokens | Generation time (s) | Avg speed (tokens/s) |
| --- | --- | ---: | ---: | ---: |
| `Cosmos-Reason2-2B` | `TextVQA` | `20696` | `732.0858` | `28.2699` |
| `Cosmos-Reason2-2B` | `DocVQA` | `32526` | `3159.7393` | `10.2939` |
| `Cosmos-Reason2-2B` | `MMBench` | `8761` | `351.7118` | `24.9096` |
| `Cosmos-Reason2-8B` | `TextVQA` | `21364` | `1352.1935` | `15.7995` |
| `Cosmos-Reason2-8B` | `DocVQA` | `33318` | `5962.5170` | `5.5879` |
| `Cosmos-Reason2-8B` | `MMBench` | `8700` | `461.4259` | `18.8546` |

## Cross-model deltas

| Benchmark | 2B exact | 8B exact | Absolute delta |
| --- | ---: | ---: | ---: |
| `TextVQA` | `0.7598200000000049` | `0.7946800000000042` | `+0.034859999999999225` |
| `DocVQA` | `0.9117385941613753` | `0.9425976346348114` | `+0.030859040473436128` |
| `MMBench` | `74.65635738831615` | `83.4192439862543` | `+8.762886597938149` |

Rounded into the same table style used in many benchmark summaries, that corresponds to:

- `TextVQA`: `+3.49` points
- `DocVQA`: `+3.09` points
- `MMBench`: `+8.76` points using exact scores, or `+8.7` when subtracting the rounded table values

## Interpretation

### TextVQA

The 8B model improves `TextVQA` by about `3.49` points over the 2B model. That is a meaningful gain, but it is not the largest shift in this comparison. The result suggests that the 8B model improves OCR-heavy open-ended QA without radically changing the model's overall task profile.

### DocVQA

`DocVQA` is the strongest benchmark for both models:

- `Cosmos-Reason2-2B`: `91.17`
- `Cosmos-Reason2-8B`: `94.26`

This reinforces the view that the Cosmos-Reason2 family is especially effective on document-centric visual question answering in the evaluated setup. The 8B model strengthens an already-strong area rather than opening a completely new capability region.

### MMBench

The biggest improvement appears on `MMBench`, where the 8B model gains `+8.76` over the 2B model. This is large enough that it materially changes how the model should be characterized.

The improvement is not driven only by already-strong recognition categories. Category-level analysis shows especially large gains in:

- `nature_relation`
- `spatial_relationship`
- `ocr`
- `attribute_comparison`
- `image_quality`
- `physical_property_reasoning`
- `structuralized_imagetext_understanding`

That pattern suggests the 8B model is meaningfully better than the 2B model on relation-heavy reasoning and structured visual understanding, not merely on basic perception.

## Recommended reading

- For the dedicated 2B report, see [results_2b.md](results_2b.md).
- For the dedicated 8B report, see [results_8b.md](results_8b.md).
- For the category-level `MMBench` comparison, see [mmbench_breakdown.md](mmbench_breakdown.md).
- For setup and rerun commands, see [reproduction.md](reproduction.md).

## Scope and limitations

- These results reflect a specific evaluation configuration built around `lmms-eval`, the `qwen3_vl` backend path, and a single RTX 4090 24 GB GPU.
- Some local task configuration patches were applied for public dataset access during evaluation. Those patches are documented in this repository.
- The repository intentionally omits raw `samples.jsonl`, full logs, and cache directories, so it should be read as a reproducible summary pack rather than a complete artifact archive.
- Cross-model comparisons should be made carefully unless competing models were evaluated with the same task splits, prompts, backends, and software versions.

## Machine-readable summary

The corresponding machine-readable score summary is available in [scores.json](scores.json).
