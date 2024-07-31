from setuptools import setup, find_packages

setup(
    name='mysqlhelper',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'mysql-connector-python',
    ],
    author='Kent010341',
    author_email='kent010341@gmail.com',
    description='A simple database connection and operation package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kent010341/mysql-helper',  # 填寫你的GitHub地址
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
