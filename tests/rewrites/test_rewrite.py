"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import pytest

from brittlebench.rewrites.rewrite import Rewrite

class DummyRewrite(Rewrite):
    pass


class TestRewrite:

    def test_is_task_compatible_with_exclusive_tasks(self):
        rewrite = DummyRewrite(name='rewrite', exclusive_tasks=['task1', 'task2'])

        assert rewrite.is_task_compatible('task1')
        assert rewrite.is_task_compatible('task1')
        assert not rewrite.is_task_compatible('task3')

    def test_is_task_compatible_with_banned_tasks(self):
        rewrite = DummyRewrite(name='rewrite', banned_tasks=['task1', 'task2'])

        assert not rewrite.is_task_compatible('task1')
        assert not rewrite.is_task_compatible('task1')
        assert rewrite.is_task_compatible('task3')

    def test_is_task_compatible_with_both_banned_and_exclusive_tasks(self):
        with pytest.raises(ValueError):
            DummyRewrite(name='rewrite', exclusive_tasks=['task1'], banned_tasks=['task2'])

    def test_is_task_compatible_with_no_tasks(self):
        rewrite = DummyRewrite(name='rewrite')

        assert rewrite.is_task_compatible('task1')
        assert rewrite.is_task_compatible('task2')

    def test_with_invalid_apply_to(self):
        with pytest.raises(ValueError):
            DummyRewrite(name='rewrite', apply_to='invalid')
