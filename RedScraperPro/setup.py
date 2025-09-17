from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="redscraperpro",
    version="1.0.0",
    author="yomazini",
    author_email="your.email@example.com",
    description="🩸 The Ultimate Reddit Scraping CLI Tool with Horror/Itachi Uchiha Aesthetic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yomazini/RedScraperPro",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.9.1",
            "flake8>=6.1.0",
            "mypy>=1.6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "redscraperpro=main:main",
            "rsp=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.json", "*.yaml", "*.yml"],
    },
    keywords="reddit scraping cli praw data-mining social-media analysis",
    project_urls={
        "Bug Reports": "https://github.com/yomazini/RedScraperPro/issues",
        "Source": "https://github.com/yomazini/RedScraperPro",
        "Documentation": "https://github.com/yomazini/RedScraperPro/blob/master/fullRedscrapperprohowtouse.pdf",
    },
)
