from setuptools import setup, find_packages

setup(
    name='Excel-Item-Classifier',
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'openai',
        'pandas',
        'PyQt6'
    ],
    entry_points={
        'console_scripts': [
            'excel-item-classifier=main:main',
        ],
    },
)
