"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import argparse
import copy
import getpass
import json
import logging
import os
import sys
import traceback
from logging import getLogger
from pathlib import Path
from typing import List, Union
from tabulate import tabulate
import wandb
import yaml
from accelerate import Accelerator

from lm_eval import evaluator, utils
from lm_eval.__main__ import setup_parser
from lm_eval.api.task import Task
from lm_eval.evaluator import request_caching_arg_to_dict
from lm_eval.loggers import EvaluationTracker, WandbLogger
from lm_eval.tasks import TaskManager, get_task_dict
from lm_eval.utils import handle_non_serializable, make_table, simple_parse_args_string

from brittlebench.rewrites.registry import RewriteRegistry
from brittlebench.rewrites.rewrite_stack import RewriteStack, parse_stacks_arg
from rewritable_task import RewritableTask
from brittlebench.rewrites.rewrite import CompositeRewrite


logger = getLogger()


def flatten_all_tasks(obj: Union[dict, Task]) -> List[Task]:
    if isinstance(obj, Task):
        return [obj]
    elif isinstance(obj, dict):
        tasks = []
        for k, v in obj.items():
            tasks.extend(flatten_all_tasks(v))
        return tasks


def rewritable_cli_evaluate(args: argparse.Namespace):
    """
    Copy of the cli_evaluate function with batteries included for rewrites
    """
    if args.wandb_args:
        wandb_args_dict = simple_parse_args_string(args.wandb_args)
        wandb_config_args_dict = simple_parse_args_string(args.wandb_config_args)
        wandb_logger = WandbLogger(wandb_args_dict, wandb_config_args_dict)

    utils.setup_logging(args.verbosity)
    eval_logger = logging.getLogger(__name__)
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    # update the evaluation tracker args with the output path and the HF token
    if args.output_path:
        args.hf_hub_log_args += f",output_path={args.output_path}"
    if os.environ.get("HF_TOKEN", None):
        args.hf_hub_log_args += f",token={os.environ.get('HF_TOKEN')}"
    evaluation_tracker_args = simple_parse_args_string(args.hf_hub_log_args)
    evaluation_tracker = EvaluationTracker(**evaluation_tracker_args)

    if args.predict_only:
        args.log_samples = True
    if (args.log_samples or args.predict_only) and not args.output_path:
        raise ValueError(
            "Specify --output_path if providing --log_samples or --predict_only"
        )

    if args.fewshot_as_multiturn and args.apply_chat_template is False:
        raise ValueError(
            "When `fewshot_as_multiturn` is selected, `apply_chat_template` must be set (either to `True` or to the chosen template name)."
        )

    if args.include_path is not None:
        eval_logger.info(f"Including path: {args.include_path}")
    metadata = (
        simple_parse_args_string(args.model_args)
        if isinstance(args.model_args, str)
        else args.model_args
        if isinstance(args.model_args, dict)
        else {}
    ) | (
        args.metadata
        if isinstance(args.metadata, dict)
        else simple_parse_args_string(args.metadata)
    )

    task_manager = TaskManager(include_path=args.include_path, metadata=metadata)

    if "push_samples_to_hub" in evaluation_tracker_args and not args.log_samples:
        eval_logger.warning(
            "Pushing samples to the Hub requires --log_samples to be set. Samples will not be pushed to the Hub."
        )

    if args.limit:
        eval_logger.warning(
            " --limit SHOULD ONLY BE USED FOR TESTING."
            "REAL METRICS SHOULD NOT BE COMPUTED USING LIMIT."
        )
    if args.samples:
        assert args.limit is None, (
            "If --samples is not None, then --limit must be None."
        )
        if (samples := Path(args.samples)).is_file():
            args.samples = json.loads(samples.read_text())
        else:
            args.samples = json.loads(args.samples)

    if args.tasks is None:
        eval_logger.error("Need to specify task to evaluate.")
        sys.exit()
    elif args.tasks == "list":
        print(task_manager.list_all_tasks())
        sys.exit()
    elif args.tasks == "list_groups":
        print(task_manager.list_all_tasks(list_subtasks=False, list_tags=False))
        sys.exit()
    elif args.tasks == "list_tags":
        print(task_manager.list_all_tasks(list_groups=False, list_subtasks=False))
        sys.exit()
    elif args.tasks == "list_subtasks":
        print(task_manager.list_all_tasks(list_groups=False, list_tags=False))
        sys.exit()
    else:
        if isinstance(args.tasks, str) and os.path.isdir(args.tasks):
            import glob

            task_names = []
            yaml_path = os.path.join(args.tasks, "*.yaml")
            for yaml_file in glob.glob(yaml_path):
                config = utils.load_yaml_config(yaml_file)
                task_names.append(config)
        else:
            task_list = args.tasks
            task_names = task_manager.match_tasks(task_list)
            for task in [task for task in task_list if task not in task_names]:
                if os.path.isfile(task):
                    config = utils.load_yaml_config(task)
                    task_names.append(config)
            task_missing = [
                task for task in task_list if task not in task_names and "*" not in task
            ]  # we don't want errors if a wildcard ("*") task name was used

            if task_missing:
                missing = ", ".join(task_missing)
                eval_logger.error(
                    f"Tasks were not found: {missing}\n"
                    f"{utils.SPACING}Try `lm-eval --tasks list` for list of available tasks",
                )
                raise ValueError(
                    f"Tasks not found: {missing}. Try `lm-eval --tasks {{list_groups,list_subtasks,list_tags,list}}` to list out all available names for task groupings; only (sub)tasks; tags; or all of the above, or pass '--verbosity DEBUG' to troubleshoot task registration issues."
                )

    # Respect user's value passed in via CLI, otherwise default to True and add to comma-separated model args
    if args.trust_remote_code:
        eval_logger.info(
            "Passed `--trust_remote_code`, setting environment variable `HF_DATASETS_TRUST_REMOTE_CODE=true`"
        )
        # HACK: import datasets and override its HF_DATASETS_TRUST_REMOTE_CODE value internally,
        # because it's already been determined based on the prior env var before launching our
        # script--`datasets` gets imported by lm_eval internally before these lines can update the env.
        import datasets

        datasets.config.HF_DATASETS_TRUST_REMOTE_CODE = True

        args.model_args = args.model_args + ",trust_remote_code=True"
    (
        eval_logger.info(f"Selected Tasks: {task_names}")
        if eval_logger.getEffectiveLevel() >= logging.INFO
        else print(f"Selected Tasks: {task_names}")
    )

    request_caching_args = request_caching_arg_to_dict(
        cache_requests=args.cache_requests
    )

    #####  Rewrite logic #######

    # Get a dictionary of task objects from the lm-harness task names and task manager
    # The output is a dict of ConfigurableGroup and ConfigurableTask objects that are nested 
    # according to the group/subgroup structure of the tasks
    # E.g. > task_name=mmlu_anatomy,output_type=multiple_choice,num_fewshot=None,num_samples=135
    task_dict = get_task_dict(task_names, task_manager)

    # Note: since get_task_dict only works with a list of Task objects, we first flatten all tasks from a group here
    # The caveat to this is that we need to pass the group name to rewrites_for_task, which is now just taking the string
    # before the first occurence of _ in task name
    # In lm-harness terms, the task object refers to the _template file.
    all_tasks = flatten_all_tasks(task_dict)

    # Initialize the registry that holds all available rewrites.
    # registry.rewrites is either a list of all rewrites, or a dict mapping task names to lists of rewrites
    registry = RewriteRegistry()

    # Prepare a list to hold the processed (rewritten) tasks
    processed_tasks = []

    # Iterate over each task to apply rewrites
    for task in all_tasks:
        tname = task.task_name
        global_task_name = tname.split("_")[0]

        # Get the list of rewrites objs applicable to this task
        eligible_rewrites_for_task = registry.rewrites_for_task(global_task_name)
        name_to_rewrite = {rewrite.name: rewrite for rewrite in eligible_rewrites_for_task}

        # Iterate over each stack of rewrites
        for _, stack_rewrites in enumerate(args.stacks):

            # Create the list of rewrite objects to be applied for this task based on stack_rewrites
            if "baseline" in stack_rewrites and len(set(stack_rewrites)) == 1:
                eval_logger.info("Running baseline mode, not running rewrites..")
                rewrites_for_task = []
            elif stack_rewrites == "all":
                eval_logger.info("Running all available rewrites for this task..")
                rewrites_for_task = eligible_rewrites_for_task
            else:
                # ensure order is preserved as per user input; remove baseline if present
                rewrites_for_task = [name_to_rewrite[name] for name in stack_rewrites if name in name_to_rewrite and name !='baseline']

            # Flatten rewrites in the stack (handle CompositeRewrites)
            rewrites_for_task = [
                sub_rw if isinstance(rw, CompositeRewrite) else rw
                for rw in rewrites_for_task
                for sub_rw in (rw.rewrites if isinstance(rw, CompositeRewrite) else [rw])
            ]

            # Creates a stack of rewrites to be applied in sequence
            stack = RewriteStack(*rewrites_for_task)
            
            # Applies the RewriteStack to the task
            new_task = RewritableTask(task_obj=copy.deepcopy(task), stack=stack)
        
            processed_tasks.append(new_task)

    eval_logger.info(f"Processing {len(processed_tasks)} tasks with rewriting logic ..")

    # Add task-related info to args for logging purposes
    args.processed_tasks_count = len(processed_tasks)
    args.processed_tasks_names = [t._config.task for t in processed_tasks]

    # Logging config
    eval_logger.info("Configuration from user input:")
    args_dict = vars(args)
    non_empty_args = {k: v for k, v in args_dict.items() if v not in (None, "", [], {}, ())}
    empty_keys = [k for k, v in args_dict.items() if v in (None, "", [], {}, ())]
    table = tabulate(non_empty_args.items(), headers=["ARGUMENT", "VALUE"], tablefmt="rounded_grid")
    eval_logger.info("\n" + table)
    eval_logger.info(f"Empty arguments: {empty_keys}\n")

    results = evaluator.simple_evaluate(
        model=args.model,
        model_args=args.model_args,
        tasks=processed_tasks,
        num_fewshot=args.num_fewshot,
        batch_size=args.batch_size,
        max_batch_size=args.max_batch_size,
        device=args.device,
        use_cache=args.use_cache,
        limit=args.limit,
        samples=args.samples,
        check_integrity=args.check_integrity,
        write_out=args.write_out,
        log_samples=args.log_samples,
        evaluation_tracker=evaluation_tracker,
        system_instruction=args.system_instruction,
        apply_chat_template=args.apply_chat_template,
        fewshot_as_multiturn=args.fewshot_as_multiturn,
        gen_kwargs=args.gen_kwargs,
        task_manager=task_manager,
        predict_only=args.predict_only,
        random_seed=args.seed[0],
        numpy_random_seed=args.seed[1],
        torch_random_seed=args.seed[2],
        fewshot_random_seed=args.seed[3],
        confirm_run_unsafe_code=args.confirm_run_unsafe_code,
        metadata=metadata,
        **request_caching_args,
    )

    if results is not None:
        if args.log_samples:
            samples = results.pop("samples")
        dumped = json.dumps(
            results, indent=2, default=handle_non_serializable, ensure_ascii=False
        )
        if args.show_config:
            print(dumped)

        batch_sizes = ",".join(map(str, results["config"]["batch_sizes"]))

        # Add W&B logging
        if args.wandb_args:
            try:
                wandb_logger.post_init(results)
                wandb_logger.log_eval_result()
                if args.log_samples:
                    wandb_logger.log_eval_samples(samples)
            except Exception as e:
                eval_logger.info(f"Logging to Weights and Biases failed due to {e}")

        evaluation_tracker.save_results_aggregated(
            results=results, samples=samples if args.log_samples else None
        )

        if args.log_samples:
            for task_name, config in results["configs"].items():
                evaluation_tracker.save_results_samples(
                    task_name=task_name, samples=samples[task_name]
                )

        if (
            evaluation_tracker.push_results_to_hub
            or evaluation_tracker.push_samples_to_hub
        ):
            evaluation_tracker.recreate_metadata_card()

        print(
            f"{args.model} ({args.model_args}), gen_kwargs: ({args.gen_kwargs}), limit: {args.limit}, num_fewshot: {args.num_fewshot}, "
            f"batch_size: {args.batch_size}{f' ({batch_sizes})' if batch_sizes else ''}"
        )
        print(make_table(results))
        if "groups" in results:
            print(make_table(results, "groups"))

        if args.wandb_args:
            # Tear down wandb run once all the logging is done.
            wandb_logger.run.finish()

    return results


