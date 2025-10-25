"""Compatibility helpers bridging pygls v1 and v2 API differences."""

from typing import Any, Callable, Optional

from lsprotocol import types


def _callable_attr(obj: Any, name: str) -> Optional[Callable[..., Any]]:
    attr = getattr(obj, name, None)
    return attr if callable(attr) else None


def get_text_document(server: Any, uri: str) -> Any:
    workspace = getattr(server, "workspace", None)
    if workspace is None:
        return None

    for getter_name in ("get_document", "get_text_document"):
        getter = _callable_attr(workspace, getter_name)
        if getter is not None:
            try:
                return getter(uri)
            except AttributeError:
                # Some pygls versions raise if method absent; continue fallback.
                pass

    for collection_name in ("text_documents", "documents"):
        documents = getattr(workspace, collection_name, None)
        if isinstance(documents, dict):
            return documents.get(uri)

    return None


def window_show_message(
    server: Any,
    message: str,
    message_type: types.MessageType = types.MessageType.Info,
) -> None:
    window_method = _callable_attr(server, "window_show_message")
    if window_method is not None:
        window_method(types.ShowMessageParams(type=message_type, message=message))
        return

    legacy_method = _callable_attr(server, "show_message")
    if legacy_method is not None:
        try:
            legacy_method(message, message_type)
        except TypeError:
            legacy_method(message)
        return

    raise AttributeError("LanguageServer does not expose a show message method.")


def window_log_message(
    server: Any,
    message: str,
    message_type: types.MessageType = types.MessageType.Info,
) -> None:
    window_method = _callable_attr(server, "window_log_message")
    if window_method is not None:
        window_method(types.LogMessageParams(type=message_type, message=message))
        return

    legacy_method = _callable_attr(server, "show_message_log")
    if legacy_method is not None:
        try:
            legacy_method(message, message_type)
        except TypeError:
            legacy_method(message)
        return

    raise AttributeError("LanguageServer does not expose a log message method.")
