FROM quentinlp/nlp_repo_public_test:latest

RUN mkdir ./dist

RUN mv *.json ./dist

RUN python3.8 -m pip install --upgrade pip

COPY ./criteria_template.xlsx ./criteria_template.xlsx

COPY ./utils ./utils

COPY ./linguistic_database ./linguistic_database

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./wordclouds_generation ./wordclouds_generation

COPY main.py .

CMD python3.8 ./main.py -f ./dist/nlp_preprocessing_output.json
