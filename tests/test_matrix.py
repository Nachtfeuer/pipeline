"""Testing of class Stage."""
# pylint: disable=no-self-use, invalid-name
import unittest
from hamcrest import assert_that, equal_to

from spline.components.config import ApplicationOptions
from spline.matrix import Matrix, MatrixProcessData, matrix_worker


class TestMatrix(unittest.TestCase):
    """Testing of class Matrix."""

    def test_simple_with_one_entry(self):
        """Testing simple matrix with one entry."""
        matrix_definition = [{'name': 'one', 'env': {'message': 'hello'}}]
        pipeline_definition = [{'stage(test)': [{
            'tasks': [{'shell': {'script': '''echo tasks1:hello1''', 'when': ''}},
                      {'shell': {'script': '''echo tasks1:hello2''', 'when': ''}}]}]}]

        process_data = MatrixProcessData()
        process_data.pipeline = pipeline_definition
        process_data.options = ApplicationOptions(definition='fake.yaml')

        matrix = Matrix(matrix_definition, parallel=False)
        result = matrix.process(process_data)
        output = [line for line in result['output'] if line.find("hello") >= 0]

        assert_that(result['success'], equal_to(True))
        assert_that(len(output), equal_to(2))
        assert_that(output[0], equal_to('tasks1:hello1'))
        assert_that(output[1], equal_to('tasks1:hello2'))

    def test_with_tags_and_filter_ordered(self):
        """Testing simple matrix with tags and filtering."""
        matrix_definition = [
            {'name': 'one', 'env': {'message': 'hello1'}, 'tags': ['group-a']},
            {'name': 'two', 'env': {'message': 'hello2'}, 'tags': ['group-b']},
            {'name': 'three', 'env': {'message': 'hello3'}, 'tags': ['group-a']}
        ]
        pipeline_definition = [{'stage(test)': [{
            'tasks': [{'shell': {'script': '''echo $message''', 'when': ''}}]}]}]

        process_data = MatrixProcessData()
        process_data.pipeline = pipeline_definition
        process_data.options = ApplicationOptions(definition='fake.yaml', matrix_tags='group-a')

        matrix = Matrix(matrix_definition, parallel=False)
        result = matrix.process(process_data)
        output = [line for line in result['output'] if line.find("hello") >= 0]

        assert_that(result['success'], equal_to(True))
        assert_that(len(output), equal_to(2))
        assert_that(output[0], equal_to('hello1'))
        assert_that(output[1], equal_to('hello3'))

    def test_with_tags_and_filter_parallel(self):
        """Testing simple matrix with tags and filtering."""
        matrix_definition = [
            {'name': 'one', 'env': {'message': 'hello1'}, 'tags': ['group-a']},
            {'name': 'two', 'env': {'message': 'hello2'}, 'tags': ['group-b']},
            {'name': 'three', 'env': {'message': 'hello3'}, 'tags': ['group-a']}
        ]
        pipeline_definition = [{'stage(test)': [{
            'tasks': [{'shell': {'script': '''echo $message''', 'when': ''}}]}]}]

        process_data = MatrixProcessData()
        process_data.pipeline = pipeline_definition
        process_data.options = ApplicationOptions(definition='fake.yaml', matrix_tags='group-a')

        matrix = Matrix(matrix_definition, parallel=True)
        result = matrix.process(process_data)
        output = sorted([line for line in result['output'] if line.find("hello") >= 0])

        assert_that(result['success'], equal_to(True))
        assert_that(len(output), equal_to(2))
        assert_that(output[0], equal_to('hello1'))
        assert_that(output[1], equal_to('hello3'))

    def test_failed_ordered(self):
        """Testing failed ordered."""
        matrix_definition = [
            {'name': 'one', 'env': {'message': 'hello1'}},
            {'name': 'two', 'env': {'message': 'hello2'}}
        ]
        pipeline_definition = [{'stage(test)': [{
            'tasks': [{'shell': {'script': '''exit 123''', 'when': ''}}]}]}]

        process_data = MatrixProcessData()
        process_data.pipeline = pipeline_definition
        process_data.options = ApplicationOptions(definition='fake.yaml')

        matrix = Matrix(matrix_definition, parallel=False)
        result = matrix.process(process_data)
        output = [line for line in result['output'] if line.find("hello") >= 0]

        assert_that(result['success'], equal_to(False))
        assert_that(len(output), equal_to(0))

    def test_failed_parallel(self):
        """Testing failed parallel."""
        matrix_definition = [
            {'name': 'one', 'env': {'message': 'hello1'}},
            {'name': 'two', 'env': {'message': 'hello2'}}
        ]
        pipeline_definition = [{'stage(test)': [{
            'tasks': [{'shell': {'script': '''exit 123''', 'when': ''}}]}]}]

        process_data = MatrixProcessData()
        process_data.pipeline = pipeline_definition
        process_data.options = ApplicationOptions(definition='fake.yaml')

        matrix = Matrix(matrix_definition, parallel=True)
        result = matrix.process(process_data)
        output = [line for line in result['output'] if line.find("hello") >= 0]

        assert_that(result['success'], equal_to(False))
        assert_that(len(output), equal_to(0))

    def test_matrix_worker(self):
        """Testing worker for matrix used in multiprocessing."""
        pipeline_definition = [{'stage(test)': [{
            'tasks': [{'shell': {'script': '''echo $message''', 'when': ''}}]}]}]

        result = matrix_worker({
            'matrix': {'name': 'one', 'env': {'message': 'hello1'}},
            'pipeline': pipeline_definition,
            'model': {},
            'options': ApplicationOptions(definition='fake.yaml'),
            'hooks': None
        })

        output = [line for line in result['output'] if line.find("hello") >= 0]

        assert_that(result['success'], equal_to(True))
        assert_that(len(output), equal_to(1))

    def test_dry_run(self):
        """Testing simple matrix with tags and filtering."""
        matrix_definition = [
            {'name': 'one', 'env': {'message': 'hello1'}},
            {'name': 'two', 'env': {'message': 'hello2'}},
            {'name': 'three', 'env': {'message': 'hello3'}}
        ]
        pipeline_definition = [{'stage(test)': [{
            'tasks': [{'shell': {'script': '''echo {{ env.message }}''', 'when': ''}}]}]}]

        process_data = MatrixProcessData()
        process_data.pipeline = pipeline_definition
        process_data.options = ApplicationOptions(definition='fake.yaml', dry_run=True)

        matrix = Matrix(matrix_definition, parallel=True)
        result = matrix.process(process_data)
        output = [line for line in result['output'] if len(line) > 0]

        assert_that(result['success'], equal_to(True))
        assert_that(len(output), equal_to(6))
        assert_that(output[0], equal_to('#!/bin/bash'))
        assert_that(output[1], equal_to('echo hello1'))
        assert_that(output[2], equal_to('#!/bin/bash'))
        assert_that(output[3], equal_to('echo hello2'))
        assert_that(output[4], equal_to('#!/bin/bash'))
        assert_that(output[5], equal_to('echo hello3'))
