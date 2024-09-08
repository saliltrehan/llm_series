from typing import Any, Dict


from langchain_community.llms.openai import BaseOpenAI
from langchain_community.utils.openai import is_openai_v1


class CustomOpenAI(BaseOpenAI):
    """Custom OpenAI-compatible API client"""

    @classmethod
    def is_lc_serializable(cls) -> bool:
        return False

    @property
    def _invocation_params(self) -> Dict[str, Any]:
        """Get the parameters used to invoke the model."""

        params: Dict[str, Any] = {
            "model": self.model_name,
            **self._default_params,
            "logit_bias": None,
        }
        if not is_openai_v1():
            params.update(
                {
                    "api_key": self.openai_api_key,
                    "api_base": self.openai_api_base,
                }
            )

        return params

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "custom-openai"