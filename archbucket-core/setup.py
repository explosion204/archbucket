from setuptools import find_packages, setup

setup(
    name='archbucket',
    author='Dmitriy Karnyshov',
    author_email='dzmitriy20magic@gmail.com',
    packages=find_packages(),
    python_requires='>=3.6',
    entry_points={ 
        'console_scripts': [
            'archbucket=archbucket.main:main',
        ],
    },
    include_package_data=True
)