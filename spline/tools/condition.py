"""Provide condition for a task for conditional execution."""
# Copyright (c) 2018 Thomas Lehmann
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# pylint: disable=useless-super-delegation
# pylint: disable=too-many-instance-attributes
import re
import ast

from spline.tools.logger import Logger


class TokensCompressor(object):
    """Compressing ast tokens (lists)."""

    def __init__(self, ast_tokens):
        """Initialize compressor with tokens."""
        self.ast_tokens = ast_tokens
        self.final_ast_tokens = []
        self.list_level = 0
        self.list_entry = None
        self.dispatcher = {
            ast.List: self.__begin_of_list,
            ast.Load: self.__end_of_list,
            'default': self.__default
        }

    def __begin_of_list(self, ast_token):
        """Handle begin of a list."""
        self.list_level += 1
        if self.list_level == 1:
            self.final_ast_tokens.append(ast_token)

    def __end_of_list(self, ast_token):
        """Handle end of a list."""
        self.list_level -= 1
        if self.list_level == 0:
            if self.list_entry is not None:
                self.final_ast_tokens.append(self.list_entry)
                self.list_entry = None
            self.final_ast_tokens.append(ast_token)

    def __default(self, ast_token):
        """Handle tokens inside the list or outside the list."""
        if self.list_level == 1:
            if self.list_entry is None:
                self.list_entry = ast_token
            elif not isinstance(ast_token, type(self.list_entry)):
                self.final_ast_tokens.append(ast_token)
        elif self.list_level == 0:
            self.final_ast_tokens.append(ast_token)

    def compress(self):
        """Main function of compression."""
        for ast_token in self.ast_tokens:
            if type(ast_token) in self.dispatcher:  # pylint: disable=unidiomatic-typecheck
                self.dispatcher[type(ast_token)](ast_token)
            else:
                self.dispatcher['default'](ast_token)


