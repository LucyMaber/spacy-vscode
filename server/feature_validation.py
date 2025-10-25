"""Script containing all logic for validation functionality"""
from lsprotocol.types import MessageType

from thinc.api import Config
from typing import Optional
from .spacy_server import SpacyLanguageServer
from .pygls_compat import window_log_message, window_show_message


def validate_config(
    server: SpacyLanguageServer, cfg: Optional[str]
) -> Optional[Config]:
    """Validate .cfg files and return their Config object"""
    try:
        config = Config().from_str(cfg)  # type: ignore[arg-type]
        window_log_message(server, "Validation Successful")
        return config
    except Exception as e:
        window_log_message(server, "Validation Unsuccessful", MessageType.Warning)
        window_show_message(
            server, "Warning: Config not valid ", MessageType.Warning
        )
        return None
