from setuptools import setup, find_packages

setup(
    name='helloworld',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_marshmallow',
        'flask_sqlalchemy',
        'passlib',
        'sendgrid',
        'wtforms',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
