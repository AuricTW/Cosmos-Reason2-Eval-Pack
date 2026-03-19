# Reproduction Notes

## Environment

- OS: Linux
- GPU: NVIDIA GeForce RTX 4090 24 GB
- Driver: `565.77`
- CUDA reported by `nvidia-smi`: `12.7`
- Python: `3.10.18`
- Python executable: `/root/miniconda3/envs/workenv/bin/python3`

## Key packages

- `torch==2.8.0`
- `torchvision==0.23.0`
- `torchaudio==2.8.0`
- `transformers==5.3.0`
- `accelerate==1.13.0`
- `datasets==4.8.2`
- `qwen-vl-utils==0.0.14`
- `decord==0.6.0`
- `lmms_eval==0.7.1`

## Setup

```bash
git clone --depth 1 https://github.com/EvolvingLMMs-Lab/lmms-eval.git artifacts/tmp/lmms-eval
python3 -m pip install --upgrade torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0
python3 -m pip install -e "artifacts/tmp/lmms-eval[video-legacy]"
```

## Load probe

```bash
HF_HOME=/root/.cache/huggingface \
HF_HUB_ENABLE_HF_TRANSFER=1 \
python3 scripts/load_vlm_probe.py \
  --model nvidia/Cosmos-Reason2-2B \
  --dtype float16 \
  --device-map auto \
  --attn-implementation sdpa
```

## Local task patch

Apply:

- `patches/lmms_eval_public_dataset_token_fix.patch`

This patch changes several `dataset_kwargs.token` fields from `True` to `False` for public MMBench and DocVQA paths, avoiding unnecessary Hugging Face token failures on public data.

## Evaluation commands

### MMBench full

```bash
HF_HOME=/root/.cache/huggingface HF_HUB_ENABLE_HF_TRANSFER=1 WANDB_MODE=disabled \
python3 -m lmms_eval eval \
  --model qwen3_vl \
  --model_args pretrained=nvidia/Cosmos-Reason2-2B,device_map=auto,attn_implementation=sdpa \
  --tasks mmbench_en_dev \
  --batch_size 1 \
  --output_path ./results/cosmos_reason2_mmbench_full \
  --log_samples \
  --verbosity INFO
```

### TextVQA full

```bash
HF_HOME=/root/.cache/huggingface HF_HUB_ENABLE_HF_TRANSFER=1 WANDB_MODE=disabled \
python3 -m lmms_eval eval \
  --model qwen3_vl \
  --model_args pretrained=nvidia/Cosmos-Reason2-2B,device_map=auto,attn_implementation=sdpa \
  --tasks textvqa_val \
  --batch_size 1 \
  --output_path ./results/cosmos_reason2_textvqa_full \
  --log_samples \
  --verbosity INFO
```

### DocVQA full

```bash
HF_HOME=/root/.cache/huggingface \
HF_HUB_ENABLE_HF_TRANSFER=1 \
WANDB_MODE=disabled \
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
python3 -m lmms_eval eval \
  --model qwen3_vl \
  --model_args pretrained=nvidia/Cosmos-Reason2-2B,device_map=auto,attn_implementation=sdpa \
  --tasks docvqa_val \
  --batch_size 1 \
  --output_path ./results/cosmos_reason2_docvqa_full_bs1 \
  --log_samples \
  --verbosity INFO
```

## Notes

- `Cosmos-Reason2-2B` loaded successfully through the `Qwen3-VL` model interface.
- For `DocVQA`, larger batch sizes were not stable on this single 24 GB GPU; `batch_size=1` was the reliable setting.
- The file `patches/lmms_eval_qwen3_vl_oom_retry_experiment.patch` is included only as an experiment log of attempted stabilization work.
