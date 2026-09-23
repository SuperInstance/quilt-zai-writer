from setuptools import setup, find_packages
setup(
    name="quilt-zai-writer",
    version="0.1.0",
    description="Creative canon writing via ZAI GLM-4.5",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Casey / SuperInstance",
    packages=find_packages(),
    python_requires=">=3.8",
)
