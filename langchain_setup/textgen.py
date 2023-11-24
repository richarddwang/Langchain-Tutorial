"""Wrapper around text-generation-webui."""
import logging, os, requests, socket
from typing import Any, Dict, List, Optional

from langchain.pydantic_v1 import Field, root_validator
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM

logger = logging.getLogger(__name__)

DEFAULT_HOST_NAME = "localhost"
DEFAULT_API_BLOCKING_PORT = 5000
DEFAULT_API_STREAMING_PORT = 5005


class TextGen(LLM):
    """Wrapper around the text-generation-webui model.

    To use, you should have the text-generation-webui installed, a model loaded,
    and --api added as a command-line option.

    Suggested installation, use one-click installer for your OS:
    https://github.com/oobabooga/text-generation-webui#one-click-installers

    Paremeters below taken from text-generation-webui api example:
    https://github.com/oobabooga/text-generation-webui/blob/main/api-examples/api-example.py

    Example:
        .. code-block:: python
            # user@local_host:~/text-generation-webui$ python server.py --api

            from langchain.llms import TextGen
            llm = TextGen() # blocking api: http://localhost:5000, streaming api: http://localhost:5005

        .. code-block:: python
            # user@remote_host:~/text-generation-webui$ python server.py --api --api-blocking-port 6001 --api-streaming-port 6002

            from langchain.llms import TextGen
            llm = TextGen(
                http_addr_or_http_name_or_ssh_name_of_remote_host,
                api_blocking_port=6001,
                api_streaming_port=6002,
            ) # automatically setup SSH tunnels for you ❤️
    """

    # Connection

    host_name_or_address: Optional[str] = None
    """HTTP host name or HTTP host address or SSH host name. If it is not set, use environment variable `textgen_host_name_or_address`."""
    api_blocking_port: Optional[int] = None
    """Host port of blocking api. If it is not set, use environment variable `textgen_api_blocking_port`."""
    api_streaming_port: Optional[int] = None
    """Host port of streaming api. If it is not set, use environment variable `textgen_api_streaming_port`."""

    streaming: bool = False

    # Length

    max_new_tokens: Optional[int] = 250
    """The maximum number of tokens to generate."""

    min_new_tokens: Optional[int] = 0
    """The minimum numbers of tokens to generate, ignoring the number of tokens in the prompt."""

    min_length: Optional[int] = 0
    """The minimum length of the sequence to be generated. Corresponds to the length of the input prompt + min_new_tokens. Its effect is overridden by min_new_tokens, if also set."""

    truncation_length: Optional[int] = 99999
    """Truncate the prompt up to this length. The leftmost tokens are removed if
    the prompt exceeds this length. Most models require this to be at most 2048."""

    # Randomness

    do_sample: bool = False
    """Do sample"""

    seed: int = -1
    """Seed (-1 for random)"""

    # Generation strategy

    num_beams: Optional[int] = 1
    """Number of beams"""

    length_penalty: Optional[float] = 1
    """Length Penalty"""

    early_stopping: bool = False
    """Early stopping"""

    penalty_alpha: Optional[float] = 0
    """Penalty Alpha"""

    # Output logits manipulation

    temperature: Optional[float] = 0.7
    """Primary factor to control randomness of outputs. 0 = deterministic
    (only the most likely token is used). Higher value = more randomness."""

    top_k: Optional[float] = 40
    """Similar to top_p, but select instead only the top_k most likely tokens.
    Higher value = higher range of possible random results."""

    top_p: Optional[float] = 0.1
    """If not set to 1, select tokens with probabilities adding up to less than this
    number. Higher value = higher range of possible random results."""

    typical_p: Optional[float] = 1
    """If not set to 1, select only tokens that are at least this much more likely to
    appear than random tokens, given the prior text."""

    epsilon_cutoff: Optional[float] = 0  # In units of 1e-4
    """Epsilon cutoff"""

    eta_cutoff: Optional[float] = 0  # In units of 1e-4
    """ETA cutoff"""

    repetition_penalty: Optional[float] = 1.18
    """Exponential penalty factor for repeating prior tokens. 1 means no penalty,
    higher value = less repetition, lower value = more repetition."""

    no_repeat_ngram_size: Optional[int] = 0
    """If not set to 0, specifies the length of token sets that are completely blocked
    from repeating at all. Higher values = blocks larger phrases,
    lower values = blocks words or letters from repeating.
    Only 0 or high values are a good idea in most cases."""

    # Special toknes

    add_bos_token: bool = True
    """Add the bos_token to the beginning of prompts.
    Disabling this can make the replies more creative."""

    ban_eos_token: bool = False
    """Ban the eos_token. Forces the model to never end the generation prematurely."""

    skip_special_tokens: bool = True
    """Skip special tokens. Some specific models need this unset."""

    stopping_strings: Optional[List[str]] = Field(default_factory=list)
    """A list of strings to stop generation when encountered."""

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        # Check values
        if values["temperature"] == 0:
            values["temperature"] = 1e-9  # temperature can not be set to 0
        values["host_name_or_address"] = values.get(
            "host_name_or_address"
        ) or os.environ.get("textgen_host_name_or_address", DEFAULT_HOST_NAME)
        values["api_blocking_port"] = values.get("api_blocking_port") or int(
            os.environ.get("textgen_api_blocking_port", DEFAULT_API_BLOCKING_PORT)
        )
        values["api_streaming_port"] = values.get("api_streaming_port") or int(
            os.environ.get("textgen_api_streaming_port", DEFAULT_API_STREAMING_PORT)
        )

        # It seems that gradio server can't properly handle proxy (?)
        os.environ["no_proxy"] = "localhost, 127.0.0.1"

        # HTTP address
        try:
            http_addr = socket.gethostbyname(values["host_name_or_address"])
            via_ssh = http_addr != "127.0.0.1" or http_addr != get_curreent_ip()
        except:
            via_ssh = True

        # Check whether direct connection is available before setting SSH Tunnel ?
        via_ssh = False

        # Create SSH tunnel if needed
        if via_ssh:
            from sshconf import read_ssh_config_file

            ssh_cfg = read_ssh_config_file(os.path.expanduser("~/.ssh/config"))
            ssh_hostnames = [
                host
                for host in ssh_cfg.hosts()
                if host == values["host_name_or_address"]
                or socket.gethostbyname(ssh_cfg.host(host)["hostname"])
                == values["host_name_or_address"]
            ]
            if len(ssh_hostnames) == 0:
                raise ValueError(
                    f"Did not find any SSH host name corresponds to {values['host_name_or_address']} in `~/.ssh/config`."
                )
            elif len(ssh_hostnames) > 1:
                raise ValueError(
                    f"Multiple SSH host {ssh_hostnames} correspond to {values['host_name_or_address']} in `~/.ssh/config`."
                )
            ssh_hostname = ssh_hostnames[0]
            api_blocking_tunnel, api_streaming_tunnel = _setup_ssh_tunnels(
                ssh_host_name=ssh_hostname,
                api_blocking_port=values["api_blocking_port"],
                api_streaming_port=values["api_streaming_port"],
            )

            values["host_name_or_address"] = "127.0.0.1"
            values["api_blocking_port"] = api_blocking_tunnel.local_bind_port
            values["api_streaming_port"] = api_streaming_tunnel.local_bind_port

        return values

    @property
    def _default_params(self) -> Dict[str, Any]:
        """Get the default parameters for calling textgen."""
        return {
            "max_new_tokens": self.max_new_tokens,
            "do_sample": self.do_sample,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "typical_p": self.typical_p,
            "epsilon_cutoff": self.epsilon_cutoff,
            "eta_cutoff": self.eta_cutoff,
            "repetition_penalty": self.repetition_penalty,
            "top_k": self.top_k,
            "min_length": self.min_length,
            "min_new_tokens": self.min_new_tokens,
            "no_repeat_ngram_size": self.no_repeat_ngram_size,
            "num_beams": self.num_beams,
            "penalty_alpha": self.penalty_alpha,
            "length_penalty": self.length_penalty,
            "early_stopping": self.early_stopping,
            "seed": self.seed,
            "add_bos_token": self.add_bos_token,
            "truncation_length": self.truncation_length,
            "ban_eos_token": self.ban_eos_token,
            "skip_special_tokens": self.skip_special_tokens,
            "stopping_strings": self.stopping_strings,
        }

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters."""
        return {
            **{
                "host_name_or_address": self.host_name_or_address,
                "api_blocking_port": self.api_blocking_port,
                "api_streaming_port": self.api_streaming_port,
            },
            **self._default_params,
        }

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "textgen"

    def _get_parameters(self, stop: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Performs sanity check, preparing paramaters in format needed by textgen.

        Args:
            stop (Optional[List[str]]): List of stop sequences for textgen.

        Returns:
            Dictionary containing the combined parameters.
        """

        # Raise error if stop sequences are in both input and default params
        # if self.stop and stop is not None:
        if self.stopping_strings and stop is not None:
            raise ValueError("`stop` found in both the input and default params.")

        params = self._default_params

        # then sets it as configured, or default to an empty list:
        params["stop"] = self.stopping_strings or stop or []

        return params

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call the textgen web API and return the output.

        Args:
            prompt: The prompt to use for generation.
            stop: A list of strings to stop generation when encountered.

        Returns:
            The generated text.

        Example:
            .. code-block:: python

                from langchain.llms import TextGen
                llm = TextGen(model_url="http://localhost:5000")
                llm("Write a story about llamas.")
        """
        if self.streaming:
            raise NotImplementedError

        url = f"http://{self.host_name_or_address}:{self.api_blocking_port}/api/v1/generate"
        params = self._get_parameters(stop)
        request = params.copy()
        request["prompt"] = prompt
        response = requests.post(url, json=request)

        if response.status_code == 200:
            result = response.json()["results"][0]["text"]
        else:
            raise ConnectionError(str(response))

        if result == "" and self.model_info()["model_name"] is None:
            raise ValueError("No model is loaded!")

        return result

    def model_info(self):
        result = requests.post(
            f"http://{self.host_name_or_address}:{self.api_blocking_port}/api/v1/model",
            json={"action": "info"},
        ).json()["result"]
        return result


def get_curreent_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def _setup_ssh_tunnels(ssh_host_name, api_blocking_port, api_streaming_port):
    from sshtunnel import SSHTunnelForwarder

    api_blocking_tunnel = SSHTunnelForwarder(
        ssh_address_or_host=ssh_host_name,
        remote_bind_address=("127.0.0.1", api_blocking_port),
    )
    api_blocking_tunnel.start()

    api_streaming_tunnel = SSHTunnelForwarder(
        ssh_address_or_host=ssh_host_name,
        remote_bind_address=("127.0.0.1", api_streaming_port),
    )
    api_streaming_tunnel.start()

    return api_blocking_tunnel, api_streaming_tunnel
