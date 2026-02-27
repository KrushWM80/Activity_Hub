"""Setup configuration for Zorro video generation system."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zorro",
    version="0.1.0",
    author="Walmart US Stores - Activity Messages Team",
    author_email="your.email@walmart.com",
    description="AI-powered video generation for Walmart activity messages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/walmart/zorro",
    packages=find_packages(exclude=["tests", "tests.*", "docs", "examples"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pydantic>=2.5.0",
        "pyyaml>=6.0.1",
        "python-dotenv>=1.0.0",
        "openai>=1.3.0",
        "diffusers>=0.24.0",
        "transformers>=4.35.0",
        "torch>=2.1.0",
        "moviepy>=1.0.3",
        "opencv-python>=4.8.1.78",
        "pillow>=10.1.0",
        "pydub>=0.25.1",
        "gTTS>=2.4.0",
        "webvtt-py>=0.4.6",
        "requests>=2.31.0",
        "structlog>=23.2.0",
        "tenacity>=8.2.3",
        "click>=8.1.7",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "zorro=src.cli:main",
        ],
    },
)
