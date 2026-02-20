import sys
import time
import os
import csv
import matplotlib.pyplot as plt
from sudoku import Sudoku
from recursividade import RecursiveSudokuSolver
import statistics


# =============================
# CONTADOR DE LINHAS EXECUTADAS
# =============================
class LineCounter:
    def __init__(self):
        self.lines = 0

    def tracer(self, frame, event, arg):
        if event == "line":
            self.lines += 1
        return self.tracer


# =============================
# EXECUTA TESTES
# =============================
def run_experiment(difficulty, runs=5):
    results = []

    for i in range(runs):
        print(f"Executando {difficulty} - Teste {i+1}")

        game = Sudoku(difficulty)
        solver = RecursiveSudokuSolver(game)

        counter = LineCounter()

        sys.settrace(counter.tracer)
        start_time = time.time()

        solver.solve()

        end_time = time.time()
        sys.settrace(None)

        results.append({
            "lines": counter.lines,
            "time": end_time - start_time,
            "recursions": solver.recursion_calls
        })

    return results


# =============================
# SALVAR RESULTADOS EM CSV
# =============================
def save_csv(all_results):
    os.makedirs("resultados", exist_ok=True)
    path = os.path.join("resultados", "dados_experimento.csv")

    with open(path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Dificuldade", "Execucao", "Linhas", "Tempo", "Chamadas_Recursivas"])

        for diff, results in all_results.items():
            for i, r in enumerate(results):
                writer.writerow([diff, i+1, r["lines"], r["time"], r["recursions"]])

    print(f"CSV salvo em {path}")


# =============================
# GRÁFICOS INDIVIDUAIS
# =============================
def plot_individual(all_results):
    os.makedirs("images", exist_ok=True)

    for diff, results in all_results.items():
        lines = [r["lines"] for r in results]

        plt.figure()
        plt.plot(range(1, len(lines)+1), lines)
        plt.xlabel("Execução")
        plt.ylabel("Linhas Executadas")
        plt.title(f"Desempenho - {diff}")
        plt.grid()
        path = f"images/{diff}.png"
        plt.savefig(path)
        plt.close()

        print(f"Gráfico salvo em {path}")


# =============================
# GRÁFICO COMPARATIVO
# =============================
def plot_comparison(all_results):
    os.makedirs("images", exist_ok=True)

    difficulties = ["easy", "medium", "hard"]
    avg_lines = []

    for diff in difficulties:
        values = [r["lines"] for r in all_results[diff]]
        avg_lines.append(sum(values) / len(values))

    plt.figure()
    plt.plot(difficulties, avg_lines)
    plt.xlabel("Dificuldade")
    plt.grid()
    plt.ylabel("Média de Linhas Executadas")
    plt.title("Comparação de Desempenho")
    path = "images/comparacao.png"
    plt.savefig(path)
    plt.close()

    print(f"Gráfico comparativo salvo em {path}")

def save_averages(all_results):
    os.makedirs("resultados", exist_ok=True)
    path = os.path.join("resultados", "estatisticas_medias.csv")

    with open(path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Dificuldade",
            "Media_Linhas",
            "Desvio_Padrao_Linhas",
            "Media_Tempo",
            "Media_Chamadas"
        ])

        for diff, results in all_results.items():
            lines = [r["lines"] for r in results]
            times = [r["time"] for r in results]
            recs = [r["recursions"] for r in results]

            writer.writerow([
                diff,
                statistics.mean(lines),
                statistics.stdev(lines),
                statistics.mean(times),
                statistics.mean(recs)
            ])

    print(f"Estatísticas salvas em {path}")


# =============================
# MAIN
# =============================
def main():
    all_results = {}

    for difficulty in ["easy", "medium", "hard"]:
        all_results[difficulty] = run_experiment(difficulty, runs=5)

    save_csv(all_results)
    plot_individual(all_results)
    plot_comparison(all_results)
    save_averages(all_results)

    print("\nExperimento finalizado!")


if __name__ == "__main__":
    main()