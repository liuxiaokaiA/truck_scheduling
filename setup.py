from setuptools import setup, find_packages


setup(
    name='truck_scheduling',
    version='1.0',
    description='truck_scheduling',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'deap',
        'scoop',
    ],
    classifiers=[
        'Programming Language :: Python',
    ],
)
