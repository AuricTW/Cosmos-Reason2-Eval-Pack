# Cosmos-Reason2-2B Benchmark Report

For the cross-model summary that compares 2B and 8B, see [results.md](results.md).

## Executive summary

This report summarizes the benchmark results obtained for `nvidia/Cosmos-Reason2-2B` using `lmms-eval` with the `qwen3_vl` backend path.

The evaluation was carried out on a single NVIDIA RTX 4090 24 GB GPU. The primary goals were:

1. verify that `Cosmos-Reason2-2B` can be loaded through the `Qwen3-VL` interface,
2. confirm that `lmms-eval` can be used as the main evaluation harness, and
3. measure model performance on `TextVQA`, `DocVQA`, and `MMBench`.

The overall pattern is clear: the model is competitive across all three benchmarks, with the strongest relative performance appearing on `DocVQA`.

## Evaluation setup

| Item | Value |
| --- | --- |
| Model | `nvidia/Cosmos-Reason2-2B` |
| Evaluator | `lmms_eval` |
| Backend path | `qwen3_vl` |
| GPU | `NVIDIA GeForce RTX 4090 24 GB` |
| Python | `3.10.18` |
| `lmms-eval` commit | `88b23e2` |
| Common model args | `pretrained=nvidia/Cosmos-Reason2-2B,device_map=auto,attn_implementation=sdpa` |

Additional environment details, setup commands, and local patch information are documented in [reproduction.md](reproduction.md).

## Final benchmark results

| Benchmark | Task | Metric | Exact score | Table value | Effective samples |
| --- | --- | --- | ---: | ---: | ---: |
| TextVQA | `textvqa_val` | `exact_match` | `0.7598200000000049` | `75.98` | `5000` |
| DocVQA | `docvqa_val` | `ANLS` | `0.9117385941613753` | `91.17` | `5349` |
| MMBench | `mmbench_en_dev` | `gpt_eval_score` | `74.65635738831615` | `74.7` | `4329` |

## Throughput summary

| Benchmark | Total output tokens | Generation time (s) | Avg speed (tokens/s) |
| --- | ---: | ---: | ---: |
| TextVQA | `20696` | `732.0858` | `28.2699` |
| DocVQA | `32526` | `3159.7393` | `10.2939` |
| MMBench | `8761` | `351.7118` | `24.9096` |

## Statistical notes

Where the benchmark emitted uncertainty estimates through `lmms-eval`, the following values were recorded:

- `TextVQA` `exact_match_stderr`: `0.005638073349489148`
- `DocVQA` `anls_stderr`: `0.0035035279431835085`
- `MMBench` does not report a standard stderr in this output format for `gpt_eval_score`

## Benchmark-by-benchmark discussion

### TextVQA

`Cosmos-Reason2-2B` achieved `75.98` on `textvqa_val`. In this setup, that is a strong result for a small vision-language model and places the model in a competitive range on OCR-heavy open-ended question answering.

The result suggests that the model is not merely strong on structured document pages; it also transfers well to more general text-in-image question answering.

### DocVQA

`Cosmos-Reason2-2B` achieved `91.17` ANLS on `docvqa_val`, which is the strongest result among the three evaluated benchmarks in this project.

This is the clearest indicator in the current evaluation that the model is especially effective on document-centric visual question answering. It is also the benchmark that imposed the heaviest memory pressure during full evaluation on a single RTX 4090 24 GB GPU.

For full `DocVQA`, the stable production configuration on this hardware was `batch_size=1`. Higher batch sizes were explored during debugging but were not consistently reliable on this machine.

### MMBench

`Cosmos-Reason2-2B` achieved `74.7` on `mmbench_en_dev`. This result places the model in a competitive range on general multimodal perception and reasoning.

The total score alone does not fully describe the model's behavior. Category-level analysis shows a distinctly uneven but interpretable profile: the model is especially strong on recognition-heavy and scene-level tasks, while remaining noticeably weaker on spatial reasoning, forward prediction, and several fine-grained relation-heavy categories.

See [mmbench_breakdown.md](mmbench_breakdown.md) for the full category-level summary.

## Main observations

- The model loads successfully through the `Qwen3-VL` interface in both direct `transformers` probing and `lmms-eval`.
- The strongest relative result in this run is on `DocVQA`, suggesting a clear strength on document-style visual QA.
- `TextVQA` and `MMBench` are also strong, but the overall picture is better described as "very competitive across tasks, with a particular strength on document understanding" rather than "uniformly dominant on every benchmark."
- The `MMBench` profile indicates that the model is not simply good or bad across the board; instead, it has a recognizable capability shape with strong recognition and scene understanding, and weaker spatial and predictive reasoning.

## Scope and limitations

- These results reflect a specific evaluation configuration built around `lmms-eval`, the `qwen3_vl` backend path, and a single RTX 4090 24 GB GPU.
- Some local task configuration patches were applied for public dataset access during evaluation. Those patches are documented in this repository.
- The repository intentionally omits raw `samples.jsonl`, full logs, and cache directories, so it should be read as a reproducible summary pack rather than a complete artifact archive.
- Cross-model comparisons should be made carefully unless competing models were evaluated with the same task splits, prompts, backends, and software versions.

## Machine-readable summary

The corresponding machine-readable score summary is available in [scores.json](scores.json).
