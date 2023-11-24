# ================================================
# Environment variables
# ================================================
import logging, os
from pathlib import Path
from dotenv import load_dotenv


def load_environment_variables(env_path=None):
    if env_path is None:
        env_paths = [
            Path("~/.cache/.env").expanduser(),
            Path(__file__).parent / ".env",
        ]
        _env_paths = [p for p in env_paths if p.exists()]
        assert (
            len(_env_paths) >= 1
        ), f"Failed at finding `.env` at any of the following locations: {env_paths}"
        env_path = _env_paths[0]
    assert load_dotenv(
        env_path
    ), f"Failed at loading dot environment file `{env_path}`."
    logging.info(f"Environment file {env_path} is loaded.")


load_environment_variables()

# ================================================
# Disabling verification warnings
# ================================================
import warnings
from urllib3.exceptions import InsecureRequestWarning
from requests import Session


def disable_ssl_verification():
    old_init = Session.__init__

    def new_init(self):
        old_init(self)
        self.verify = False

    Session.__init__ = new_init

    # Diabling SSL verification trigger InsecureRequestWarning for every request, which is annoying.
    warnings.filterwarnings(action="ignore", category=InsecureRequestWarning)


disable_ssl_verification()


# ================================================
# A handy context manager for upload only selected runs to LangSmith
# ================================================
import langchain
from langchain.callbacks.manager import tracing_v2_enabled


class tracing_v2_enabled_if_api_key_set:
    """
    A wrapper for users without Langhcain API Key no need to modify the tutorial code.
    Note that the toggling of enable/disable tracing is handled by `tracing_v2_enabled`, so we don't need to cope with `LANGCHAIN_TRACING_V2`.
    """
    def __init__(self, project_name: None | str = None, client=None):
        if os.environ.get("LANGCHAIN_API_KEY", ""):
            self.context_manager = tracing_v2_enabled(
                project_name=project_name, client=client
            )
            
    def __enter__(self):
        if hasattr(self, "context_manager"):
            self.cb = self.context_manager.__enter__()
            return self.cb

    def __exit__(self, type, value, traceback):
        if hasattr(self, "context_manager"):
            print(f"[LangSmith URL]: {self.cb.get_run_url()}")
            self.context_manager.__exit__(type, value, traceback)


# ================================================
# Automatically decide whether to use Azure API and the default model/deployment name
# ================================================
from langchain.chat_models import ChatOpenAI as _ChatOpenAI, AzureChatOpenAI
from langchain.llms import OpenAI as _OpenAI, AzureOpenAI
from functools import partial

if os.environ.get("OPENAI_API_TYPE", None) == "azure":
    OpenAI = partial(
        AzureOpenAI, deployment_name=os.environ["DEFAULT_AZURE_OPENAI_LLM_DEPLOYMENT"]
    )
    ChatOpenAI = partial(
        AzureChatOpenAI,
        deployment_name=os.environ["DEFAULT_AZURE_OPENAI_CHAT_DEPLOYMENT"],
    )
else:
    OpenAI = partial(_OpenAI, model_name=os.environ["DEFAULT_OPENAI_LLM_MODEL"])
    ChatOpenAI = partial(
        _ChatOpenAI, model_name=os.environ["DEFAULT_OPENAI_CHAT_MODEL"]
    )

# ================================================
# Pretty print documents
# ================================================
from pprint import pprint, pformat
from textwrap import dedent
from langchain.schema import Document


def pprint_document(document: Document = None, document_id=None, return_string=False):
    displayed_text = ""
    if document_id:
        displayed_text += f"Document {document_id}:\n\n"
    displayed_text += f"{document.page_content}\n\n"
    metadata_text = pformat(document.metadata, indent=1)
    if "\n" in metadata_text:
        displayed_text += f"Metadata:\n{metadata_text}"
    else:
        displayed_text += f"Metadata:{metadata_text}"

    if return_string:
        return displayed_text
    else:
        print(displayed_text)


def pprint_documents(documents, document_ids=None):
    if not document_ids:
        document_ids = [i + 1 for i in range(len(documents))]

    displayed_texts = []
    for document_id, document in zip(document_ids, documents):
        displayed_text = pprint_document(
            document_id=document_id, document=document, return_string=True
        )
        displayed_texts.append(displayed_text)
    print(f"\n{'-' * 100}\n".join(displayed_texts))


# ================================================
# Pretty print
# ================================================

from textwrap import fill


def wrap_print(string: str, width=100):
    print(fill(string, width=width, replace_whitespace=False))
