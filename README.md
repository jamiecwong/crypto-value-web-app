# Crypto value web app

This repo includes the application code, Dockerfile, Helm chart and GitHub Actions workflow used to deploy a crypto currency value web app.

## The application

The application is written as a python flask app, the code for which can be found in `./app.py`, with the HTML file `index.html` in `/templates`.

If I had more time:
- I designed the code with variables for the `coin_id` and `currency`, with the idea that we could pass these as container environment variables in the Helm chart. Meaning that the crypto currency and the currency values could both be changed easily.
- I retrieved the crypto currency value every minute by using a refresh in the HTML. This feels like a bit of a hack to me, I know that this can be done in Javascript with jquery ajax, so with more time I would have tried to implement that.
- I would have added tests for the python code.

## The Helm chart

The Helm chart lives in the `./chart` directory. It deploys the application as `service-a`.

- I chose to use a LoadBalancer service to expose the service. I set this to HTTP as I tested it in minikube. This should use HTTPS, be secured by an SSL certificate and use a friendly DNS name, all of which could be done with more time/seemed out of scope for this exercise.
- In an enterprise environment we might want to instead use an ingress controller for this.

If I had more time:
- I generated the Helm chart using `helm create`, it's very basic with just enough changes to deploy the service. With more time I would refine it and add options such as the `coin_id` and `currency` container env vars as mentioned above.

## The GitHub Actions workflow

The Github Actions workflow is defined in `.github/workflows/build-and-deploy.yaml`.

Workflow steps:
- build docker image
- scan the image for vulnerabilities using the action `snyk/actions/docker@master`
- lint the helm chart
- test installing the helm chart
- there is then an approval gate created using the `environment` argument. This allows us to check the results of the vulnerability test and helm linting and testing before proceeding.
- once approved the docker image is pushed to ECR, and the helm chart is deployed

If I had more time:
- For the purposes of the exercise I wanted to show all of this in one workflow. It might make sense to separate these jobs into different workflows and to deploy the Helm chart with a GitOps CD tool such as ArgoCD which will maintain the kubernetes objects state to match what is in the git repo.
