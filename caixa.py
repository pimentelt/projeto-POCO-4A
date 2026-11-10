"""@file caixa.py
@brief Implementa as operações presenciais do caixa do RU.
"""

from pedidos import MetodoPagamento, Pedido


class CaixaRU:
    """@brief Representa o caixa presencial do Restaurante Universitário."""

    def validar_codigo_retirada(self, pedido: Pedido, codigo: str) -> bool:
        """@brief Confere se o código corresponde a um pedido pago.

        @param pedido Pedido cuja retirada será validada.
        @param codigo Código informado no caixa.
        @return True se o código for válido e o pedido aguardar retirada; caso contrário, False.
        """
        return (
            pedido.status == "aguardando_retirada"
            and pedido.codigo_retirada == codigo.strip().upper()
        )

    def receber_pagamento_especie(self, pedido: Pedido, valor: float) -> float:
        """@brief Registra pagamento em dinheiro e calcula o troco.

        @param pedido Pedido que será pago.
        @param valor Valor recebido em reais.
        @return Troco devido em reais.
        @throws ValueError Se o pedido não aguardar pagamento ou o valor for insuficiente.
        """
        if pedido.status != "aguardando_pagamento":
            raise ValueError("Este pedido não está aguardando pagamento.")
        if valor < pedido.valor_total:
            raise ValueError("O valor recebido é menor que o total do pedido.")
        pedido.registrar_pagamento(MetodoPagamento.DINHEIRO_ESPECIE)
        return round(valor - pedido.valor_total, 2)

    def confirmar_retirada(self, pedido: Pedido, codigo: str) -> None:
        """@brief Confirma a retirada de um pedido pago.

        @param pedido Pedido a ser entregue.
        @param codigo Código apresentado pelo usuário.
        @throws ValueError Se o código for inválido ou o pedido ainda não estiver pago.
        """
        if not self.validar_codigo_retirada(pedido, codigo):
            raise ValueError("Código inválido ou pedido ainda não pago.")
        pedido.status = "retirado"
