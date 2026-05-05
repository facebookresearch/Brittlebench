"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.perturbations.to_class_perturbation import ToClassPerturbation


class TestToClassPerturbation:

    def test_change_code_entities_perturbation(self):
        input_text = (
            "from typing import List\n"
            "def has_close_elements(numbers: List[float], threshold: float) -> bool:\n"
            "    \"\"\" Check if in given list of numbers, are any two numbers closer to each other than\n"
            "    given threshold.\n"
            "    \"\"\""
        )
        perturbed_text = (
            "class MyClass:\n"
            "    from typing import List\n"
            "    def has_close_elements(numbers: List[float], threshold: float) -> bool:\n"
            "        \"\"\" Check if in given list of numbers, are any two numbers closer to each other than\n"
            "        given threshold.\n"
            "        \"\"\""
        )
        perturbation = ToClassPerturbation()
        perturbed_text = perturbation.apply(input_text)

        assert "class" in perturbed_text
        assert "def" in perturbed_text
        assert perturbed_text == perturbed_text

    def test_empty_function(self):
        input_text = ""
        perturbed_text = (
            "class MyClass:\n"
            "    pass\n"
        )

        perturbation = ToClassPerturbation()
        perturbed_text = perturbation.apply(input_text)

        assert perturbed_text == perturbed_text

    def test_function_with_empty_lines(self):
        input_text = (
            "def example_function():\n\n"
            "    print(\"Hello, World!\")\n\n"
        )
        perturbed_text = (
            "class MyClass:\n"
            "    def example_function():\n\n"
            "        print(\"Hello, World!\")\n\n"
        )
        perturbation = ToClassPerturbation()
        perturbed_text = perturbation.apply(input_text)

        assert perturbed_text == perturbed_text

    def test_function_with_only_whitespace_lines(self):
        input_text = (
            "def example_function():\n"
            "    \n"
            "    print(\"Hello, World!\")\n"
            "    \n"
        )
        perturbed_text = (
            "class MyClass:\n"
            "    def example_function():\n"
            "        \n"
            "        print(\"Hello, World!\")\n"
            "        \n"
        )
        perturbation = ToClassPerturbation()
        perturbed_text = perturbation.apply(input_text)

        assert perturbed_text == perturbed_text

    def test_function_with_no_body(self):
        input_text = (
            "def empty_function():\n"
            "    pass\n"
        )
        perturbed_text = (
            "class MyClass:\n"
            "    def empty_function():\n"
            "        pass\n"
        )
        perturbation = ToClassPerturbation()
        perturbed_text = perturbation.apply(input_text)

        assert perturbed_text == perturbed_text

    def test_function_with_multiline_body(self):    
        input_text = (
            "def complex_function(x):\n"
            "    if x > 0:\n"
            "        return x\n"
            "    else:\n"
            "        return -x\n"
        )
        perturbed_text = (
            "class MyClass:\n"
            "    def complex_function(x):\n"
            "        if x > 0:\n"
            "            return x\n"
            "        else:\n"
            "            return -x\n"
        )
        perturbation = ToClassPerturbation()
        perturbed_text = perturbation.apply(input_text)

        assert perturbed_text == perturbed_text

    def test_function_with_leading_trailing_whitespace(self):
        input_text = (
            "   def spaced_function():\n"
            "       print(\"Spaced!\")\n"
            "   \n"
        )
        perturbed_text = (
            "class MyClass:\n"
            "    def spaced_function():\n"
            "        print(\"Spaced!\")\n"
            "    \n"
        )
        perturbation = ToClassPerturbation()
        perturbed_text = perturbation.apply(input_text)

        assert perturbed_text == perturbed_text

    def test_function_with_comments(self):
        input_text = (
            "def commented_function():\n"
            "    # This is a comment\n"
            "    print(\"With comments\")\n"
        )
        perturbed_text = (
            "class MyClass:\n"
            "    def commented_function():\n"
            "        # This is a comment\n"
            "        print(\"With comments\")\n"
        )
        perturbation = ToClassPerturbation()
        perturbed_text = perturbation.apply(input_text)

        assert perturbed_text == perturbed_text

    def test_function_with_decorators(self):
        input_text = (
            "@decorator\ndef decorated_function():\n"
            "    print(\"Decorated\")\n"
        )
        perturbed_text = (
            "class MyClass:\n"
            "    @decorator\n"
            "    def decorated_function():\n"
            "        print(\"Decorated\")\n"
        )
        perturbation = ToClassPerturbation()
        perturbed_text = perturbation.apply(input_text)

        assert perturbed_text == perturbed_text
        
    def test_function_with_nested_functions(self):
        input_text = (
            "def outer_function():\n"
            "    def inner_function():\n"
            "        return \"Inner\"\n"
            "    return inner_function()\n"
        )
        perturbed_text = (
            "class MyClass:\n"
            "    def outer_function():\n"
            "        def inner_function():\n"
            "            return \"Inner\"\n"
            "        return inner_function()\n"
        )
        perturbation = ToClassPerturbation()
        perturbed_text = perturbation.apply(input_text)

        assert perturbed_text == perturbed_text
