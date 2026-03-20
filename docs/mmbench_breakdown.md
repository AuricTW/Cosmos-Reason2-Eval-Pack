# MMBench Breakdown and 2B-to-8B Comparison

## Overview

This document summarizes the category-level `MMBench` performance observed for `nvidia/Cosmos-Reason2-2B` and `nvidia/Cosmos-Reason2-8B` on `mmbench_en_dev`.

Overall scores:

| Model | Exact score | Table value |
| --- | ---: | ---: |
| `Cosmos-Reason2-2B` | `74.65635738831615` | `74.7` |
| `Cosmos-Reason2-8B` | `83.4192439862543` | `83.4` |

The exact-score delta is:

- `83.4192439862543 - 74.65635738831615 = +8.762886597938149`

## Category-level accuracy

| Category | 2B | 8B | Delta (8B - 2B) |
| --- | ---: | ---: | ---: |
| action_recognition | `94.444` | `94.444` | `+0.000` |
| attribute_comparison | `59.091` | `79.545` | `+20.454` |
| attribute_recognition | `90.541` | `95.946` | `+5.405` |
| celebrity_recognition | `88.889` | `92.929` | `+4.040` |
| function_reasoning | `83.544` | `86.076` | `+2.532` |
| future_prediction | `40.000` | `55.000` | `+15.000` |
| identity_reasoning | `97.778` | `97.778` | `+0.000` |
| image_emotion | `88.000` | `84.000` | `-4.000` |
| image_quality | `54.717` | `73.585` | `+18.868` |
| image_scene | `97.115` | `96.154` | `-0.961` |
| image_style | `88.679` | `90.566` | `+1.887` |
| image_topic | `88.889` | `91.667` | `+2.778` |
| nature_relation | `52.083` | `87.500` | `+35.417` |
| object_localization | `60.494` | `64.198` | `+3.704` |
| ocr | `71.795` | `92.308` | `+20.513` |
| physical_property_reasoning | `60.000` | `78.667` | `+18.667` |
| physical_relation | `62.500` | `58.333` | `-4.167` |
| social_relation | `86.047` | `86.047` | `+0.000` |
| spatial_relationship | `26.667` | `57.778` | `+31.111` |
| structuralized_imagetext_understanding | `60.256` | `76.923` | `+16.667` |

## Strongest categories by model

### Cosmos-Reason2-2B

The strongest categories in the 2B run were:

- `identity_reasoning`: `97.778`
- `image_scene`: `97.115`
- `action_recognition`: `94.444`
- `attribute_recognition`: `90.541`

### Cosmos-Reason2-8B

The strongest categories in the 8B run were:

- `identity_reasoning`: `97.778`
- `image_scene`: `96.154`
- `attribute_recognition`: `95.946`
- `action_recognition`: `94.444`

The strongest regions remain recognition-heavy, but the 8B model broadens that strength into more reasoning-heavy categories than the 2B model managed.

## Weakest categories by model

### Cosmos-Reason2-2B

The weakest categories in the 2B run were:

- `spatial_relationship`: `26.667`
- `future_prediction`: `40.000`
- `nature_relation`: `52.083`
- `image_quality`: `54.717`

### Cosmos-Reason2-8B

The weakest categories in the 8B run were:

- `future_prediction`: `55.000`
- `spatial_relationship`: `57.778`
- `physical_relation`: `58.333`
- `object_localization`: `64.198`

Even where the 8B model still has weaker categories, the overall floor is noticeably higher than in the 2B run.

## Largest gains

The biggest improvements from 2B to 8B were:

- `nature_relation`: `+35.417`
- `spatial_relationship`: `+31.111`
- `ocr`: `+20.513`
- `attribute_comparison`: `+20.454`
- `image_quality`: `+18.868`
- `physical_property_reasoning`: `+18.667`
- `structuralized_imagetext_understanding`: `+16.667`
- `future_prediction`: `+15.000`

These are not only "easy recognition" categories. They cluster around relation-heavy reasoning, OCR-adjacent understanding, and structured image-text interpretation.

## Regressions and flat categories

Most categories improved, but a few remained flat or moved slightly downward:

- `image_emotion`: `-4.000`
- `physical_relation`: `-4.167`
- `image_scene`: `-0.961`
- `action_recognition`: `+0.000`
- `identity_reasoning`: `+0.000`
- `social_relation`: `+0.000`

These small regressions do not change the overall picture, but they are worth keeping in mind if a downstream workload is concentrated in those subareas.

## Interpretation

The `MMBench` profile is not flat for either model. Instead, both runs show a recognizable capability shape.

For the 2B model:

- very strong scene and identity-focused recognition
- solid social and OCR-related perception
- clear weakness on spatial, predictive, and certain relation-heavy categories

For the 8B model:

- the strongest recognition categories remain strong
- OCR, structured image-text understanding, and relation-heavy reasoning improve substantially
- spatial reasoning is still not the strongest part of the model, but it is no longer a severe outlier in the same way as the 2B run

This makes the `83.4` 8B score easier to interpret. The gain is not just general scaling noise; it reflects a real broadening of the model's multimodal reasoning profile.
