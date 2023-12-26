import re
import os


def get_env_variable(variable: str) -> str:
    var = os.environ.get(variable, '')
    return var


def string_to_list(env_variable: str) -> list[str]:
    var = get_env_variable(env_variable)

    list_of_strings = []

    for s in var.split():
        txt = re.sub(r"[,\('\)\" ]", '', s)
        list_of_strings.append(txt)

    return list_of_strings
