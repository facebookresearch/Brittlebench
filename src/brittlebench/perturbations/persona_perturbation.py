"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import random

from datasets import load_dataset

from brittlebench.perturbations.perturbation import TextPerturbation


class PersonaPerturbation(TextPerturbation):
    """
    Add a random persona from Tencent PersonaHub as an instruction to the input
    """

    def __init__(self, subset="instruction"):
        super().__init__()
        self.persona_subset = subset
        self.persona_data = load_dataset("proj-persona/PersonaHub", subset)["train"]

    def apply(self, text: str) -> str:
        # randomly choose a persona
        key = (
            "persona"
            if self.persona_subset in ["elite_persona", "persona"]
            else "input persona"
        )
        total_personas = len(self.persona_data)
        while True:
            row_id = random.choice(range(total_personas))
            row = self.persona_data[row_id]
            persona = row[key]
            if persona.startswith("A "):
                break
        perturbed_text = "You are a " + persona.lstrip("A ") + "\n\n" + text
        return perturbed_text


if __name__ == "__main__":
    pp = PersonaPerturbation()
    print(pp.apply("This is a question."))
