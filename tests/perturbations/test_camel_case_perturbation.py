"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.perturbations.camel_case_perturbation import CamelCasePerturbation


class TestCamelCasePerturbation:

    def test_with_snake_case_input(self):
        text = "This is a function convert_to_camel_case that we want to convert."

        perturbation = CamelCasePerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "This is a function convertToCamelCase that we want to convert."

    def test_with_camel_case_input(self):
        text = "This is a function convertToCamelCase that we want to convert."

        perturbation = CamelCasePerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "This is a function convertToCamelCase that we want to convert."

    def test_with_mixed_input(self):
        text = "Use the apply_edit function to apply edits and convert_to_camel_case."

        perturbation = CamelCasePerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "Use the applyEdit function to apply edits and convertToCamelCase."

    def test_with_no_variable_names(self):
        text = "This text has no variable names."

        perturbation = CamelCasePerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "This text has no variable names."

    def test_with_leading_trailing_underscores(self):
        text = "Is this a _private_variable and this a public_variable_?"

        perturbation = CamelCasePerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "Is this a privateVariable and this a publicVariable?"

    def test_with_parentheses(self):
        text = "Call the function compute_value(param1, param2) to get the result."

        perturbation = CamelCasePerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == "Call the function computeValue(param1, param2) to get the result."

    def test_with_multiple_lines(self):
        text = (
            """def my_function(param_one, param_two): \n"""
            """    return param_one + param_two"""
        )

        perturbation = CamelCasePerturbation()
        perturbed_text = perturbation.apply(text)

        assert perturbed_text == (
            """def myFunction(paramOne, paramTwo): \n"""
            """    return paramOne + paramTwo"""
        )