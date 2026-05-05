"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
# Use submitit to run eval using slurm
from pathlib import Path

import fire
import submitit
import yaml
from accelerate import notebook_launcher

from eval_scaffold import run_eval


def run(num_gpus=1, 
        tasks="", 
        stacks="all", 
        num_fewshot=0, 
        log_samples=False, 
        limit: None | float | int = None, 
        config="",  
        save_loc="", 
        trust_remote_code=False, 
        confirm_run_unsafe_code=False):

    with open(config, "r") as file:
        config_args = yaml.safe_load(file)

    if config_args["model"] == "vllm":
        # do not use notebook launcher with vllm
        run_eval(tasks, 
                 stacks, 
                 config, 
                 save_loc, 
                 num_fewshot=num_fewshot, 
                 log_samples=log_samples, 
                 limit=limit,
                 trust_remote_code=trust_remote_code, 
                 confirm_run_unsafe_code=confirm_run_unsafe_code)
    else:
        args = (tasks, stacks, config, save_loc, num_fewshot, log_samples, trust_remote_code, confirm_run_unsafe_code)
        notebook_launcher(run_eval, 
                          args, 
                          num_processes=num_gpus)


def main(
    tasks="",
    stacks="all",
    limit: None | float | int =None,
    config="",
    num_fewshot=0,
    save_loc="",
    num_gpus=1,
    qos="",
    slurm_account="",
    local=False,
    log_samples=False,
    trust_remote_code=False,
    confirm_run_unsafe_code=False,
):
    """
    Args:
        limit: if provided limits the number or percent of samples used for evaluation
            (useful for testing)
    """

    save_loc = Path(save_loc) / config.split("/")[-1].split(".yaml")[0]
    if not save_loc.exists():
        save_loc.mkdir(parents=True, exist_ok=True)

    if not local:
        if type(tasks) == str:
            tasks = tasks.split(",")
        executor = submitit.AutoExecutor(
            folder=str(save_loc / "job_%j"), slurm_max_num_timeout=20
        )
        executor.update_parameters(
            name="mllm_eval",
            slurm_partition="learn",
            slurm_account=slurm_account,
            slurm_qos=qos,
            slurm_mem_per_gpu="210G",
            timeout_min=100,
            nodes=1,
            tasks_per_node=1,
            cpus_per_task=16,
            gpus_per_node=num_gpus,
        )

        jobs = []
        with executor.batch():
            for task in tasks:
                job = executor.submit(
                    run,
                    num_gpus,
                    task,
                    stacks,
                    num_fewshot,
                    log_samples,
                    limit,
                    config,
                    str(save_loc),
                    trust_remote_code,
                    confirm_run_unsafe_code,
                )
                jobs.append(job)

        print("Submitted jobs: ", ",".join([job.job_id for job in jobs]))
    else:
        run(num_gpus, 
            tasks, 
            stacks,
            num_fewshot=num_fewshot,
            log_samples=log_samples,
            limit=limit, 
            config=config,
            save_loc=str(save_loc),
            trust_remote_code=trust_remote_code,
            confirm_run_unsafe_code=confirm_run_unsafe_code)


if __name__ == "__main__":
    fire.Fire(main)
