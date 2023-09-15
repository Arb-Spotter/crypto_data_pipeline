from setuptools import find_packages, setup

setup(
    name="pricing_pipelines",
    packages=find_packages(exclude=["pricing_pipelines_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
