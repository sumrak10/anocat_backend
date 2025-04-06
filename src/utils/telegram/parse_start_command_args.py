from typing import Any


def parse_start_command_args(message_text: str) -> tuple[str | None, str | None]:
    args_str_ = message_text.split(' ')
    if len(args_str_) > 1:
        args_str_ = args_str_[1]
    else:
        return None, None
    return args_str_.split('__')
