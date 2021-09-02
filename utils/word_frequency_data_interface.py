"""
This file is used to define an Interface that
will act as an overlay between the script and the input data
"""
import os
import json
from typing import Dict
from dataclasses import dataclass

Category = str
Word = str
Frequency = int
WordFrequencyMapping = Dict[Word, Frequency]
WordFrequenciesCategoryMapping = Dict[Category, WordFrequencyMapping]


class WordFrequencyLoader:
    """
    Interface for data loading
    """
    def load(self):
        """
        method used to load data before it is passed to the processing
        functions
        """
        pass


@dataclass
class WordFrequenciesByCategory:
    """
    Data structure used to describe the raw data loaded from
    the api or the local json file.
    """
    filename: str
    preprocessed: WordFrequenciesCategoryMapping
    unprocessed: WordFrequenciesCategoryMapping


@dataclass
class WordFrequencies:
    """
    Data structure used to represent
    the preprocessed data and the classical one
    once the filter on category has been apply (see parse_data)
    """
    filename: str
    preprocessed: WordFrequencyMapping
    unprocessed: WordFrequencyMapping


class LocalWordFrequencyDataLoading(WordFrequencyLoader):
    """
    Implements the main interface and the methods load for
    when a local file is to be preprocessed
    """
    def __init__(self, file_path):
        self._file_path = file_path
        self._filename = os.path.basename(os.path.normpath(os.path.splitext(file_path)[0]))

    def load(self) -> WordFrequenciesByCategory:
        """
        implements the load method from WordFrequencyLoader interface
        in case of a local execution. It will load the data stored in a json file.
        and return both the preprocessed
        word frequencies and the classical one
        """
        with open(self._file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return WordFrequenciesByCategory(filename=self._filename,
                                         preprocessed=data["word_frequency_preprocessed"],
                                         unprocessed=data["word_frequency"])


class ApiWordFrequencyDataLoading(WordFrequencyLoader):
    """
    Implements the main interface WordFrequencyLoader to deal
    with the data that send by a post request to the API
    """
    def __init__(self, post_request_data, filename):
        self._post_request_data = post_request_data
        self._filename = filename

    def load(self) -> WordFrequenciesByCategory:
        """
        implements the load method from WordFrequencyLoader interface
        in case of a post request send by the API and returns both the preprocessed
        word frequencies and the classical one
        """
        return WordFrequenciesByCategory(filename=self._filename,
                                         preprocessed=self._post_request_data["word_frequency_preprocessed"],
                                         unprocessed=self._post_request_data["word_frequency"])
