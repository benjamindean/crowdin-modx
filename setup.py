from setuptools import setup

setup(
        name='crowdin-parse',
        version='1.0',
        py_modules=['crowdin_parse'],
        install_requires=[
            'Click',
        ],
        entry_points='''
            [console_scripts]
            crowdin-parse=crowdin_parse:cli
        '''
)
