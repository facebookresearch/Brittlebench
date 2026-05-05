"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from abc import ABC
from typing import Dict, List, Optional, Union

from brittlebench.perturbations.perturbation import (
    ListPerturbation,
    TextPerturbation,
)

class Rewrite(ABC):
    def __init__(
        self,
        name: str,
        exclusive_tasks: Optional[List[str]] = None,
        banned_tasks: Optional[List[str]] = None,
        apply_to: str = "process_docs",
        perturbation: Optional[
            Union[TextPerturbation, ListPerturbation]
        ] = None,
    ) -> None:
        super().__init__()

        self.name = name
        self.perturbation = perturbation
        self.exclusive_tasks = exclusive_tasks  # Only apply the rewrite to these tasks
        self.banned_tasks = banned_tasks  # Apply the rewrite to all tasks except these
        self.apply_to = apply_to

        if self.exclusive_tasks is not None and self.banned_tasks is not None:
            raise ValueError("Cannot specify both exclusive_tasks and banned_tasks")

        if self.apply_to not in ["process_docs", "build_all_requests"]:
            raise ValueError(f"Expected `apply_to` to be either `process_docs` or `build_all_requests`; instead got {self.apply_to}")


    def is_task_compatible(self, task_name) -> bool:
        if self.exclusive_tasks is not None and len(self.exclusive_tasks) > 0:
            return task_name in self.exclusive_tasks
        elif self.banned_tasks is not None and len(self.banned_tasks) > 0:
            return task_name not in self.banned_tasks
        else:
            return True

    def apply(self, sample: Dict) -> Dict:
        pass


class CompositeRewrite(ABC):
    def __init__(self,
                 name,
                 rewrites: List[Rewrite]) -> None:
        """A composite rewrite that applies multiple rewrites components in sequence."""
        self.name = name
        self.rewrites = rewrites

    def is_task_compatible(self, task_name) -> bool:
        return all(rewrite.is_task_compatible(task_name) for rewrite in self.rewrites)
