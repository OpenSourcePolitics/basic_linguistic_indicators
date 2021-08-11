import os
import argparse
from utils.data_manipulation import parse_data
from utils.word_frequency_data_interface import WordFrequenciesByCategory, \
    LocalWordFrequencyDataLoading,\
    WordFrequencies,\
    ApiWordFrequencyDataLoading
from wordclouds_generation.wordcloud_creation import create_wordcloud_from_frequency, get_most_common_words
from linguistic_database.ldb_creation import update_template_xlsx

MAIN_PATH = os.path.split(os.path.realpath(__file__))[0]


def parse_cli_arguments() -> argparse.Namespace:
    """
    Adds an argument to the cli execution : file_path
    use python get_all_statistical_indicators_from_file.py -h to access information about the argument.
    :return: list of arguments accessible for a cli execution
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",
                        "--file_path",
                        type=str,
                        help="path to the Decidim-like data to be preprocessed :"
                             " supported extensions are .json and the data should be formatted as"
                             "the output of the nlp_preprocessing project.",
                        required=True)
    parser.add_argument("-sc",
                        "--subset_category",
                        help="String used to subset the data :  it corresponds to the Decidim"
                             "classes that structures the consultation.",
                        required=False)
    return parser.parse_args()


def get_parsed_data(unparsed_data: WordFrequenciesByCategory, category=None) -> WordFrequencies:
    return WordFrequencies(preprocessed=parse_data(unparsed_data.preprocessed, category),
                           unprocessed=parse_data(unparsed_data.unprocessed, category))


def generate_statistical_insights_from_preprocessed_data(parsed_word_frequency_data_preprocessed: dict, category=None):
    create_wordcloud_from_frequency(parsed_word_frequency_data_preprocessed, category)
    # get_most_common_words(parsed_word_frequency_data_preprocessed)


def get_linguistic_database_indicators(parsed_word_frequency_data: dict, category=None) -> None:
    update_template_xlsx(template_path=MAIN_PATH + "/criteria_template.xlsx",
                         parsed_word_frequency_data=parsed_word_frequency_data,
                         category=category)


def get_all_statistical_indicators_from_file(local_file_path: str, category=None):
    unparsed_data = LocalWordFrequencyDataLoading(local_file_path).load()
    parsed_data = get_parsed_data(unparsed_data, category)
    generate_statistical_insights_from_preprocessed_data(parsed_data.preprocessed, category)
    get_linguistic_database_indicators(parsed_data.unprocessed, category)


def get_all_statistical_indicators_from_api(post_request_data: dict, category=None):
    unparsed_data = ApiWordFrequencyDataLoading(post_request_data).load()
    parsed_data = get_parsed_data(unparsed_data, category)
    generate_statistical_insights_from_preprocessed_data(parsed_data.preprocessed, category)
    get_linguistic_database_indicators(parsed_data.unprocessed, category)


if __name__ == '__main__':
    ARGS = parse_cli_arguments()
    get_all_statistical_indicators_from_file(ARGS.file_path, ARGS.subset_category)
