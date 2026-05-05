"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from collections.abc import Mapping
from enum import Enum
from functools import partial
from typing import Tuple, Union, List

import datasets

from brittlebench.rewrites.rewrite import Rewrite


def parse_stacks_arg(rewrite_arg: Union[Tuple[str], str]) -> List[List[str]]:
    """
    Parse user input for rewrites into a structured list of lists.
    """
    if not rewrite_arg:
        return [["all"]]

    if isinstance(rewrite_arg, tuple):
        return [list(rewrite_arg)]
    elif isinstance(rewrite_arg, str):
        # Split by semicolon to get outer list elements
        outer_parts = rewrite_arg.split(';')

        # For each part, split by comma to get inner list elements
        result = []
        for part in outer_parts:
            if part.strip():  # Skip empty parts
                inner_list = [item.strip() for item in part.split(',') if item.strip()]
                if inner_list:  # Only add non-empty inner lists
                    result.append(inner_list)
        return result
    else:
        raise ValueError("Input must be a string or a tuple of strings.")


class Stage(Enum):
    PROCESS_DOCS = "process_docs"
    BUILD_ALL_REQUESTS = "build_all_requests"


class RewriteStack:
    def __init__(self, *rewrites: Rewrite):
        # Ordered stack: left to right is the execution order.
        self.rewrites = list(rewrites)

    def add(self, rewrite: Rewrite) -> "RewriteStack":
        """Create and return a new RewriteStack with the added rewrite."""
        new_rewrites = self.rewrites + [rewrite]
        return RewriteStack(*new_rewrites)

    def apply(self, sample: Union[Mapping, str], stage: Stage) -> Union[dict, str]:
        """Apply all rewrites in the stack to the sample at the given stage."""
        for rw in self.rewrites:
            if rw.apply_to == stage.value:
                if isinstance(sample, str):
                    sample = rw.perturbation.apply(sample)  # call from build_all_requests
                elif isinstance(sample, Mapping):
                    sample = rw.apply(sample)  # call from process_docs
                else:
                    raise ValueError("Sample must be either a Mapping or a string.")
        return sample

    @property
    def names(self) -> str:
        return "+".join(rw.name for rw in self.rewrites) if self.rewrites else "baseline"

    def to_process_docs(self, orig_process_docs=None, stage=Stage.PROCESS_DOCS):
        """Generate a process_docs function to be used with lm-eval-harness."""

        def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
            """Applies all rewrites in the stack to the dataset at the given stage."""
            if orig_process_docs is not None:
                dataset = orig_process_docs(dataset)
            return dataset.map(lambda sample: self.apply(sample, stage=stage))

        return process_docs