def run_eval(tasks="", 
             stacks="all", 
             config="", 
             save_loc="", 
             num_fewshot=0,
             log_samples=False, 
             limit=None,
             trust_remote_code=False, 
             confirm_run_unsafe_code=False):
    import os

    parse = setup_parser()
    args = parse.parse_args("")
    args.stacks = parse_stacks_arg(stacks)
    args.num_fewshot = num_fewshot
    args.log_samples = log_samples
    args.trust_remote_code = trust_remote_code
    args.confirm_run_unsafe_code = confirm_run_unsafe_code
    args.limit = limit
    if isinstance(tasks, str):
        tasks = tasks.split(",")
    args.tasks = tasks

    if len(os.environ.get("SLURM_ARRAY_JOB_ID", "")) > 0:
        job_id = f"{os.environ.get('SLURM_ARRAY_JOB_ID')}_{os.environ.get('SLURM_ARRAY_TASK_ID')}"
    else:
        job_id = os.environ.get("SLURM_JOB_ID", "na")

    user = getpass.getuser()
    os.environ["HF_HOME"] = f"/home/{user}/.cache/huggingface/"

    args_list = []
    results_list = []
    if not os.path.exists(config):
        raise ValueError(f"Config file does not exist: {args.config}")

    with open(config, "r") as file:
        config_args = yaml.safe_load(file)
    config_args = [config_args] if type(config_args) != list else config_args
    # multiple configs, create args list first
    for cfg in config_args:
        args_copy = argparse.Namespace(**vars(args))
        for key, value in cfg.items():
            setattr(args_copy, key, value)
        setattr(
            args_copy, "output_path", str(Path(save_loc) / f"job_{job_id}" / "logs")
        )
        args_list.append(args_copy)

    if args.verbosity:
        os.environ["VERBOSITY"] = args.verbosity
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    # initialize Accelerator
    accelerator = Accelerator()
    if accelerator.is_main_process:
        is_main_process = True
    else:
        is_main_process = False

    if is_main_process:
        model_name = args_list[0].model_args.split(",")[0].split("=")[-1]
        if model_name.startswith("/checkpoint"):
            model_name = model_name.rstrip("/").split("/")[-1]
        wandb_logger = wandb.init(
            dir=save_loc,
            entity="brittlebench",
            project=f"eval_{tasks}",
            config={
                "eval": vars(args_list[0]),
                "env": dict(os.environ),
            },
            name=model_name,
        )
    else:
        wandb_logger = None

    for args in args_list:
        try:
            results = rewritable_cli_evaluate(args)
            results_list.append(results)

            accelerator.wait_for_everyone()

        except Exception as e:
            if args.verbosity == "DEBUG":
                raise e
            else:
                traceback.print_exc()
                results_list.append(None)

    for ri, (args, results) in enumerate(zip(args_list, results_list)):
        # cli_evaluate will return none if the process is not the main process (rank 0)
        if results is not None:
            # log to wandb
            if wandb_logger:
                metrics = {
                    f"result/{task}/{k}": v
                    for task, m in results["results"].items()
                    for k, v in m.items()
                }
                wandb_logger.log(metrics)
                if "groups" in results:
                    group_metrics = {
                        f"group/{task}/{k}": v
                        for task, m in results["groups"].items()
                        for k, v in m.items()
                    }
                    wandb_logger.log(group_metrics)

    if wandb_logger and is_main_process:
        wandb_logger.finish()