class Condition(object):
    """Verification and evaluation of a simple condition."""

    RULES = [{
        'name': 'str-eq-str',
        'types': [ast.Compare, ast.Str, ast.Eq, ast.Str],
        'evaluate': lambda tokens: tokens[3].s == tokens[5].s
    }, {
        'name': 'str-neq-str',
        'types': [ast.UnaryOp, ast.Not, ast.Compare, ast.Str, ast.Eq, ast.Str],
        'evaluate': lambda tokens: not tokens[5].s == tokens[7].s
    }, {
        'name': 'num-eq-num',
        'types': [ast.Compare, ast.Num, ast.Eq, ast.Num],
        'evaluate': lambda tokens: tokens[3].n == tokens[5].n
    }, {
        'name': 'num-neq-num',
        'types': [ast.UnaryOp, ast.Not, ast.Compare, ast.Num, ast.Eq, ast.Num],
        'evaluate': lambda tokens: not tokens[5].n == tokens[7].n
    }, {
        'name': 'num-gt-num',
        'types': [ast.Compare, ast.Num, ast.Gt, ast.Num],
        'evaluate': lambda tokens: tokens[3].n > tokens[5].n
    }, {
        'name': 'num-gte-num',
        'types': [ast.Compare, ast.Num, ast.GtE, ast.Num],
        'evaluate': lambda tokens: tokens[3].n >= tokens[5].n
    }, {
        'name': 'num-lt-num',
        'types': [ast.Compare, ast.Num, ast.Lt, ast.Num],
        'evaluate': lambda tokens: tokens[3].n < tokens[5].n
    }, {
        'name': 'num-lte-num',
        'types': [ast.Compare, ast.Num, ast.LtE, ast.Num],
        'evaluate': lambda tokens: tokens[3].n <= tokens[5].n
    }, {
        'name': 'num-in-list',
        'types': [ast.Compare, ast.Num, ast.In, ast.List, ast.Num, ast.Load],
        'evaluate': lambda tokens: tokens[3].n in [token.n for token in tokens[6:-1]]
    }, {
        'name': 'num-nin-list',
        'types': [ast.Compare, ast.Num, ast.NotIn, ast.List, ast.Num, ast.Load],
        'evaluate': lambda tokens: tokens[3].n not in [token.n for token in tokens[6:-1]]
    }, {
        'name': 'str-in-list',
        'types': [ast.Compare, ast.Str, ast.In, ast.List, ast.Str, ast.Load],
        'evaluate': lambda tokens: tokens[3].s in [token.s for token in tokens[6:-1]]
    }, {
        'name': 'str-nin-list',
        'types': [ast.Compare, ast.Str, ast.NotIn, ast.List, ast.Str, ast.Load],
        'evaluate': lambda tokens: tokens[3].s not in [token.s for token in tokens[6:-1]]
    }]

    @staticmethod
    def get_tokens(condition):
        """
        Get AST tokens for Python condition.

        Returns:
            list: list of AST tokens
        """
        try:
            ast_tokens = list(ast.walk(ast.parse(condition.strip())))
        except SyntaxError as exception:
            Logger.get_logger(__name__).error("Syntax error: %s", exception)
            ast_tokens = []
        return ast_tokens

    @staticmethod
    def match_tokens(ast_tokens, ast_types):
        """
        Verify that each token in order does match the expected types.

        The list provided by `get_tokens` does have three more elements
        at the beginning of the list which should be always the same
        for a condition (Module and Expr). Those are automatically
        added first to the final list of expected types so you don't have
        to specify it yourself each time.

        >>> tokens = Condition.get_tokens('2 == 3')
        >>> Condition.match_tokens(tokens, [ast.Compare, ast.Num, ast.Eq, ast.Num])
        True

        Args:
            ast_entries (list): list of AST tokens parsers previously.
            ast_types (list): list of expected AST types.

        Returns:
            bool: when all tokes match the expected types
        """
        ast_final_types = [ast.Module, ast.Expr] + ast_types
        return all(isinstance(ast_token, ast_type)
                   for ast_token, ast_type in zip(ast_tokens, ast_final_types))

    @staticmethod
    def compress_tokens(ast_tokens):
        """
        Compress entries when there is a list.

        The function is for simplifying the verification;
        when there is a list of multiple integers we just
        need one entry that we can match that setup as the
        example below demonstrates:

        >>> ast_tokens = Condition.get_tokens('2 in [1, 2, 3, 4, 5, 6]')
        >>> ast_compressed_tokens = Condition.compress_tokens(ast_tokens)
        >>> expected_types = [ast.Module, ast.Expr, ast.Compare,
        ...                   ast.Num, ast.In, ast.List, ast.Num, ast.Load]
        >>> expected_types == [type(token) for token in ast_compressed_tokens]
        True

        Args:
            ast_tokens (list): AST tokens as provided by `Condition.get_tokens`.

        Returns:
            list: compressed tokens.
        """
        compressor = TokensCompressor(ast_tokens)
        compressor.compress()
        return compressor.final_ast_tokens

    @staticmethod
    def is_valid(condition):
        """
        Verify condition (format).

        >>> Condition.is_valid('{{ foo }} == 42')
        True
        >>> Condition.is_valid('"{{ foo }}" == 42')
        False
        >>> Condition.is_valid('  not "{{ foo }}" == "42"  ')
        True
        >>> Condition.is_valid('  not {{ foo }} == 42  ')
        True
        >>> Condition.is_valid('{{ foo }} in [ 42, 43, 44 ]')
        True
        """
        matched = False

        if len(condition) > 0:
            final_condition = re.sub('{{.*}}', '42', condition)
            ast_tokens = Condition.get_tokens(final_condition)
            ast_compressed_tokens = Condition.compress_tokens(ast_tokens)

            for rule in Condition.RULES:
                if Condition.match_tokens(ast_compressed_tokens, rule['types']):
                    matched = True
                    break
        else:
            matched = True

        return matched

    @staticmethod
    def find_rule(condition):
        """
        Find rule for given condition.

        Args:
            condition (str): Python condition as string.

        Returns:
            str, list, function: found rule name, list of AST tokens for condition
                                 and verification function.
        """
        final_condition = re.sub('{{.*}}', '42', condition)
        ast_tokens = Condition.get_tokens(final_condition)
        ast_compressed_tokens = Condition.compress_tokens(ast_tokens)

        name = 'undefined'
        function = lambda tokens: False

        if len(ast_compressed_tokens) > 0:
            for rule in Condition.RULES:
                if Condition.match_tokens(ast_compressed_tokens, rule['types']):
                    name = rule['name']
                    function = rule['evaluate']
                    break
        return name, ast_tokens, function

    @staticmethod
    def evaluate(condition):
        """
        Evaluate simple condition.

        >>> Condition.evaluate('  2  ==  2  ')
        True
        >>> Condition.evaluate('  not  2  ==  2  ')
        False
        >>> Condition.evaluate('  not  "abc"  ==  "xyz"  ')
        True
        >>> Condition.evaluate('2 in [2, 4, 6, 8, 10]')
        True
        >>> Condition.evaluate('5 in [2, 4, 6, 8, 10]')
        False
        >>> Condition.evaluate('"apple" in ["apple", "kiwi", "orange"]')
        True
        >>> Condition.evaluate('5 not in [2, 4, 6, 8, 10]')
        True
        >>> Condition.evaluate('"apple" not in ["kiwi", "orange"]')
        True

        Args:
            condition (str): Python condition as string.

        Returns:
            bool: True when condition evaluates to True.
        """
        success = False
        if len(condition) > 0:
            try:
                rule_name, ast_tokens, evaluate_function = Condition.find_rule(condition)
                if not rule_name == 'undefined':
                    success = evaluate_function(ast_tokens)
            except AttributeError as exception:
                Logger.get_logger(__name__).error("Attribute error: %s", exception)
        else:
            success = True
        return success
