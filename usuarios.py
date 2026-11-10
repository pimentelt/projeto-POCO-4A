"""@file usuarios.py
@brief Define os usuários do RU e suas carteiras digitais.
@details Contém a classe abstrata Usuario e os perfis Aluno, Servidor e Externo.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pedidos import Pedido


@dataclass
class CarteiraDigital:
    """@brief Representa a carteira digital de um usuário.

    @details A carteira é criada junto com o usuário e mantém seu saldo em memória.
    @param saldo Saldo inicial da carteira, em reais.
    """

    saldo: float = 0.0

    def depositar(self, valor: float) -> None:
        """@brief Adiciona um valor ao saldo.

        @param valor Quantia a depositar, em reais.
        @throws ValueError Se o valor não for maior que zero.
        """
        if valor <= 0:
            raise ValueError("O depósito deve ser maior que zero.")
        self.saldo += valor

    def debitar(self, valor: float) -> None:
        """@brief Retira um valor do saldo.

        @param valor Quantia a debitar, em reais.
        @throws ValueError Se o valor não for positivo ou superar o saldo disponível.
        """
        if valor <= 0:
            raise ValueError("O débito deve ser maior que zero.")
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente.")
        self.saldo -= valor


class Usuario(ABC):
    """@brief Classe abstrata que representa um usuário do RU.

    @details Cada usuário possui uma carteira digital e uma lista de pedidos associados.
    As subclasses devem implementar gerar_codigo_identificacao().
    @param nome Nome completo do usuário.
    @param email Endereço de e-mail do usuário.
    @param identificador RA, ID funcional ou código de cadastro.
    """

    def __init__(self, nome: str, email: str, identificador: str) -> None:
        self.nome = nome
        self.email = email
        self.identificador = identificador
        self.carteira = CarteiraDigital()
        self.pedidos: list[Pedido] = []

    @abstractmethod
    def gerar_codigo_identificacao(self) -> str:
        """@brief Gera o código de identificação do usuário.

        @return Código de identificação formatado conforme o perfil.
        """


class Aluno(Usuario):
    """@brief Usuário do RU identificado pelo Registro Acadêmico (RA).

    @param nome Nome completo do aluno.
    @param email Endereço de e-mail do aluno.
    @param ra Registro Acadêmico do aluno.
    """

    def __init__(self, nome: str, email: str, ra: str) -> None:
        super().__init__(nome, email, ra)
        self.ra = ra

    def gerar_codigo_identificacao(self) -> str:
        """@brief Gera a identificação do aluno.
        @return Código no formato ALUNO-<RA>.
        """
        return f"ALUNO-{self.ra}"


class Servidor(Usuario):
    """@brief Usuário do RU identificado por seu ID funcional.

    @param nome Nome completo do servidor.
    @param email Endereço de e-mail do servidor.
    @param id_servidor Identificador funcional do servidor.
    """

    def __init__(self, nome: str, email: str, id_servidor: str) -> None:
        super().__init__(nome, email, id_servidor)
        self.id_servidor = id_servidor

    def gerar_codigo_identificacao(self) -> str:
        """@brief Gera a identificação do servidor.
        @return Código no formato SERVIDOR-<ID>.
        """
        return f"SERVIDOR-{self.id_servidor}"


class Externo(Usuario):
    """@brief Usuário externo identificado pelo código de cadastro.
    @details Recebe nome, e-mail e identificador no construtor herdado de Usuario.
    """

    def gerar_codigo_identificacao(self) -> str:
        """@brief Gera a identificação do usuário externo.
        @return Código no formato EXTERNO-<identificador>.
        """
        return f"EXTERNO-{self.identificador}"
