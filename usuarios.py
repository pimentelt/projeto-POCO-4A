"""
@file usuarios.py
@brief Define os usuários do RU.
@details Contém a classe abstrata Usuario e os perfis Aluno, Servidor e Externo.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pedidos import Pedido


class Usuario(ABC):
    """
    @brief Classe abstrata que representa um usuário do RU.
    @details Mantém os dados cadastrais e a lista de pedidos associados.
    @param nome Nome completo do usuário.
    @param email Endereço de e-mail do usuário.
    @param identificador RA, ID funcional ou código de cadastro.
    """

    def __init__(self, nome: str, email: str, identificador: str) -> None:
        self._nome = nome
        self._email = email
        self._identificador = identificador
        self._pedidos: list["Pedido"] = []

    @property
    def nome(self) -> str:
        """
        @brief Obtém o nome do usuário.
        @return Nome completo do usuário.
        """
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
        """
        @brief Associa um novo pedido ao histórico do usuário.
        @param pedido Instância do pedido criado.
        """
        self._pedidos.append(pedido)

    @abstractmethod
    def gerar_codigo_identificacao(self) -> str:
        """
        @brief Gera o código de identificação formatado do usuário.
        @return Código de identificação formatado conforme a subclasse.
        """
        pass


class Aluno(Usuario):
    """
    @brief Usuário do RU identificado pelo Registro Acadêmico (RA).
    """

    def __init__(self, nome: str, email: str, ra: str) -> None:
        if not ra.isdigit() or len(ra) != 7:
            raise ValueError("O RA do aluno deve conter exatamente 7 dígitos numéricos.")
        super().__init__(nome, email, ra)
        self._ra = ra

    @property
    def ra(self) -> str:
        """
        @brief Obtém o Registro Acadêmico do aluno.
        @return RA do aluno.
        """
        return self._ra

    def gerar_codigo_identificacao(self) -> str:
        """
        @brief Gera a identificação do aluno.
        @return Código no formato ALUNO-<RA>.
        """
        return f"ALUNO-{self._ra}"


class Servidor(Usuario):
    """
    @brief Usuário do RU identificado por seu ID funcional.
    """

    def __init__(self, nome: str, email: str, id_servidor: str) -> None:
        if not id_servidor.isdigit() or len(id_servidor) != 8:
            raise ValueError("O ID do servidor deve conter exatamente 8 dígitos numéricos.")
        super().__init__(nome, email, id_servidor)
        self._id_servidor = id_servidor

    @property
    def id_servidor(self) -> str:
        """
        @brief Obtém o ID funcional do servidor.
        @return ID funcional do servidor.
        """
        return self._id_servidor

    def gerar_codigo_identificacao(self) -> str:
        """
        @brief Gera a identificação do servidor.
        @return Código no formato SERVIDOR-<ID>.
        """
        return f"SERVIDOR-{self._id_servidor}"


class Externo(Usuario):
    """
    @brief Usuário externo identificado pelo código de cadastro.
    """

    def gerar_codigo_identificacao(self) -> str:
        """
        @brief Gera a identificação do usuário externo.
        @return Código no formato EXTERNO-<identificador>.
        """
        return f"EXTERNO-{self._identificador}"