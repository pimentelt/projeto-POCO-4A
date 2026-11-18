"""@file usuarios.py
@brief Define os usuários do RU e suas regras de validação cadastral.
@details Contém a classe abstrata Usuario e os perfis Aluno, Servidor e Externo.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pedidos import Pedido


class Usuario(ABC):
    """@brief Classe abstrata que representa um usuário do RU."""

    def __init__(self, nome: str, email: str, identificador: str) -> None:
        nome_limpo = nome.strip()
        email_limpo = email.strip()
        id_limpo = identificador.strip()

        if not nome_limpo:
            raise ValueError("Informe o nome completo do usuário.")
        if not email_limpo or "@" not in email_limpo:
            raise ValueError("Informe um endereço de e-mail válido.")
        if not id_limpo:
            raise ValueError("Informe o RA, ID funcional ou código de identificação.")

        self._nome = nome_limpo
        self._email = email_limpo
        self._identificador = id_limpo
        self._pedidos: list["Pedido"] = []

    @property
    def nome(self) -> str:
        """@brief Obtém o nome do usuário."""
        return self._nome

    @property
    def email(self) -> str:
        """@brief Obtém o e-mail do usuário."""
        return self._email

    @property
    def identificador(self) -> str:
        """@brief Obtém o identificador base do usuário."""
        return self._identificador

    @property
    def pedidos(self) -> list["Pedido"]:
        """@brief Retorna uma cópia da lista de pedidos do usuário."""
        return list(self._pedidos)

    def adicionar_pedido(self, pedido: "Pedido") -> None:
        """@brief Associa um novo pedido ao histórico do usuário."""
        self._pedidos.append(pedido)

    @abstractmethod
    def gerar_codigo_identificacao(self) -> str:
        """@brief Gera o código de identificação formatado do usuário."""
        pass


class Aluno(Usuario):
    """@brief Usuário do RU identificado pelo Registro Acadêmico (RA)."""

    def __init__(self, nome: str, email: str, ra: str) -> None:
        ra_limpo = ra.strip()
        if not ra_limpo.isdigit() or len(ra_limpo) != 7:
            raise ValueError("O RA do aluno deve conter exatamente 7 dígitos numéricos.")
        super().__init__(nome, email, ra_limpo)
        self._ra = ra_limpo

    @property
    def ra(self) -> str:
        """@brief Obtém o Registro Acadêmico do aluno."""
        return self._ra

    def gerar_codigo_identificacao(self) -> str:
        """@brief Gera a identificação no formato ALUNO-<RA>."""
        return f"ALUNO-{self._ra}"


class Servidor(Usuario):
    """@brief Usuário do RU identificado por seu ID funcional."""

    def __init__(self, nome: str, email: str, id_servidor: str) -> None:
        id_limpo = id_servidor.strip()
        if not id_limpo.isdigit() or len(id_limpo) != 8:
            raise ValueError("O ID do servidor deve conter exatamente 8 dígitos numéricos.")
        super().__init__(nome, email, id_limpo)
        self._id_servidor = id_limpo

    @property
    def id_servidor(self) -> str:
        """@brief Obtém o ID funcional do servidor."""
        return self._id_servidor

    def gerar_codigo_identificacao(self) -> str:
        """@brief Gera a identificação no formato SERVIDOR-<ID>."""
        return f"SERVIDOR-{self._id_servidor}"


class Externo(Usuario):
    """@brief Usuário externo identificado pelo código de cadastro."""

    def gerar_codigo_identificacao(self) -> str:
        """@brief Gera a identificação no formato EXTERNO-<identificador>."""
        return f"EXTERNO-{self._identificador}"