"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import random

from brittlebench.perturbations.typo_perturbation import TypoPerturbation, TypoCountPerturbation


class TestTypoPerturbation:

    def setup_method(self, _):
        # Reset the random seed before each test method
        random.seed(a=0)

    def test_typo_perturbation(self):
        text = "This is some sample text."

        perturbation = TypoPerturbation()

        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "This is some sampre texm."

    def test_typo_perturbation_with_misspellings(self):
        text = "Hello again."

        perturbation = TypoPerturbation(typo_type="misspelling")

        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "Hello agian."

    def test_typo_perturbation_with_charmix(self):
        text = "This is some sample text."

        perturbation = TypoPerturbation(typo_type="charmix")

        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "This is some sampre texm."

    def test_typo_perturbation_with_keyboard(self):
        text = "This is some sample text."

        perturbation = TypoPerturbation(typo_type="keyboard")

        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "This is some samp;e texy."

    def test_typo_perturbation_with_multiline_string(self):
        text = "This is some sample text\nover two lines."

        perturbation = TypoPerturbation()

        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "Htis is some sampgle text\nover twpo liner."

    def test_typo_perturbation_with_different_count_typos(self):
        counts = [1, 3, 5, 8, 10]
        text = "This is some random sentence the we want to test the typo perturbation on."

        for count in counts:
            perturbation = TypoCountPerturbation(typos_count=count)

            perturbed_text = perturbation.apply(text)

            # Count the number of typos by comparing the original and perturbed tokens
            typos = 0
            for token_og, token_pert in zip(text.split(), perturbed_text.split()):
                if token_og != token_pert:
                    typos += 1

            assert typos == count

    def test_count_typo_perturbation_with_larger_count_than_words(self):
        text = "This is some sample text."

        perturbation = TypoCountPerturbation(typos_count=10)

        perturbed_text = perturbation.apply(text)

        # Count the number of typos by comparing the original and perturbed tokens
        typos = 0
        for token_og, token_pert in zip(text.split(), perturbed_text.split()):
            if token_og != token_pert:
                typos += 1

        assert typos == len(text.split())

    def test_typo_perturbation_with_different_count_typos_with_multiline_str(self):
        text = "This is some random sentence\nover two lines."
        typos_count = 3

        perturbation = TypoCountPerturbation(typos_count=typos_count)
        perturbed_text = perturbation.apply(text)

        # Count the number of typos by comparing the original and perturbed tokens
        typos = 0
        for token_og, token_pert in zip(text.split(), perturbed_text.split()):
            if token_og != token_pert:
                typos += 1

        assert typos == typos_count

    def test_typo_perturbation_with_empty_string(self):
        text = ""

        perturbation = TypoPerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == ""

    def test_count_typo_perturbation_with_empty_string(self):
        text = ""

        perturbation = TypoCountPerturbation(typos_count=5)
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == ""

    def test_typo_perturbation_with_only_spaces(self):
        text = "     "

        perturbation = TypoPerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "     "

    def test_typo_count_perturbation_with_only_spaces(self):
        text = "     "

        perturbation = TypoCountPerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "     "

    def test_count_typo_perturbation_with_negative_count(self):
        text = "This is some sample text."

        perturbation = TypoCountPerturbation(typos_count=-3)
        perturbed_text = perturbation.apply(text)

        # No typos should be applied
        assert perturbed_text == text

    def test_typo_perturbation_with_an_equation(self):
        text = "This is a very important equation that we want to solve E = mc^2."

        perturbation = TypoPerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "Htis is a vrey importamt equation thast qe want to solve E = mc^2."  # No typos should be applied to equation part

    def test_typo_perturbation_with_a_number(self):
        text = "We have 12343546435214 apples and 2345621 cherries and 2345765432 bags to put them in."

        perturbation = TypoPerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "Wb have 12343546435214 apples adn 2345621 chrries and 2345765432 bas ti put them ih."  # No typos should be applied to equation part

    def test_typo_with_gpqa(self):
        text = "Two quantum states with energies E1 and E2 have a lifetime of 10^-9 sec and 10^-8 sec, respectively. We want to clearly distinguish these two energy levels. Which one of the following options could be their energy difference so that they be clearly resolved?"

        perturbation = TypoPerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "Two quantum stat4s with energes E1 and E2 hvea a lifetime oa 10^-9 sec and 10^-8 sec, repsectively. We want to claerly distingish these teo energy levels. Whic one of teh follwoing option*s coudl be theri energy differene o thta htey be claerly resolved?"

    def test_typo_with_abbreviations(self):
        text = "These are some abbreviations: INCLUDE, ABC, TEST"

        perturbation = TypoPerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "These ame some abbreviarions: INCLUDE, ABC, TEST"

    def test_typo_with_unit_of_measurement(self):
        text = "eV meters cm 1234 L"

        perturbation = TypoPerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == text

    def test_typo_with_case_sensitive(self):
        text = "meters Meters PM SECONDS Degree MINS KG MILES ATM Liters"

        perturbation = TypoPerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == text
