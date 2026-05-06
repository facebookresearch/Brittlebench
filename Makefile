## paths
.ONESHELL:
.PHONY: help
.DEFAULT_GOAL := help

## print a help msg to display the comments
help:
	@grep -hE '^[A-Za-z0-9_ \-]*?:.*##.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

USER := $(shell whoami)
PWD := $(shell pwd)
ROOT := $(shell cd ..;  pwd)
HF_HOME:=/home/$(USER)/.cache/huggingface/
HF_DATASETS_CACHE=/home/$(USER)/.cache/huggingface/

# Set default parameters for backwards-compatibility 
SAVE_LOC?=results/

setup:
	uv sync
	cd lm-evaluation-harness/
	uv pip install -e .

test:
	uv run -m pytest tests/ 

test_eval:
	uv run lm_eval --model vllm \
    --model_args pretrained=meta-llama/Llama-3.2-1B-Instruct,dtype=auto \
    --tasks mmlu \
    --batch_size auto

run_brittlebench_local:
	WANDB_MODE=offline uv run python submit_job.py \
		--config configs/qwen3_4B.yaml \
		--tasks mmlu \
		--stacks baseline \
		--save_loc $(SAVE_LOC) \
		--slurm_account $(SLURM_ACCOUNT) \
		--qos $(SLURM_QOS) \
		--num_fewshot 0 \
		--num_gpus 1 \
		--limit 5 \
		--log_samples \
		--local

run_brittlebench_slurm:
	WANDB_MODE=offline uv run python submit_job.py \
		--config configs/qwen3_4B.yaml \
		--tasks mmlu \
		--stacks baseline \
		--save_loc $(SAVE_LOC) \
		--slurm_account $(SLURM_ACCOUNT) \
		--qos $(SLURM_QOS) \
		--num_fewshot 0 \
		--num_gpus 1 \
		--log_samples 
