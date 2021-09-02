"""
Project API
"""
import os
import sys
import traceback
from functools import wraps
from flask import Flask, jsonify, request, send_file, make_response
from utils.word_frequency_data_interface import ApiWordFrequencyDataLoading
from main import get_all_statistical_indicators_from_api, \
    generate_statistical_insights_from_preprocessed_data, \
    get_linguistic_database_indicators, get_parsed_data
from utils.system_functions import clean_directory

API_PATH = os.path.split(os.path.realpath(__file__))[0]
app = Flask(__name__)


def check_subset_category():
    if "subset_category" not in request.args:
        subset_category = None
    else:
        subset_category = request.args['subset_category']
    return subset_category


def load_data_from_post_request(subset_category):
    raw_data = ApiWordFrequencyDataLoading(post_request_data=request.get_json()).load()
    parsed_data = get_parsed_data(raw_data, subset_category)
    return parsed_data


@app.teardown_request
def empty_dist_directory(response):
    """
    Function that will be called after the request
    to clean the dist directory. It will remove only the files
    that are not
    :param response:
    :return:
    """
    clean_directory(os.path.join(API_PATH, "dist"))
    return response


def check_correct_data(func):
    """
    decorator function used to check that the data is not null or invalid
    :param func: function on which the decorator is called
    :return:
    """

    @wraps(func)
    def wrapped(*args, **kwargs):
        data = request.get_json()
        if data is None:
            return jsonify({'message': 'Invalid data'}), 403
        return func(*args, **kwargs)

    return wrapped


@app.route('/', methods=["POST"])
@check_correct_data
def get_all_indicators():
    """
    This function get a json file transmitted by the
    client with a POST request.
    It then returns an archive containing the outputs of the script
    :return: Send the contents of a file to the client. see send_file documentation
    for further information
    """
    subset_category = check_subset_category()
    data = request.get_json()

    try:
        get_all_statistical_indicators_from_api(post_request_data=data,
                                                category=subset_category)
    except Exception as execution_error:
        print(type(execution_error))
        print(execution_error.args)
        traceback.print_exc(file=sys.stdout)
        print(execution_error)
        return jsonify(
            {'message': 'Error executing script'}
        ), 403
    parsed_file = os.path.join(API_PATH, 'dist/basic_linguistic_indicators.zip')
    response = make_response(send_file(
        path_or_file=parsed_file,
        mimetype="application/zip",
        as_attachment=True,
        download_name="basic_linguistic_indicators"
    ))
    response.headers['Content-Disposition'] = "attachment; filename=basic_linguistic_indicators"
    return response


@app.route('/ldb', methods=["POST"])
def get_speech_analysis_indicators():
    subset_category = check_subset_category()
    data = load_data_from_post_request(subset_category=subset_category)
    try:
        get_linguistic_database_indicators(parsed_word_frequency_data=data.unprocessed,
                                           category=subset_category)
    except Exception as execution_error:
        print(type(execution_error))
        print(execution_error.args)
        traceback.print_exc(file=sys.stdout)
        print(execution_error)
        return jsonify(
            {'message': 'Error executing script'}
        ), 403
    speech_analysis_data = os.path.join(API_PATH, 'dist/linguistic_database_template.xlsx')
    response = make_response(send_file(
        path_or_file=speech_analysis_data,
        mimetype="application/vnd.ms-excel",
        as_attachment=True,
        download_name="ldb_indicators.xlsx"
    ))
    response.headers['Content-Disposition'] = "attachment; filename=ldb_indicators.xlsx"
    return response


@app.route('/wordclouds', methods=["POST"])
def get_word_clouds():
    subset_category = check_subset_category()
    data = load_data_from_post_request(subset_category=subset_category)

    try:
        generate_statistical_insights_from_preprocessed_data(parsed_word_frequency_data_preprocessed=data.preprocessed,
                                                             category=subset_category)
    except Exception as execution_error:
        print(type(execution_error))
        print(execution_error.args)
        traceback.print_exc(file=sys.stdout)
        print(execution_error)
        return jsonify(
            {'message': 'Error executing script'}
        ), 403
    if subset_category is None:
        word_cloud_image = os.path.join(API_PATH, 'dist/wordcloud.png')
    else:
        word_cloud_image = os.path.join(API_PATH, 'dist/wordcloud{}.png'.format("_" + subset_category))
    response = make_response(send_file(
        path_or_file=word_cloud_image,
        mimetype="application/png",
        as_attachment=True,
        download_name="wordcloud"
    ))
    response.headers['Content-Disposition'] = "attachment; filename=wordcloud"
    return response


if __name__ == "__main__":
    app.run()
