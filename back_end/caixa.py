"""@file caixa.py
@brief Implementa as operações presenciais e validações financeiras do caixa do RU.
"""

from pedidos import MetodoPagamento, Pedido


class CaixaRU:
    """@brief Representa o caixa presencial do Restaurante Universitário."""

    def validar_codigo_retirada(self, pedido: Pedido, codigo: str) -> bool:
        """@brief Confere se o código vinculado ao usuário corresponde a um pedido pago."""
        return (
            pedido.status == "aguardando_retirada"
            and pedido.codigo_retirada == codigo.strip().upper()
        )

    def registrar_pagamento_pedido(
        self, pedido: Pedido, metodo: MetodoPagamento, valor: float
    ) -> float:
        """@brief Valida o valor recebido e registra o pagamento do pedido."""
        if pedido.status != "aguardando_pagamento":
            raise ValueError("Este pedido não está aguardando pagamento.")
        if not pedido.itens:
            raise ValueError("Adicione pelo menos um item ao pedido antes de pagar.")
        if round(valor, 2) < pedido.valor_total:
            raise ValueError(
                f"Valor insuficiente! O total a ser pago é R$ {pedido.valor_total:.2f}."
            )
        if metodo != MetodoPagamento.DINHEIRO_ESPECIE and round(valor, 2) > pedido.valor_total:
            raise ValueError(
                f"Para {metodo.value}, o valor pago deve ser exatamente R$ {pedido.valor_total:.2f}."
            )

        pedido.registrar_pagamento(metodo)
        if metodo == MetodoPagamento.DINHEIRO_ESPECIE:
            return round(valor - pedido.valor_total, 2)
        return 0.0

    def receber_pagamento_especie(self, pedido: Pedido, valor: float) -> float:
        """@brief Registra pagamento em dinheiro e calcula o troco."""
        return self.registrar_pagamento_pedido(
            pedido, MetodoPagamento.DINHEIRO_ESPECIE, valor
        )

    def confirmar_retirada(self, pedido: Pedido, codigo: str) -> None:
        """@brief Confirma a retirada de um pedido pago."""
        if not self.validar_codigo_retirada(pedido, codigo):
            raise ValueError("Código inválido ou pedido ainda não pago.")
        pedido.status = "retirado"