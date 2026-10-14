from setuptools import setup, find_packages

setup(
    name="ainoseclicker",
    version="1.0.0",
    description="NoseClicker AI — Первая нейросеть с тактильной отдачей и симулятором хрящей",
    packages=find_packages(),
    py_modules=["main"],
    install_requires=[
        "rich>=13.0.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.20.0",
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ainoseclicker=main:main",
            "noseclicker=main:main",
        ],
    },
)
