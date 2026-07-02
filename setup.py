"""Setup script for WordCloud Emergence."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wordcloud-emergence",
    version="1.0.0",
    author="hazelian0619",
    author_email="hazelian0619@example.com",
    description="GAT-Powered Semantic Network Exploration - Between two concepts, find the third that doesn't yet exist",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hazelian0619/wordcloud2tester",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires=">=3.8",
    install_requires=[
        # 运行时真实依赖：仅 LLM 网关调用 + 环境变量加载。
        # 历史上曾声明 torch/torch-geometric/transformers/fastapi 等，但代码从未使用，已移除。
        "openai==0.28.0",
        "python-dotenv==1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.0",
            "black==23.7.0",
            "flake8==6.0.0",
            "mypy==1.5.1",
            "pre-commit==3.5.0",
            "coverage==7.3.0",
        ],
        "docs": [
            "sphinx==7.2.6",
            "sphinx-rtd-theme==1.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "wordcloud-emergence=wordcloud_emergence.cli:main",
        ],
    },
)