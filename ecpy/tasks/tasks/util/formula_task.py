# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright 2015 by Ecpy Authors, see AUTHORS for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# -----------------------------------------------------------------------------
"""Task for defining a mathematical formula
"""

from atom.api import (Dict, Unicode, set_default)

from ...base_tasks import SimpleTask


class FormulaTask(SimpleTask):
    """Compute values according to formulas. Any valid python expression can be
    evaluated and replacement to access to the database data can be used.
    """
    #: List of formulas.
    # If you want to modify it (Add/remove entry) you must copy, modify and then REASSIGN it
    formulas = Dict(Unicode()).tag(pref=True)

    wait = set_default({'activated': True})  # Wait on all pools by default.

    def perform(self):
        """
        """
    #    for i, formula in enumerate(self.formulas):
    #        value = self.format_and_eval_string(formula[1])
    #        self.write_in_database(formula[0], value)

        for key in self.formulas:
            value = self.format_and_eval_string(self.formulas[key])
            #self.database_entries[key] = value
            self.write_in_database(key, value)

    def check(self, *args, **kwargs):
        """
        """
        traceback = {}
        test = True
        for key in self.formulas:
            try:
                value = self.format_and_eval_string(self.formulas[key])
                self.write_in_database(key, value)
            except Exception as e:
                test = False
                name = self.path + '/' + self.name + '/' + key
                traceback[name] =\
                    "Failed to eval the formula {}: {}".format(key, e)
        return test, traceback

    def prepare(self):
        ""
        print(self.formulas)
        dat = self.database_entries.copy()
        for key in self.formulas:
            dat[key] = "1.0"
        self.database_entries = dat
        print(self.database_entries)

#    def add_entry(self, key, value):
#        dict =

    def _post_setattr_formulas(self, old, new):
        """ Observer adding the new definitions to the database.

        """
        self.database_entries = {key: 1.0 for key in new}
        print("database entries:")
        print(self.database_entries)
        print(self.database.go_to_path('root').data)
