from setuptools import setup, find_packages

setup(
    name='colab_remote',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Ehsan KhademOlama',
    author_email='ekoshv.igt@gmail.com',
    description='A Python library for interacting with a remote Google Colab API',
)
