"""
This file will test that the execution of the workflow is working properly
"""
import os

TEST_INTEGRATION_PATH = os.path.split(os.path.realpath(__file__))[0]


def test_correct_execution():
    """
    Checks if the execution of the workflow went well
    """
    result = os.system("python {}/../main.py".format(TEST_INTEGRATION_PATH))
    assert result == 0
