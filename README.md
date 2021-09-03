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

## Configure CD with Github Secrets

This Continuous Deployment workflows requires some secrets to work. Here is the list of secrets required: 

- `REGISTRY_ENDPOINT`: Registry endpoint for container image 
- `REGISTRY_NAMESPACE`: Registry namespace for container image
- `IMAGE_NAME`: Image name to push on registry
- `PRODUCTION_TAG`: Tag name when CD is executing for production image
- `DEVELOPMENT_TAG`: Tag name when CD is executing for development image
- `TOKEN`: Token for authenticating on the registry

You can easily set up your secrets on the repository using the web interface : Settings > Secrets > New repository secret

Or you can use the [Github CLI](https://github.com/cli/cli) to [define secret on repository](https://cli.github.com/manual/gh_secret_set).
