"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import re

from brittlebench.perturbations.perturbation import TextPerturbation


class PoEInstructionsPerturbation(TextPerturbation):

    # Regex matches: optional newline, optional whitespace, ("Answer:" or "The answer is:"), optional whitespace, at end of string
    _ANSWER_PROMPT_PATTERN = re.compile(
        r"(?:\r?\n)?\s*(Answer:|The answer is:)\s*$",
        re.IGNORECASE
    )

    def __init__(self, is_poe: bool = True):
        super().__init__()
        self.is_poe = is_poe

    def _strip_answer_suffix(self, text: str) -> str:
        # Remove only a trailing answer prompt, not those inside the text
        return self._ANSWER_PROMPT_PATTERN.sub("", text).rstrip()

    def apply(self, text: str) -> str:
        """
        Args:
            text: test str
            is_poe: if True, return the text with two choices asking the model to find the incorrect answer, 
                    else return the text with two choices asking the model to find the correct answer.
        Returns:
            prompt: The constructed prompt string.
        """
        text = self._strip_answer_suffix(text)

        if self.is_poe:
            prefix = "Your goal is to identify the incorrect answer to the multiple choice question.\n"
            prompt = f"{prefix}{text}\nIncorrect Answer:"

        else:
            prefix = "Your goal is to identify the correct answer to the multiple choice question.\n"
            prompt = f"{prefix}{text}\nCorrect Answer:"
        return prompt
