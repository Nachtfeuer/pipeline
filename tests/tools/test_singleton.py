"""Testing of module filter."""
# pylint: disable=no-self-use, invalid-name
import unittest
from hamcrest import assert_that, equal_to, is_not
from spline.tools.decorators import singleton


class TestSingleton(unittest.TestCase):
    """Testing of singleton decorator."""

    def test_without_parameters(self):
        """Testing singleton decorator without parameters."""
        @singleton
        class SingletonTest1(object):
            """Test singleton."""

            def __init__(self):
                """No parameters, no fields."""
                pass

        instance_a = SingletonTest1()
        instance_b = SingletonTest1()
        assert_that(instance_a, equal_to(instance_b))
        assert_that(id(instance_a), equal_to(id(instance_b)))

    def test_with_positional_arguments(self):
        """Testing singleton decorator with positional parameters."""
        @singleton
        class SingletonTest2(object):
            """Test singleton."""

            def __init__(self, value_a, value_b):
                """Init fields."""
                self.value_a = value_a
                self.value_b = value_b

        instance_a = SingletonTest2(10, "hello")
        instance_b = SingletonTest2(10, "hello")
        instance_c = SingletonTest2(20, "hello")
        assert_that(instance_a, equal_to(instance_b))
        assert_that(id(instance_a), equal_to(id(instance_b)))
        assert_that(instance_a.value_a, equal_to(instance_b.value_a))
        assert_that(instance_a.value_b, equal_to(instance_b.value_b))

        assert_that(instance_a, is_not(equal_to(instance_c)))
        assert_that(id(instance_a), is_not(equal_to(id(instance_c))))
        assert_that(instance_a.value_a, is_not(equal_to(instance_c.value_a)))
        assert_that(instance_a.value_b, equal_to(instance_c.value_b))

    def test_with_named_arguments(self):
        """Testing singleton decorator with named parameters."""
        @singleton
        class SingletonTest3(object):
            """Test singleton."""

            def __init__(self, value_a, value_b):
                """Init fields."""
                self.value_a = value_a
                self.value_b = value_b

        instance_a = SingletonTest3(10, value_b="hello")
        instance_b = SingletonTest3(10, value_b="hello")
        instance_c = SingletonTest3(10, "hello")
        assert_that(instance_a, equal_to(instance_b))
        assert_that(id(instance_a), equal_to(id(instance_b)))
        assert_that(instance_a.value_a, equal_to(instance_b.value_a))
        assert_that(instance_a.value_b, equal_to(instance_b.value_b))
        # also the field values are the same the instances are
        # different because of the different call.
        assert_that(instance_a, is_not(equal_to(instance_c)))
        assert_that(id(instance_a), is_not(equal_to(id(instance_c))))
        assert_that(instance_a.value_a, equal_to(instance_c.value_a))
        assert_that(instance_a.value_b, equal_to(instance_c.value_b))
