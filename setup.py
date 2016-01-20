from setuptools import setup

setup(
        name='crowdin-modx',
        version='0.1',
        py_modules=['crowdin_modx'],
        install_requires=[
            'Click',
        ],
        entry_points='''
            [console_scripts]
            crowdin-modx=crowdin_modx:cli
        '''
)
