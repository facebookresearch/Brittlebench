"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from brittlebench.rewrites.rewrite_padding_prompt import (
    create_padding_prompt_class,
    RewritePaddingPromptBase,
)


class TestRewritePaddingPrompt:

    def test_rewrite_padding_prompt_base(self):
        rewrite = RewritePaddingPromptBase()
        sample = {"text": "This is a test."}
        perturbed_sample = rewrite.apply(sample)
        assert perturbed_sample["text"] == ' This is a test. '

    def test_create_padding_prompt_class_quotes(self):
        RewritePaddingPromptQuotes5 = create_padding_prompt_class(char='quotes', char_count=5)
        rewrite = RewritePaddingPromptQuotes5()
        sample = {"text": "This is a test."}
        perturbed_sample = rewrite.apply(sample)
        assert perturbed_sample["text"] == '""""" This is a test. """""'

    def test_create_padding_prompt_class_spaces(self):
        RewritePaddingPromptSpaces5 = create_padding_prompt_class(char='spaces', char_count=5)
        rewrite = RewritePaddingPromptSpaces5()
        sample = {"text": "This is a test."}
        perturbed_sample = rewrite.apply(sample)
        assert perturbed_sample["text"] == '      This is a test.      '

    def test_create_padding_prompt_class_new_lines(self):
        RewritePaddingPromptNewLines5 = create_padding_prompt_class(char='new_lines', char_count=5)
        rewrite = RewritePaddingPromptNewLines5()
        sample = {"text": "This is a test."}
        perturbed_sample = rewrite.apply(sample)
        assert perturbed_sample["text"] == '\n\n\n\n\n This is a test. \n\n\n\n\n'

    def test_create_padding_prompt_class_invalid_char(self):
        try:
            create_padding_prompt_class(char='invalid_char', char_count=5)
        except ValueError as e:
            assert str(e) == "Character 'invalid_char' is not supported. Choose from ['spaces', 'quotes', 'new_lines']."
        else:
            assert False, "Expected ValueError for unsupported character."
