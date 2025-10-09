from setuptools import setup, find_packages

SETUP_E = '-e .'
def get_requirements(file_name):

    with open(file_name) as file:
        contents = file.readlines()
        contents = [line.strip() for line in contents if line.strip() and not line.startswith('-e')]
        return contents

setup(
    name='Vehicle_Insurance',
    version='0.0.1',
    description='Vehicle Insurance Domain',
    author='Md. Samsul Arefin',
    packages=find_packages(),
    install_requires=get_requirements(file_name='requirements.txt'),
)