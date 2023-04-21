from setuptools import setup

setup(
    name='donations',
    packages=['src'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
