"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import pandas as pd
import wandb
import os
import datetime
from pathlib import Path


class Runs:
    """
    Pulls the latest run data from wandb and creates a summary dataframe of the results.

    Args:
        tag: filter only for runs with specified tag. No filtering is applied if None.
        skip_hidden: skips runs with the hidden tag from wandb, if True
    """

    def __init__(
        self,
        project: str,
        entity: str = "brittlebench",
        tag: str | None = None,
        skip_hidden: bool = True,
        filters: dict = {"state": "finished", "created_at": {"$gt": "2025-06-24T##"}},
    ):
        self.entity = entity
        self.project = project
        self.tag = None
        self.skip_hidden = skip_hidden

        if tag is not None:
            filters["tags"] = tag

        self.config_keys = [
            "name",
            "logs_dir",
            "git_hash",
        ]

        api = wandb.Api()
        self.runs = api.runs(
            entity + "/" + project,
            filters=filters,
            # sort by most recent runs
            order="created_at",
        )
        self.df = self.create_df()

    def create_df(self):
        """Creates a dataframe of all runs"""
        data = []
        for run in self.runs:
            run_data = dict()
            run_data.update(self.extract_summary(run.summary._json_dict))
            run_data.update(self.extract_config(run.config))
            run_data.update({"tags": run.tags})
            run_data.update({"name": run.name})
            run_data.update({"created_at": run.created_at})
            run_data.update({"id": run.id})
            # skip runs with hidden tag
            if self.skip_hidden and ("hidden" in run.tags):
                continue
            data.append(run_data)

        runs_df = pd.DataFrame.from_records(data)
        # sort columns
        runs_df = runs_df.sort_index(axis=1)
        return runs_df

    def extract_config(self, config: dict) -> dict:
        data = dict()
        for config_key in self.config_keys:
            if config_key in config:
                data[config_key] = config[config_key]
            elif "." in config_key:
                # handles nested keys
                keys = config_key.split(".")
                data[config_key] = config[keys[0]][keys[1]]
        return data

    def extract_summary(self, summary: dict) -> dict:
        """Summary containing accuracy and other metrics"""
        data = dict()
        for (
            k,
            v,
        ) in summary.items():
            if k.startswith("_"):
                continue
            k = self.clean_summary_statistic_name(k)
            data[k] = v
        return data

    def clean_summary_statistic_name(self, name: str) -> str:
        name = name.replace("custom-extract", "")
        name = name.replace("result/", "")
        return name

    def save(self, save_dir: str = "results"):
        output_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        save_path = os.path.join(save_dir, f"{output_date}.csv")
        self.df.to_csv(save_path)


if __name__ == "__main__":
    runs = Runs(project="eval_mmlu_pro")
    print(runs.df)
