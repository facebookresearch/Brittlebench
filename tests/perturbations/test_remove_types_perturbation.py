"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.perturbations.remove_types_perturbation import RemoveTypesPerturbation


class TestRemoveTypesPerturbation:

    def test_with_function_definition(self):
        perturbation = RemoveTypesPerturbation()
        code = "def example_func(a: int, b: str = 'default', *args: float, **kwargs: bool) -> None:"
        expected_code = "def example_func(a, b ='default', *args, **kwargs):"
        perturbed_code = perturbation.apply(code)
        assert perturbed_code == expected_code

    def test_with_type_annotations(self):
        perturbation = RemoveTypesPerturbation()
        code = (
            "from typing import List\n"
            "def has_close_elements(numbers: List[float], threshold: float) -> bool:\n"
            "    \"\"\" Check if in given list of numbers, are any two numbers closer to each other than\n"
            "    given threshold.\n"
            "    \"\"\""
        )
        expected_code = (
            "from typing import List\n\n"
            "def has_close_elements(numbers, threshold):\n"
            "    \"\"\" Check if in given list of numbers, are any two numbers closer to each other than\n"
            "    given threshold.\n"
            "    \"\"\""
        )
        perturbed_code = perturbation.apply(code)
        assert perturbed_code == expected_code

    def test_with_no_type_annotations(self):
        perturbation = RemoveTypesPerturbation()
        code = (
            "def multiply(a, b):\n"
            "    return a * b\n"
            "z = 42"
        )
        perturbed_code = perturbation.apply(code)
        assert perturbed_code == code

    def test_with_mixed_code(self):    
        perturbation = RemoveTypesPerturbation()
        code = (
            "def greet(name: str) -> str:\n"
            "    return 'Hello, ' + name\n"
            "count = 10\n"
            "is_active: bool = True"
        )
        expected_code = (
            "def greet(name):\n"
            "    return 'Hello, ' + name\n"
            "count = 10\n"
            "is_active = True"
        )
        perturbed_code = perturbation.apply(code)
        assert perturbed_code == expected_code

    def test_with_multiple_types(self):
        perturbation = RemoveTypesPerturbation()
        code = (
            "def complex_func(a: List[int], b: Dict[str, float]) -> Optional[float]:\n"
            "    pass\n"
            "data: Tuple[int, str] = (1, 'one')"
        )
        expected_code = (
            "def complex_func(a, b):\n"
            "    pass\n"
            "data = (1, 'one')"
        )
        perturbed_code = perturbation.apply(code)
        assert perturbed_code == expected_code

    def test_with_empty_string(self):
        perturbation = RemoveTypesPerturbation()
        empty_code = ""
        perturbed_code = perturbation.apply(empty_code)
        assert perturbed_code == "" 

    def test_with_no_code(self):
        perturbation = RemoveTypesPerturbation()
        no_code = "Just some random text without code."
        perturbed_code = perturbation.apply(no_code)
        assert perturbed_code == no_code

    def test_with_multiline_function_definition(self):
        perturbation = RemoveTypesPerturbation()
        multiline_code = (
            "def long_function_name(\n"
            "    param1: int,\n"
            "    param2: str,\n"
            ") -> None:\n"
            "    pass"
        )
        expected_multiline_code = (
            "def long_function_name(param1, param2):\n"
            "    pass"
        )
        perturbed_code = perturbation.apply(multiline_code)
        assert perturbed_code == expected_multiline_code

    def test_with_prefix_suffix_text(self):
        perturbation = RemoveTypesPerturbation()
        text = "Complete the following function based on its definition:\n\ndef example_func(a: int, b: str = 'default', *args: float, **kwargs: bool) -> None:\n\nMake sure you get it right!"
        expected_text = "Complete the following function based on its definition:\n\ndef example_func(a, b ='default', *args, **kwargs):\n\nMake sure you get it right!"
        perturbed_text = perturbation.apply(text)
        assert perturbed_text == expected_text
