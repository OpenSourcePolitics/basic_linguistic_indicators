# easy_wordclouds

Easy wordclouds API  


## Run in local with Docker

easy_wordclouds API can be run using Docker, to do so, you must have a Docker on your local system.

**Run API**

You can deploy your API on docker with a single command

```
make start
```

A new image named `rg.fr-par.scw.cloud/osp-internal-tools/basic_linguistic_indicators:latest` should be created

Then you should have a running container, on your current shell session, your API is ready for handling request

**Create request using cURL**

You can easily create a request using cURL, you need to pass a data-raw argument containing preprocessed data json. 
Json data needs to be output from [NLP preprocessing](https://github.com/OpenSourcePolitics/nlp_preprocessing)

You can find light JSON output at `./test_data/preprocessed.json`, you can add this content in cURL request at `<YOUR_JSON_PREPROCESSED_DATA>`.

```
curl --location --request POST 'http://0.0.0.0:8080/' \
--header 'Content-Type: application/json' \
--data-raw '<YOUR_JSON_PREPROCESSED_DATA>' -L -o easy_wordclouds.zip
```

At the end of process, you should have a new zip file named `easy_wordclouds.zip`.
s
