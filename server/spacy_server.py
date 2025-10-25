try:
    # pygls >= 1.3 exposes LanguageServer under pygls.lsp.server
    from pygls.lsp.server import LanguageServer
except ImportError:  # pragma: no cover - fallback for older pygls
    from pygls.server import LanguageServer

from thinc.api import Config
from typing import Optional


class SpacyLanguageServer(LanguageServer):
    """
    The language server is responsible for receiving and sending messages over the Language Server Protocol
    which is based on the Json RPC protocol.
    DOCS: https://pygls.readthedocs.io/en/latest/pages/advanced_usage.html#language-server
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.config: Optional[Config] = None
        self.doc_uri: str = None
