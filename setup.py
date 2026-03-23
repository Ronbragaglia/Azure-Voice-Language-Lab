from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="azure-voice-language-lab",
    version="1.0.0",
    author="Rone Bragaglia",
    author_email="ronbragaglia@gmail.com",
    description="Laboratório completo para exploração de Azure Speech e Language Studio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ronbragaglia/Azure-Voice-Language-Lab",
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "azure-cognitiveservices-speech>=1.46.0",
        "azure-ai-textanalytics>=5.3.0",
        "azure-ai-translation-text>=1.0.0",
        "azure-ai-language>=1.1.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "pydantic>=2.6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "black>=24.1.0",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
        ],
        "web": [
            "streamlit>=1.31.0",
            "gradio>=4.20.0",
        ],
        "audio": [
            "pydub>=0.25.0",
            "soundfile>=0.12.0",
        ],
        "visualization": [
            "matplotlib>=3.8.0",
            "seaborn>=0.13.0",
            "pandas>=2.2.0",
            "numpy>=1.26.0",
        ],
        "docs": [
            "sphinx>=7.2.0",
            "sphinx-rtd-theme>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "azure-speech-lab=src.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
