import argparse
import json
import os
import platform
import sys

import torch
import transformers
from transformers import AutoProcessor, Qwen3VLForConditionalGeneration


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe loading a Qwen3-VL-compatible model.")
    parser.add_argument("--model", required=True, help="Model ID or local path")
    parser.add_argument("--dtype", default="float16", choices=["float16", "bfloat16"], help="Torch dtype to use")
    parser.add_argument("--device-map", default="auto", help="Transformers device_map")
    parser.add_argument("--attn-implementation", default="sdpa", help="Attention implementation")
    args = parser.parse_args()

    dtype = {"float16": torch.float16, "bfloat16": torch.bfloat16}[args.dtype]

    env_info = {
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "torch": torch.__version__,
        "torch_cuda": torch.version.cuda,
        "transformers": transformers.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device_count": torch.cuda.device_count(),
        "cuda_device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "cuda_bf16_supported": torch.cuda.is_bf16_supported() if torch.cuda.is_available() else None,
        "hf_home": os.environ.get("HF_HOME"),
        "hf_token_present": bool(os.environ.get("HF_TOKEN")),
    }
    print("[probe] environment")
    print(json.dumps(env_info, indent=2, ensure_ascii=False))

    print(f"[probe] loading processor for {args.model}")
    processor = AutoProcessor.from_pretrained(args.model)
    print(f"[probe] processor class: {processor.__class__.__name__}")

    print(f"[probe] loading model for {args.model}")
    model = Qwen3VLForConditionalGeneration.from_pretrained(
        args.model,
        dtype=dtype,
        device_map=args.device_map,
        attn_implementation=args.attn_implementation,
    ).eval()
    print(f"[probe] model class: {model.__class__.__name__}")
    print(f"[probe] model device: {getattr(model, 'device', 'unknown')}")
    if torch.cuda.is_available():
        print(f"[probe] gpu_allocated_bytes: {torch.cuda.memory_allocated(0)}")
        print(f"[probe] gpu_reserved_bytes: {torch.cuda.memory_reserved(0)}")
    print("[probe] load successful")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
