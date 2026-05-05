"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import Union, Sequence
import copy

from lm_eval.api.task import ConfigurableTask
from brittlebench.rewrites.rewrite import Rewrite, CompositeRewrite
from brittlebench.rewrites.rewrite_stack import RewriteStack, Stage


class RewritableTask(ConfigurableTask):
    def __init__(
        self,
        task_obj: ConfigurableTask = None,
        stack: Union[RewriteStack, Sequence[Rewrite],
                     CompositeRewrite, Sequence[CompositeRewrite]] = None,
    ) -> None:
        """
        RewritableTask extends ConfigurableTask to allow for our perturbations to be applied.
        We have two places of applying perturbations: either on the docs (using Rewrite.apply_to=process_docs),
        or on the instance post few-shot modifications (using Rewrite.apply_to=build_all_requests).
        If rewrite is a string, it is assumed to be "baseline" and no perturbation is applied.

        - If apply_to is process_doc, it alters the config process_docs function.
        - If apply_to is build_all_requests, it alters the instances after they are built.
        """
        for key in task_obj.__dict__.keys():
            setattr(self, key, getattr(task_obj, key))

        self.stack = stack

        rname = f"{self.task_name}_{stack.names}"
        self._config.task = rname

        self._config.process_docs = stack.to_process_docs(
            self._config.process_docs, stage=Stage.PROCESS_DOCS
        )

    def build_all_requests(self, **kwargs):
        """
        This method first calls the superclass implementation to build the initial set of instances.
        It applies the specified perturbation to the context (first argument) of each instance.
        The modified instances are deep-copied to avoid mutating the originals, and the updated
        list replaces the current instances.
        """
        super().build_all_requests(**kwargs)

        processed_instances = []
        for inst in self._instances:
            arguments = list(inst.arguments)
            ctx = arguments[0]

            ctx = self.stack.apply(ctx, stage=Stage.BUILD_ALL_REQUESTS)
            new_inst = copy.deepcopy(inst)
            arguments[0] = ctx

            new_inst.arguments = tuple(arguments)
            processed_instances.append(new_inst)

        self._instances = processed_instances
