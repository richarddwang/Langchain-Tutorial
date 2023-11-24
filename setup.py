import setuptools

with open("README.md", "r", encoding='utf-8') as d:
    long_description = d.read()

REQUIRED_PKGS = [
    # Environments
    'python-dotenv',
    # Langchain
    'langchain',
    'langchain_experimental',
    'langsmith',
    'langchainhub',
    'langserve',
    'httpx-sse', # for langserve
    'sse-starlette', # for langserve
    'fastapi', # for langserve
    # OpenAI
    'openai==0.28.1', # https://github.com/langchain-ai/langchain/issues/12958
    'tiktoken==0.4.0',
    # Text Generation Webui
    'sshconf',
    'sshtunnel',
]

TUTORIAL_REQUIRED_PKGS = [
    # Lock Versions
    'langchain==0.0.334',
    'langchain_experimental==0.0.39',
    'langsmith==0.0.63',
    'langchainhub==0.1.13',
    'langserve==0.0.26',
    # Jupyter Notebook
    'ipykernel',
    'jupyterlab',
    # Vectorstores
    'qdrant-client',
    # Extensions
    'lark',
    'html2text',
    'rank_bm25',
    'duckduckgo-search',
]

setuptools.setup(
    name="langchain_setup",
    version="0.0.10.dev",
    author="Richard Wang",
    author_email="richardyy1188@gmail.com",
    description="Some customized code for using langchain.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache 2.0',
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires='>=3',
    keywords='datasets machine learning datasets metrics fastai huggingface',
    install_requires=REQUIRED_PKGS,
    extras_require={'tutorial': TUTORIAL_REQUIRED_PKGS},
)
