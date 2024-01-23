from setuptools import setup, find_packages

setup(
    name='DateFinder',
    version='1.0',
    packages=find_packages(),
    description='Machine learning approach to identifying date formats',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rob Salethorn',
    author_email='rob@salethorn.com',
    url='https://github.com/RSalethorn/DateFinder',
    include_package_data=True,
    install_requires=[
        "torch",
    ],
)