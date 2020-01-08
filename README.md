# tstest

This is modified version of [tstest](https://github.com/gsorry/tstest) to fit on "AWS Elastic Beanstalk" based on "AWS CodeStar sample web service".

This sample code is a simple Flask web service deployed by "AWS Elastic Beanstalk" and "AWS CloudFormation".


## Install

It is recommended to use the latest version of Python 3 and PyPy.

Clone the repository:
```shell script
git clone https://github.com/gsorry/ts.git
cd ts
```


Python 3 comes bundled with the `venv` module to create virtual environments.

Create a virtual environment:
```shell script
python3 -m venv venv
```

Before you work on your project, activate the corresponding environment:
```shell script
. venv/bin/activate
```

Within the activated environment, use the following command to install dependencies:
```shell script
pip3 install -r requirements.txt
```

Install the application code into your virtual environment:
```shell script
python3 setup.py install
```

## Run (Development only)

Export environment variable for Sendgrid API Key:
```shell script
export SENDGRID_API_KEY='<YOUR_SECRET_API_KEY>'
```

Now you can run your application.
Start the Flask development server:
```shell script
python helloworld/application.py --port 5000
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in a browser.

## Build and deploy

There is complete CI/CD pipeline created by "AWS CodeStar". To build and deploy application, just merge changes to master bracnh. Then CI/CD pipeline is triggered via web hook. Pipeline will pull changes form fit repository, build application and deploy it to "AWS Elastic Beanstalk". Then you can try application at: [http://tsapp.v9xnw3r22z.us-east-2.elasticbeanstalk.com/](http://tsapp.v9xnw3r22z.us-east-2.elasticbeanstalk.com/).
