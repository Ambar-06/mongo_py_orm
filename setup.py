from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A lightweight Python Object-Relational Mapper (ORM)-like implementation for MongoDB'
with open('README.md', 'r', encoding='utf-8') as f: 
    LONG_DESCRIPTION = f.read()

setup(
    name="MongoPyORM",
    version=VERSION,
    author="Ambar Rizvi",
    author_email="<brannstrom9911@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    py_modules=["mongo_orm", "client"],
    package_dir=find_packages(),
    install_requires=[
        "pymongo>=3.11",   # To interact with MongoDB
        "bson>=0.5"        # For BSON-specific operations like ObjectId
    ],
    keywords=['mongodb', 'ORM', 'database', 'MongoDB ORM', "Django", "Django ORM"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    package_data={
        'mongopyorm': ['mongo_client/*.py', 'mongopyorm/*.py'],
    },
    python_requires='>=3.6',
)