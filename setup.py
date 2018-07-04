from setuptools import setup, find_packages


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

version = '1.5.2'

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
    install_requires=parse_requirements('requirements.txt'),
    include_package_data=True,
)
