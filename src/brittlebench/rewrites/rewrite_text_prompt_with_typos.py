"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import Dict, Optional

from brittlebench.perturbations.typo_perturbation import TypoPerturbation, TypoCountPerturbation
from brittlebench.rewrites.rewrite import Rewrite


class RewriteTextPromptWithTypos(Rewrite):
    """Apply common typos to a given sample key.

    By default, will apply a mix of character-level typos, keyboard typos, and misspellings.

    typo_type='charmix' applies character-level insertions/deletions/modifications.
    typo_type='keyboard' applies typos based on keyboard layout.
    typo_type='misspelling' applies common misspellings based on a dictionary.

    Examples:
    "What is the capital of France?" -> "Whot is the capitol of France?"
    "Write a function to calculate the factorial of a number." -> "Writ a function to calclate the factrial of a number."
    """

    def __init__(self, name: str = "rewrite_text_prompt_with_typos", 
                 key: str = "text", 
                 typo_type: str = "all", 
                 typos_count: Optional[int] = None):
        super().__init__(name=name)
        self.key = key
        self.typo_type = typo_type
        self.banned_tasks = ['mbpp', 'humaneval']
        self.apply_to = "process_docs"

        if typo_type not in ["charmix", "keyboard", "misspelling", "all"]:
            raise ValueError(
                f"Invalid typo_type: {typo_type}. Must be one of 'charmix', 'keyboard', 'misspelling', or 'all'."
            )

        if typos_count:
            if typos_count < 1:
                raise ValueError("typos_count must be at least 1.")
            self.perturbation = TypoCountPerturbation(typo_type=typo_type, typos_count=typos_count)
        else:
            self.perturbation = TypoPerturbation(typo_type=typo_type)

    def apply(self, sample: Dict) -> Dict:
        sample[self.key] = self.perturbation.apply(sample[self.key])
        return sample


class RewriteTextPromptWithMisspellings(RewriteTextPromptWithTypos):
    """Apply misspelling typos to a given sample key.

    This rewrite is only applied to the MBPP and Humaneval tasks, where other forms of typo are inappropriate.
    Examples:
    "What is the capital of France?" -> "What is the capitol of France?"
    """

    def __init__(self, key: str = "text"):
        super().__init__(name="rewrite_text_prompt_with_misspellings", key=key, typo_type='misspelling')
        self.exclusive_tasks = ["mbpp", 'humaneval']


def create_typos_count_class(typos_count):
    # A factory function to create classes for specific typos_count values
    # The orchestration script calls the factory function instead of directly instantiating the class.
    # This is to avoid code duplication for different number of typos experiments.
    return type(
        f"RewriteTextPromptWithTypos{typos_count}",
        (RewriteTextPromptWithTypos,),
        {
            "__init__": lambda self, key="text": RewriteTextPromptWithTypos.__init__(
                self,
                name=f"rewrite_text_prompt_with_typos_{typos_count}".lower(),
                key=key,
                typos_count=typos_count
            )
        }
    )