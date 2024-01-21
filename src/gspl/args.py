from argparse import ArgumentParser
from typing import Any, Final

__all__ = ["ArgumentParser", "StaticArgumentParser"]


class StaticArgumentParser:
    __argparser: dict[str, ArgumentParser] = {}
    __namespace: str

    def __init__(self, namespace: str = "core", /, **kwargs: Any) -> None:
        self.__namespace = namespace
        self.__load(namespace, **kwargs)
        self.set_defaults()

    @staticmethod
    def __load(namespace: str, /, **kwargs: Any) -> None:
        if namespace not in StaticArgumentParser.__argparser:
            StaticArgumentParser.__argparser[namespace] = ArgumentParser(**kwargs)

    @property
    def argparser(self) -> ArgumentParser:
        return self.__nsget()

    @property
    def namespace(self) -> str:
        return self.__namespace

    def __nsget(self, namespace: str | None = None) -> ArgumentParser:
        return StaticArgumentParser.__argparser[namespace or self.namespace]

    def set_defaults(self) -> None:
        """Define argumentos default para todos os parsers"""
        return self

    def add_argument(self, *args: Any, **kwargs: Any) -> None:
        """Adiciona argumento a todos os parsers"""
        for parser in StaticArgumentParser.__argparser.values():
            parser.add_argument(*args, **kwargs)

    def parse_args(self, *args: Any, **kwargs: Any) -> Any:
        """Faz o parsing dos argumentos"""
        return self.argparser.parse_args(*args, **kwargs)
