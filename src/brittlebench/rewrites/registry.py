"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import Dict, List, Optional, Type, Union
import inspect

from brittlebench.rewrites.rewrite import Rewrite
from brittlebench.rewrites.rewrite_in_camel_case import (
    RewriteInCamelCase,
)
from brittlebench.rewrites.rewrite_latexify_word_problems import (
    RewriteLatexifyWordProblems,
)
from brittlebench.rewrites.rewrite_list_with_shuffled_order import (
    RewriteListWithShuffledOrder,
)
from brittlebench.rewrites.rewrite_personas import (
    RewritePersonaInstruction,
    RewritePersonaKnowledge,
    RewritePersonaMath,
)
from brittlebench.rewrites.rewrite_text_prompt_with_typos import (
    RewriteTextPromptWithTypos,
    RewriteTextPromptWithMisspellings,
    create_typos_count_class
)

from brittlebench.rewrites.rewrite_emotion_prompts import create_stimuli_class

from brittlebench.rewrites.rewrite_padding_prompt import create_padding_prompt_class

from brittlebench.rewrites.rewrite_punct_spaces import RewritePunctSpaces

from brittlebench.rewrites.rewrite_ignore_above import (
    RewriteIgnoreAboveCorrect,
    RewriteIgnoreAboveIncorrect,
)

from brittlebench.rewrites.rewrite_poe import (
    CompositeRewritePoE,
    CompositeRewriteNoPoE
)

from brittlebench.rewrites.rewrite_shuffle_choices import (
    RewriteListWithShuffledChoices,
)

from brittlebench.rewrites.rewrite_word_manipulation import (
    RewriteWordMerge,
    RewriteWordSplit,
)

from brittlebench.rewrites.rewrite_drop_stop_words import RewriteDropStopWords

from brittlebench.rewrites.rewrite_add_space_seq import RewriteAddSpaceSeq

from brittlebench.rewrites.rewrite_symmetrical_operation import (
    RewriteSymmetricalAddition,
    RewriteSymmetricalMultiplication,
)

from brittlebench.rewrites.rewrite_to_class import RewriteToClass

from brittlebench.rewrites.rewrite_remove_types import RewriteRemoveTypes

# Define stimuli codes for which child classes will be created and dynamically generate child classes
POSITIVE_STIMULI_CODES = [f"EP0{i}" if i < 10 else f"EP{i}" for i in range(1, 21)]
ATTACKS_STIMULI_CODES = [f"EA0{i}" if i < 10 else f"EA{i}" for i in range(1, 23)]
dynamic_emotion_rewrites = [create_stimuli_class(code) for code in POSITIVE_STIMULI_CODES + ATTACKS_STIMULI_CODES]

# Define quotes counts for which child classes will be created and dynamically generate child classes
dynamic_quotes_rewrites = [create_padding_prompt_class(char='quotes', char_count=quotes_count) for quotes_count in [1, 3, 5, 10, 15, 20]]
dynamic_spaces_rewrites = [create_padding_prompt_class(char='spaces', char_count=spaces_count) for spaces_count in [1, 3, 5, 10, 15, 20]]
dynamic_new_lines_rewrites = [create_padding_prompt_class(char='new_lines', char_count=new_lines_count) for new_lines_count in [1, 3, 5, 10, 15, 20]]

# Define typo counts for which child classes will be created and dynamically generate child classes
TYPO_COUNT = [1, 3, 5, 10, 15, 20]
dynamic_typos_count_rewrites = [create_typos_count_class(count) for count in TYPO_COUNT]

