"""@file main_gui.py
@brief Ponto de entrada da Interface Gráfica (GUI) do sistema do RU.
"""

from interface_ru import TelaSistemaRU


def main() -> None:
    """@brief Instancia a janela principal e inicia o laço de eventos do Tkinter."""
    aplicacao = TelaSistemaRU()
    aplicacao.mainloop()


if __name__ == "__main__":
    main()