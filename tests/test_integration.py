"""
This file will test that the execution of the workflow is working properly
"""
import os
import pytest

TEST_INTEGRATION_PATH = os.path.split(os.path.realpath(__file__))[0]

STORED_TEST_DATA_MULTI_CATEGORIES = os.path.join(os.path.dirname(TEST_INTEGRATION_PATH),
                                                 "test_data/word_frequency_test.json")
STORED_TEST_DATA_ONE_CATEGORY = os.path.join(os.path.dirname(TEST_INTEGRATION_PATH),
                                             "test_data/word_frequency_test2.json")

CONFIG = [STORED_TEST_DATA_MULTI_CATEGORIES, STORED_TEST_DATA_ONE_CATEGORY]


@pytest.mark.parametrize("file_path", CONFIG)
def test_correct_execution(file_path):
    pytest.skip("TODO: fix this test")
    """
    Checks if the execution of the workflow went well (for the time being
    no category can be added to testing => unknown argument)
    """
    result = os.system("python {} -f {}".format(os.path.join(os.path.dirname(TEST_INTEGRATION_PATH), "main.py"),
                                                file_path))
    assert result == 0
