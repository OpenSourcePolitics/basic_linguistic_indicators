"""
Project API
"""
import os
import sys
import html
import traceback
import requests
from dotenv import load_dotenv
from functools import wraps
from flask import Flask, jsonify, request, send_file, make_response
from utils.word_frequency_data_interface import ApiWordFrequencyDataLoading
from main import get_all_statistical_indicators_from_api, \
    generate_statistical_insights_from_preprocessed_data, \
    get_linguistic_database_indicators, get_parsed_data
from utils.system_functions import clean_directory

API_PATH = os.path.split(os.path.realpath(__file__))[0]

load_dotenv()
app = Flask(__name__)

def required_params_are_present(request_args):
    if len(request_args) < 1:
        return False

    if 'token' in request_args and 'analysis_id' in request_args:
        if request_args["token"] == "" or request_args["analysis_id"] == "":
            return False
        else:
            return True
    else:
        return False

def check_subset_category():
    if "subset_category" not in request.args:
        subset_category = None
    else:
        subset_category = html.unescape(request.args['subset_category'])
    return subset_category

def load_preprocessed_data(filenmae) -> dict:
    with open(os.path.join(API_PATH, filename), 'r', encoding='utf-8') as file:
        return json.load(file)

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
            return jsonify({'message': 'Invalid data'}), 400
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
    try:
        if required_params_are_present(request.args):
            params = {
                "token": request.args['token'],
                "analysis_id": request.args['analysis_id']
            }
        else:
            return jsonify({'message': 'Required params are missing or invalid'}), 400

        subset_category = check_subset_category()
        data = request.get_json()

        get_all_statistical_indicators_from_api(post_request_data=data,
                                                category=subset_category)

        parsed_file = os.path.join(API_PATH, 'dist/basic_linguistic_indicators.zip')
        requests.post(os.environ.get('RAILS_APP_ENDPOINT'), params=params, files={"archive": ("basic_linguistic_indicators.zip", open(parsed_file, 'rb'))})
        response = make_response(send_file(
            path_or_file=parsed_file,
            mimetype="application/zip",
            as_attachment=True,
            download_name="basic_linguistic_indicators"
        ))
        response.headers['Content-Disposition'] = "attachment; filename=basic_linguistic_indicators"
        return response
    except Exception as execution_error:
        print(type(execution_error))
        print(execution_error.args)
        traceback.print_exc(file=sys.stdout)
        print(execution_error)
        return jsonify(
            {'message': 'An unexpected error occured'}
        ), 500



@app.route('/ldb', methods=["POST"])
def get_speech_analysis_indicators():
    try:
        if required_params_are_present(request.args):
            params = {
                "token": request.args['token'],
                "analysis_id": request.args['analysis_id']
            }
        else:
            return jsonify({'message': 'Required params are missing or invalid'}), 400

        subset_category = check_subset_category()
        data = load_data_from_post_request(subset_category=subset_category)

        get_linguistic_database_indicators(parsed_word_frequency_data=data.unprocessed,
                                           category=subset_category)

        speech_analysis_data = os.path.join(API_PATH, 'dist/linguistic_database_template.xlsx')
        requests.post(os.environ.get('RAILS_APP_ENDPOINT'), params=params, files={"archive": ("linguistic_database_template.xlsx", open(speech_analysis_data, 'rb'))})
        response = make_response(send_file(
            path_or_file=speech_analysis_data,
            mimetype="application/vnd.ms-excel",
            as_attachment=True,
            download_name="ldb_indicators.xlsx"
        ))
        response.headers['Content-Disposition'] = "attachment; filename=ldb_indicators.xlsx"
        return response
    except Exception as execution_error:
        print(type(execution_error))
        print(execution_error.args)
        traceback.print_exc(file=sys.stdout)
        print(execution_error)
        return jsonify(
           {'message': 'An unexpected error occured'}
       ), 500


@app.route('/wordclouds', methods=["POST"])
def get_word_clouds():
    try:
        if required_params_are_present(request.args):
            params = {
                "token": request.args['token'],
                "analysis_id": request.args['analysis_id']
            }
        else:
            return jsonify({'message': 'Required params are missing or invalid'}), 400
        subset_category = check_subset_category()
        data = load_data_from_post_request(subset_category=subset_category)

        generate_statistical_insights_from_preprocessed_data(parsed_word_frequency_data_preprocessed=data.preprocessed,
                                                             category=subset_category)

        if subset_category is None:
            word_cloud_image = os.path.join(API_PATH, 'dist/wordcloud.png')
        else:
            word_cloud_image = os.path.join(API_PATH, 'dist/wordcloud{}.png'.format("_" + subset_category))

        requests.post(os.environ.get('RAILS_APP_ENDPOINT'), params=params, files={"archive": ("wordcloud.png", open(word_cloud_image, 'rb'))})
        response = make_response(send_file(
            path_or_file=word_cloud_image,
            mimetype="application/png",
            as_attachment=True,
            download_name="wordcloud"
        ))
        response.headers['Content-Disposition'] = "attachment; filename=wordcloud"

        return response
    except Exception as execution_error:
        print(type(execution_error))
        print(execution_error.args)
        traceback.print_exc(file=sys.stdout)
        print(execution_error)
        return jsonify(
           {'message': 'An unexpected error occured'}
        ), 500

if __name__ == "__main__":
    app.run()