_ALL_REWRITES = [
    RewriteTextPromptWithTypos,
    RewriteTextPromptWithMisspellings,
    RewritePersonaInstruction,
    RewritePersonaKnowledge,
    RewritePersonaMath,
    RewriteLatexifyWordProblems,
    RewriteInCamelCase,
    RewritePunctSpaces,
    RewriteIgnoreAboveCorrect,
    RewriteIgnoreAboveIncorrect,
    CompositeRewritePoE,
    CompositeRewriteNoPoE,
    RewriteListWithShuffledOrder,
    RewriteListWithShuffledChoices,
    RewriteWordMerge,
    RewriteWordSplit,
    RewriteDropStopWords,
    RewriteAddSpaceSeq,
    RewriteSymmetricalAddition,
    RewriteSymmetricalMultiplication,
    RewriteToClass,
    RewriteRemoveTypes,
    *dynamic_emotion_rewrites,
    *dynamic_typos_count_rewrites,
    *dynamic_quotes_rewrites,
    *dynamic_spaces_rewrites,
    *dynamic_new_lines_rewrites,
]

# define kwargs for the tasks where perturbation should be applied.
_TASK_KWARGS = {
    "mmlu": {"key": "question", 
             "choices": "choices",
             "answer": "answer"},
    "anli": {"key": "premise"},
    "humaneval": {"key": "prompt"},
    "arc": {"key": "question",
            "choices": "choices",
            "answer": "answerKey"},
    "acp": {"key": "question"},
    "ai2": {"key": "question",
            "choices": "choices",
            "answer": "answerKey"},
    "truthfulqa": {"key": "question"},
    "logiqa": {"key": "question",
               "choices": "choices",
              "answer": "label"},
    "mathqa": {"key": "Problem",
               "choices": "options",
               "answer": "correct"},
    "mbpp": {"key": "text"},
    "gpqa": {"key": "Question", 
             "choices": ["choice1", "choice2", "choice3", "choice4"],
             "answer": "answer"},
    "gsm8k": {"key": "question", 
              "answer": "answer"},
    "aime25": {"key": "problem",
               "answer": "answer"},
}

class RewriteRegistry:
    """A registry of tasks and applicable rewrites.

    Usage:
    ```
    registry = RewriteRegistry()
    rewrites_for_mmlu = registry.rewrites_for_task('mmlu')
    process_docs = rewrites_for_mmlu[0].to_process_docs()
    ```
    """
    def __init__(self, task_to_rewrites: Optional[Dict[str, List[Rewrite]]] = None):
        """
        Initializes the registry with a mapping of task names to rewrite classes.
        If task_to_rewrites is provided, it will override the default mappings.
        """
        self.rewrites: Union[List[Rewrite], Dict[str, List[Rewrite]]] = (
            task_to_rewrites or _ALL_REWRITES
        )

    def rewrites_for_task(self, task_name):
        """
        Returns a list of rewrite classes for the given task name.
        """
        rewrites = []
        if isinstance(self.rewrites, dict):
            assert task_name in self.rewrites, (
                f"No rewrites found for task {task_name}, RewriteRegistry initialized with mapping containing {self.rewrites.keys()} tasks"
            )
            rewrites = self.rewrites[task_name]
        else:
            rewrites = self.rewrites

        filtered_rewrites = []
        # Iterate through each rewrite class and instantiate it with task-specific kwargs if available
        for rewrite_cls in rewrites:
            benchmark_cols = _TASK_KWARGS.get(task_name, {})

            # Get the required arguments for the rewrite class dynamically
            required_args = self._get_required_args(rewrite_cls)

            # Map task-specific columns to the required arguments
            mapped_args = {arg: benchmark_cols[arg] for arg in required_args if arg in benchmark_cols}
            rewrite = rewrite_cls(**mapped_args)
            if rewrite.is_task_compatible(task_name):
                filtered_rewrites.append(rewrite)

        return filtered_rewrites

    def _get_required_args(self, rewrite_cls: Type[Rewrite]) -> List[str]:
        """
        Extracts the required arguments for a rewrite class from its constructor.
        """
        # Use inspect to get the signature of the __init__ method
        signature = inspect.signature(rewrite_cls.__init__)

        # Exclude 'self' and optional arguments (those with default values)
        return [
            param_name
            for param_name in signature.parameters.keys()
            if param_name != "self"
        ]
