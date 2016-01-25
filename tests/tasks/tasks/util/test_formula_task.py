# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright 2015 by Ecpy Authors, see AUTHORS for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# -----------------------------------------------------------------------------
"""Test of the Formula task.

"""
from __future__ import (division, unicode_literals, print_function,
                        absolute_import)

import pytest
import enaml
from multiprocessing import Event
from collections import OrderedDict

from ecpy.tasks.base_tasks import RootTask
from ecpy.tasks.tasks.util.formula_task import FormulaTask
with enaml.imports():
    from ecpy.tasks.tasks.util.views.formula_view import FormulaView

from ecpy.testing.util import show_and_close_widget


class TestFormulaTask(object):
    """Test LogTask.

    """

    def setup(self):
        self.root = RootTask(should_stop=Event(), should_pause=Event())
        self.task = FormulaTask(name='Test')
        self.root.add_child_task(0, self.task)

    def test_perform1(self):
        """Test checking that the message value gets written to the database

        """
        self.task.formulas = OrderedDict([('key1', "1.0+3.0"),
                                          ('key2', '3.0+4.0')])
        self.root.prepare()

        self.task.perform()
        assert self.task.get_from_database('Test_key1') == 4.0


@pytest.mark.ui
def test_view(windows):
    """Test the LogTask view.

    """
    show_and_close_widget(FormulaView(task=FormulaTask(name='Test')))
