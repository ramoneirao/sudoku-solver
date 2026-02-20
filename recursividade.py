"""
recursividade.py
Resolve um Sudoku importando a classe Sudoku
Salva logs e estatísticas na pasta /resultados
"""

import time
import copy
import os
from datetime import datetime
from sudoku import Sudoku


class RecursiveSudokuSolver:
    def __init__(self, sudoku_game):
        self.game = sudoku_game
        self.board = copy.deepcopy(sudoku_game.board)
        self.size = 9
        self.steps = 0
        self.recursion_calls = 0
        self.max_depth = 0

        # Criar pasta resultados se não existir
        self.results_dir = "resultados"
        os.makedirs(self.results_dir, exist_ok=True)

        self.log_path = os.path.join(self.results_dir, "iteracoes_recursividade.txt")
        self.stats_path = os.path.join(self.results_dir, "estatisticas.txt")

        # Limpa arquivo de log ao iniciar
        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write("=== LOG DE RECURSIVIDADE - SUDOKU ===\n\n")

    def log(self, message):
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(message + "\n")

    def is_valid(self, row, col, num):
        return self.game.is_valid(self.board, row, col, num)

    def find_empty(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def solve(self, depth=0):
        self.recursion_calls += 1
        self.max_depth = max(self.max_depth, depth)

        empty = self.find_empty()

        if not empty:
            self.log(" " * depth + "✔ Sudoku resolvido!")
            return True

        row, col = empty

        for num in range(1, 10):
            self.log(" " * depth + f"Testando {num} em ({row},{col})")

            if self.is_valid(row, col, num):
                self.log(" " * depth + f"✔ {num} válido -> descendo recursão")
                self.board[row][col] = num
                self.steps += 1

                if self.solve(depth + 2):
                    return True

                self.log(" " * depth + f"↩ Backtracking removendo {num} de ({row},{col})")
                self.board[row][col] = 0

        self.log(" " * depth + f"✖ Nenhum número válido em ({row},{col})")
        return False

    def save_statistics(self, execution_time):
        with open(self.stats_path, "w", encoding="utf-8") as f:
            f.write("=== ESTATÍSTICAS DA EXECUÇÃO ===\n\n")
            f.write(f"Data/Hora: {datetime.now()}\n")
            f.write(f"Dificuldade: {self.game.difficulty}\n")
            f.write(f"Chamadas recursivas: {self.recursion_calls}\n")
            f.write(f"Passos realizados: {self.steps}\n")
            f.write(f"Profundidade máxima atingida: {self.max_depth}\n")
            f.write(f"Tempo de execução (segundos): {execution_time:.6f}\n")


def main():
    print("Gerando Sudoku...")
    game = Sudoku("hard")

    solver = RecursiveSudokuSolver(game)

    print("Resolvendo... (arquivos serão salvos na pasta /resultados)")
    start_time = time.time()

    solved = solver.solve()

    end_time = time.time()
    execution_time = end_time - start_time

    solver.save_statistics(execution_time)

    if solved:
        print("Sudoku resolvido com sucesso!")
    else:
        print("Não foi possível resolver.")

    print("\nArquivos gerados:")
    print(" - resultados/iteracoes_recursividade.txt")
    print(" - resultados/estatisticas.txt")


if __name__ == "__main__":
    main()