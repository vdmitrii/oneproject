from setuptools import setup

setup(name='forecasting',
      version='0.1',
      description='A simple package to wrap some forecasting functionality',
      author='Dima',
      license='MIT',
      packages=['catboost', 'numpy', 'pandas', 'seaborn'],
      zip_safe=False)