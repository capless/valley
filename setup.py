from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)

version = '1.4.1'

LONG_DESCRIPTION = """
=======================
Valley
=======================

Python extensible schema validations and declarative syntax helpers.


"""

setup(
    name='valley',
    version=version,
    description="""Python extensible schema validations and declarative syntax helpers.""",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
    ],
    keywords='validations,schema,declarative',
    author='Brian Jinwright',
    author_email='opensource@capless.io',
    maintainer='Brian Jinwright',
    packages=find_packages(),
    url='https://github.com/capless/valley',
    license='GNU GPL V3',
    install_requires=[str(ir.req) for ir in install_reqs],
    include_package_data=True,
)
