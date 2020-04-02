from setuptools import find_packages, setup

setup(
    name='archbucket',
    author='Dmitriy Karnyshov',
    author_email='dzmitriy20magic@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'singleton3'
    ],
    python_requires='>=3.6',
    include_package_data=True
)