"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import List, Union
import random

from brittlebench.perturbations.ignore_above_perturbation import IgnoreAbovePerturbation
from brittlebench.rewrites.rewrite import Rewrite


class RewriteIgnoreAboveBase(Rewrite):
    def __init__(self, 
                 key: str = "text",
                 choices="choices",
                 answer="answer", 
                 is_correct: bool = True, 
):
        super().__init__(name="rewrite_ignore_above", apply_to="process_docs")
        self.key = key
        self.is_correct = is_correct
        self.choices = choices
        self.answer = answer
        self.exclusive_tasks = ["mmlu", "truthfulqa_mc1", "logiqa", "gpqa"]
        self.perturbation = IgnoreAbovePerturbation()

    def _resolve_answer(self, choices: List[str], answer: Union[int, str]) -> str:
        """
        Finds the correct or an incorrect answer from a list of choices and prepends it to a prompt.

        Args:
            choices (list): A list of possible answer choices.
            answer: The correct answer, which can be in letter, numerical, or string format.
            is_correct (bool): If True, the correct answer is selected. 
                                If False, a random incorrect answer is selected.
            prompt (str): The base prompt to which the selected choice will be prepended.

        Returns:
            str: The prompt with the selected choice prepended.
        """

        correct_choice = None
        
        # Determine the correct choice based on various answer key formats
        for i, choice in enumerate(choices):
            if isinstance(answer, str) and answer.upper() in ["A", "B", "C", "D"]:
                if chr(65 + i) == answer.upper():  # Convert index to letter (A, B, C, D)
                    correct_choice = choice
                    break
            elif isinstance(answer, int):
                if i == answer:
                    correct_choice = choice
                    break
            elif isinstance(answer, str) and choice == answer:
                correct_choice = choice
                break

        if correct_choice is None:
            raise ValueError("The provided answer does not match any choice in the list.")

        if self.is_correct:
            selected_choice = correct_choice
        else:
            incorrect_choices = [c for c in choices if c != correct_choice]
            if not incorrect_choices:
                raise ValueError("No incorrect choices available to select from.")
            selected_choice = random.choice(incorrect_choices)

        return selected_choice


    def apply(self, sample: dict) -> dict:
        """
        Finds the correct answer from the choices. 
            If self.is_correct=True then prepends the correct answer in the prompt. 
            Else it randomly selects an incorrect choice and then prepends it to the prompt.
        """

        # find the correct answer choice based on the answer key for various answer key formats
        answer = self._resolve_answer(sample[self.choices], sample[self.answer])

        sample[self.key] = self.perturbation.apply(sample[self.key], answer)
        return sample


class RewriteIgnoreAboveCorrect(RewriteIgnoreAboveBase):
    def __init__(self, key: str = "text", choices="choices", answer="answer"):
        super().__init__(key=key, choices=choices, answer=answer, is_correct=True)
        self.name = "rewrite_ignore_above_correct"


class RewriteIgnoreAboveIncorrect(RewriteIgnoreAboveBase):
    def __init__(self, key: str = "text", choices="choices", answer="answer"):
        super().__init__(key=key, choices=choices, answer=answer, is_correct=False)
        self.name = "rewrite_ignore_above_incorrect"
