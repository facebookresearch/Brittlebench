"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import pytest
from typing import Union

from brittlebench.rewrites.registry import RewriteRegistry
from brittlebench.rewrites.rewrite import Rewrite, CompositeRewrite

POSITIVE_STIMULI_CODES = [f"EP0{i}" if i < 10 else f"EP{i}" for i in range(1, 21)]
ATTACKS_STIMULI_CODES = [f"EA0{i}" if i < 10 else f"EA{i}" for i in range(1, 23)]
EMOTION_REWRITE_NAMES = [f"rewrite_emotion_prompt_{code}".lower() for code in POSITIVE_STIMULI_CODES + ATTACKS_STIMULI_CODES]
QUOTES_REWRITE_NAMES = [f"rewrite_quotes_{quotes_count}" for quotes_count in [1, 3, 5, 10, 15, 20]]
SPACES_REWRITE_NAMES = [f"rewrite_spaces_{spaces_count}" for spaces_count in [1, 3, 5, 10, 15, 20]]
NEW_LINES_REWRITE_NAMES = [f"rewrite_new_lines_{new_lines_count}" for new_lines_count in [1, 3, 5, 10, 15, 20]]
TYPO_REWRITE_NAMES = [f"rewrite_text_prompt_with_typos_{count}" for count in [1, 3, 5, 10, 15, 20]]

BASE_PERTS_FOR_TEXT_BENCHS = [
                    'rewrite_persona_instruction',
                    'rewrite_persona_knowledge',
                    'rewrite_persona_math',
                    'rewrite_punct_spaces',
                    'rewrite_word_merge',
                    'rewrite_word_split',
                    'rewrite_drop_stop_words',
                    'rewrite_add_space_seq',
                    *QUOTES_REWRITE_NAMES,
                    *SPACES_REWRITE_NAMES,
                    *NEW_LINES_REWRITE_NAMES,
                    *EMOTION_REWRITE_NAMES
                ]

PERTS_FOR_TEXT_BENCHS = BASE_PERTS_FOR_TEXT_BENCHS + ['rewrite_text_prompt_with_typos', *TYPO_REWRITE_NAMES]

MCQ_BERTS = [
    'rewrite_shuffled_choices',
    'rewrite_shuffled_order_options',
    'rewrite_ignore_above_correct',
    'rewrite_ignore_above_incorrect',
    'rewrite_poe',
    'rewrite_no_poe',
]

MATH_PERTS = [
    'rewrite_symmetrical_addition',
    'rewrite_symmetrical_multiplication',
    'rewrite_latexify',
]

CODE_PERTS = ['rewrite_to_class', 'rewrite_in_camel_case']


class _DummyRewrite(Rewrite):
    def __init__(self, **kwargs):
        super().__init__(name="dummy_rewrite")
        self.kwargs = kwargs

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.kwargs == other.kwargs


class TestRewriteRegistry:
    @pytest.mark.parametrize(
        "task_name",
        [
            "mbpp",
            "humaneval",
        ],
    )
    def test_rewrites_for_task_instantiates_rewrites(self, task_name):
        registry = RewriteRegistry()

        # Implicitly checks that each rewrite can be instantiated
        rewrites = registry.rewrites_for_task(task_name)

        assert isinstance(rewrites, list)
        for rewrite in rewrites:
            assert isinstance(rewrite, Union[Rewrite, CompositeRewrite])

    def test_rewrites_for_task_with_default_constructor_args(self):
        task_to_rewrites = {"some-task": [_DummyRewrite]}

        registry = RewriteRegistry(task_to_rewrites=task_to_rewrites)

        rewrites = registry.rewrites_for_task("some-task")

        assert len(rewrites) == 1
        assert rewrites[0] == _DummyRewrite()

    @pytest.mark.parametrize(
        "task_name,expected_rewrites",
        [
            pytest.param(
                "mmlu",
                PERTS_FOR_TEXT_BENCHS + MCQ_BERTS
            ),
            pytest.param(
                "truthfulqa_mc1",
                PERTS_FOR_TEXT_BENCHS + MCQ_BERTS
            ),
            pytest.param(
                "ai2_arc",
                PERTS_FOR_TEXT_BENCHS
            ),
            pytest.param(
                "acp_mcq_cot_2shot",
                PERTS_FOR_TEXT_BENCHS
            ),
            pytest.param(
                "logiqa",
                PERTS_FOR_TEXT_BENCHS + MCQ_BERTS
            ),
            pytest.param(
                "mathqa", 
                PERTS_FOR_TEXT_BENCHS + MATH_PERTS
            ),
            pytest.param(
                "gpqa", 
                PERTS_FOR_TEXT_BENCHS + MCQ_BERTS + MATH_PERTS
            ),
            pytest.param(
                "gsm8k", 
                PERTS_FOR_TEXT_BENCHS + MATH_PERTS
            ),
            pytest.param(
                "mbpp", 
                BASE_PERTS_FOR_TEXT_BENCHS + ['rewrite_text_prompt_with_misspellings']
            ),
            pytest.param(
                "humaneval", 
                BASE_PERTS_FOR_TEXT_BENCHS + CODE_PERTS + ['rewrite_text_prompt_with_misspellings', 'rewrite_remove_types']
            ),
            pytest.param(
                "aime25",
                PERTS_FOR_TEXT_BENCHS + MATH_PERTS
            ),
        ],
    )
    def test_rewrites_for_tasks_with_limited_applicability(self, task_name, expected_rewrites):
        registry = RewriteRegistry()

        # Implicitly checks that each rewrite can be instantiated
        rewrites = registry.rewrites_for_task(task_name)

        rewrite_names = [rewrite.name for rewrite in rewrites]
        assert set(rewrite_names) == set(expected_rewrites)
