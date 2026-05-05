"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.perturbations.perturbation import TextPerturbation


class ToClassPerturbation(TextPerturbation):
    """ Wraps a given function string inside a Python class with proper indentation. """

    def apply(self, text: str) -> str:
        # Split the function string into lines
        func_lines = text.splitlines()

        # Indent each line by 4 spaces (Python standard for class members)
        indented_func_lines = []
        for line in func_lines:
            # Avoid adding indentation to empty lines to keep code clean
            if line.strip():
                indented_func_lines.append("    " + line)
            else:
                indented_func_lines.append("")

        # Compose the class code
        class_code = f"class MyClass:\n"
        if not any(line.strip() for line in indented_func_lines):
            # If function string is empty or only whitespace, add pass
            class_code += "    pass\n"
        else:
            class_code += "\n".join(indented_func_lines) + "\n"

        return class_code
