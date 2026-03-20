# Cosmos-Reason2-8B Benchmark Report

For the cross-model summary that compares 2B and 8B, see [results.md](results.md).

## Executive summary

This report summarizes the benchmark results obtained for `nvidia/Cosmos-Reason2-8B` using `lmms-eval` with the `qwen3_vl` backend path.

The evaluation was carried out on a single NVIDIA RTX 4090 24 GB GPU. The primary goals were:

1. verify that `Cosmos-Reason2-8B` can be loaded through the `Qwen3-VL` interface,
2. confirm that `lmms-eval` can be used as the main evaluation harness for the 8B variant,
3. validate the setup with small smoke tests, and
4. measure model performance on `TextVQA`, `DocVQA`, and `MMBench`.

The overall pattern is clear: the model completes all three full benchmarks successfully, improves over the 2B variant on every reported metric, and is especially strong on `DocVQA`.

## Evaluation setup

| Item | Value |
| --- | --- |
| Model | `nvidia/Cosmos-Reason2-8B` |
| Evaluator | `lmms_eval` |
| Backend path | `qwen3_vl` |
| GPU | `NVIDIA GeForce RTX 4090 24 GB` |
| Python | `3.10.18` |
| `lmms-eval` commit | `88b23e2` |
| Common model args | `pretrained=nvidia/Cosmos-Reason2-8B,device_map=auto,attn_implementation=sdpa` |

Additional environment details, setup commands, and local patch information are documented in [reproduction.md](reproduction.md).

## Validation checks

| Check | Outcome |
| --- | --- |
| Direct `transformers` load probe | Success |
| Observed processor class | `Qwen3VLProcessor` |
| Observed model class | `Qwen3VLForConditionalGeneration` |
| GPU allocated after load probe | `17534319104` bytes |
| GPU reserved after load probe | `17555259392` bytes |
| `MMBench` smoke (`mmbench_en_dev_lite`, 8 samples) | Success, `100.0` |
| `DocVQA` smoke (`docvqa_val_lite`, 8 samples) | Success, `0.9095394736842105` |

These checks confirm that the 8B model can follow the same `Qwen3-VL` loading and `lmms-eval` evaluation path that was used for the 2B variant.

## Final benchmark results

| Benchmark | Task | Metric | Exact score | Table value | Effective samples |
| --- | --- | --- | ---: | ---: | ---: |
| TextVQA | `textvqa_val` | `exact_match` | `0.7946800000000042` | `79.47` | `5000` |
| DocVQA | `docvqa_val` | `ANLS` | `0.9425976346348114` | `94.26` | `5349` |
| MMBench | `mmbench_en_dev` | `gpt_eval_score` | `83.4192439862543` | `83.4` | `4329` |

## Throughput summary

| Benchmark | Total output tokens | Generation time (s) | Avg speed (tokens/s) |
| --- | ---: | ---: | ---: |
| TextVQA | `21364` | `1352.1935` | `15.7995` |
| DocVQA | `33318` | `5962.5170` | `5.5879` |
| MMBench | `8700` | `461.4259` | `18.8546` |

## Statistical notes

Where the benchmark emitted uncertainty estimates through `lmms-eval`, the following values were recorded:

- `TextVQA` `exact_match_stderr`: `0.005283703532996975`
- `DocVQA` `anls_stderr`: `0.0028426622917632287`
- `MMBench` does not report a standard stderr in this output format for `gpt_eval_score`

## Benchmark-by-benchmark discussion

### TextVQA

`Cosmos-Reason2-8B` achieved `79.47` on `textvqa_val`. Compared with the 2B variant, that is an improvement of roughly `+3.49` points and indicates stronger OCR-heavy open-ended question answering without changing the overall task family.

The score suggests that the 8B model is materially better than the 2B model on text-in-image QA, but the increase is still smaller than the jump observed on `MMBench`.

### DocVQA

`Cosmos-Reason2-8B` achieved `94.26` ANLS on `docvqa_val`, making `DocVQA` the strongest benchmark for the 8B variant as well.

This result reinforces the picture already visible in the 2B evaluation: document-centric visual QA is a particularly strong area for the Cosmos-Reason2 family in this setup. The 8B model pushes that already-strong region further upward by roughly `+3.09` points over the 2B variant.

On this hardware, the stable production configuration for the full 8B `DocVQA` run was `batch_size=1`.

### MMBench

`Cosmos-Reason2-8B` achieved `83.4` on `mmbench_en_dev`, improving over the 2B result by `+8.762886597938149` on the exact score.

This is the largest gain among the three benchmarks and materially changes the model's profile. The improvement is not only a matter of stronger recognition-heavy categories; it is also driven by visibly stronger performance on OCR, structured image-text understanding, spatial reasoning, and relation-heavy categories.

See [mmbench_breakdown.md](mmbench_breakdown.md) for the full 2B versus 8B category-level comparison.

## Comparison against Cosmos-Reason2-2B

| Benchmark | 2B exact | 8B exact | Absolute delta |
| --- | ---: | ---: | ---: |
| TextVQA | `0.7598200000000049` | `0.7946800000000042` | `+0.034859999999999225` |
| DocVQA | `0.9117385941613753` | `0.9425976346348114` | `+0.030859040473436128` |
| MMBench | `74.65635738831615` | `83.4192439862543` | `+8.762886597938149` |

Largest observed `MMBench` category gains versus 2B:

- `nature_relation`: `+35.417`
- `spatial_relationship`: `+31.111`
- `ocr`: `+20.513`
- `attribute_comparison`: `+20.454`
- `image_quality`: `+18.868`
- `physical_property_reasoning`: `+18.667`
- `structuralized_imagetext_understanding`: `+16.667`
- `future_prediction`: `+15.000`

## Main observations

- The 8B variant successfully follows the same evaluation path as the 2B model: direct `Qwen3-VL` interface loading, `lmms-eval` smoke validation, and then full evaluation on `MMBench`, `TextVQA`, and `DocVQA`.
- The 8B model improves over the 2B baseline on all three benchmarks on the same machine and software stack.
- The largest MMBench gains are concentrated in relation-heavy, OCR-adjacent, and structured visual reasoning categories, which suggests a deeper capability improvement than simple scaling of already-strong recognition categories.
- `DocVQA` remains the strongest benchmark for the 8B variant and is one of the strongest indicators that the family is especially effective on document-centric visual QA.

## Scope and limitations

- These results reflect a specific evaluation configuration built around `lmms-eval`, the `qwen3_vl` backend path, and a single RTX 4090 24 GB GPU.
- Some local task configuration patches were applied for public dataset access during evaluation. Those patches are documented in this repository.
- The repository intentionally omits raw `samples.jsonl`, full logs, and cache directories, so it should be read as a reproducible summary pack rather than a complete artifact archive.
- The 8B full runs in this repository were executed with `batch_size=1` on this hardware.
- Cross-model comparisons should be made carefully unless competing models were evaluated with the same task splits, prompts, backends, and software versions.

## Machine-readable summary

The corresponding machine-readable score summary is available in [scores.json](scores.json).
