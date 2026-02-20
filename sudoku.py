import random
import copy


class Sudoku:
    """Classe para criar e jogar sudoku"""
    
    # Códigos de cor ANSI
    GREEN = '\033[92m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    
    def __init__(self, difficulty='medium'):
        """
        Inicializa um novo jogo de Sudoku
        
        Args:
            difficulty (str): Nível de dificuldade - 'easy', 'medium', 'hard'
        """
        self.size = 9
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.solution = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.fixed = [[False for _ in range(self.size)] for _ in range(self.size)]  # Células fixas (originais)
        self.difficulty = difficulty
        self.generate_puzzle()
    
    def is_valid(self, board, row, col, num):
        """
        Verifica se um número pode ser colocado em uma posição
        
        Args:
            board: Tabuleiro atual
            row: Linha
            col: Coluna
            num: Número a verificar
            
        Returns:
            bool: True se o número é válido na posição
        """
        # Verifica linha
        if num in board[row]:
            return False
        
        # Verifica coluna
        if num in [board[i][col] for i in range(self.size)]:
            return False
        
        # Verifica quadrante 3x3
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
        
        return True
    
    def solve(self, board):
        """
        Resolve o sudoku usando backtracking
        
        Args:
            board: Tabuleiro a resolver
            
        Returns:
            bool: True se conseguiu resolver
        """
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            
                            if self.solve(board):
                                return True
                            
                            board[row][col] = 0
                    
                    return False
        return True
    
    def fill_board(self, board):
        """
        Preenche o tabuleiro completamente de forma aleatória
        
        Args:
            board: Tabuleiro a preencher
            
        Returns:
            bool: True se conseguiu preencher
        """
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    
                    for num in numbers:
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            
                            if self.fill_board(board):
                                return True
                            
                            board[row][col] = 0
                    
                    return False
        return True
    
    def remove_numbers(self, board, attempts):
        """
        Remove números do tabuleiro completo para criar o puzzle
        
        Args:
            board: Tabuleiro completo
            attempts: Número de células a tentar remover
        """
        while attempts > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            
            if board[row][col] != 0:
                backup = board[row][col]
                board[row][col] = 0
                
                # Verifica se o puzzle ainda tem solução única
                board_copy = copy.deepcopy(board)
                if not self.has_unique_solution(board_copy):
                    board[row][col] = backup
                
                attempts -= 1
    
    def has_unique_solution(self, board):
        """
        Verifica se o puzzle tem solução única (simplificado)
        
        Args:
            board: Tabuleiro a verificar
            
        Returns:
            bool: True se tem solução
        """
        # Versão simplificada - apenas verifica se é possível resolver
        return self.solve(copy.deepcopy(board))
    
    def generate_puzzle(self):
        """Gera um novo puzzle de Sudoku"""
        # Cria um tabuleiro completo válido
        self.solution = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.fill_board(self.solution)
        
        # Copia a solução para o board
        self.board = copy.deepcopy(self.solution)
        
        # Define quantos números remover baseado na dificuldade
        difficulty_map = {
            'easy': 35,
            'medium': 45,
            'hard': 55
        }
        attempts = difficulty_map.get(self.difficulty, 45)
        
        # Remove números para criar o puzzle
        self.remove_numbers(self.board, attempts)
        
        # Marca as células que não foram removidas como fixas
        for i in range(self.size):
            for j in range(self.size):
                self.fixed[i][j] = (self.board[i][j] != 0)
    
    def print_board(self, board=None, show_colors=True):
        """
        Imprime o tabuleiro de forma formatada
        
        Args:
            board: Tabuleiro a imprimir (usa self.board se None)
            show_colors: Se True, mostra cores (verde para fixos, branco para jogador)
        """
        if board is None:
            board = self.board
        
        print("\n  " + "─" * 25)
        for i in range(self.size):
            if i % 3 == 0 and i != 0:
                print("  " + "─" * 25)
            
            row_str = "  "
            for j in range(self.size):
                if j % 3 == 0 and j != 0:
                    row_str += "│ "
                
                if board[i][j] == 0:
                    row_str += ". "
                else:
                    # Aplica cor: verde para fixos, branco para jogados
                    if show_colors and board == self.board:
                        if self.fixed[i][j]:
                            row_str += self.GREEN + str(board[i][j]) + self.RESET + " "
                        else:
                            row_str += self.WHITE + str(board[i][j]) + self.RESET + " "
                    else:
                        row_str += str(board[i][j]) + " "
            
            print(row_str)
        print("  " + "─" * 25 + "\n")
    
    def play(self, row, col, num):
        """
        Faz uma jogada
        
        Args:
            row: Linha (0-8)
            col: Coluna (0-8)
            num: Número a colocar (1-9)
            
        Returns:
            bool: True se a jogada é válida
        """
        if not (0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9):
            print("Posição ou número inválido!")
            return False
        
        # Verifica se é uma célula fixa (original do puzzle)
        if self.fixed[row][col]:
            print("Você não pode modificar os números originais do puzzle!")
            return False
        
        if self.board[row][col] != 0:
            print("Esta célula já está preenchida! Use 'apagar' para remover.")
            return False
        
        if self.is_valid(self.board, row, col, num):
            self.board[row][col] = num
            print("Jogada válida!")
            return True
        else:
            print("Número inválido para esta posição!")
            return False
    
    def erase(self, row, col):
        """
        Apaga um número colocado pelo jogador
        
        Args:
            row: Linha (0-8)
            col: Coluna (0-8)
            
        Returns:
            bool: True se conseguiu apagar
        """
        if not (0 <= row < 9 and 0 <= col < 9):
            print("Posição inválida!")
            return False
        
        # Verifica se é uma célula fixa (original do puzzle)
        if self.fixed[row][col]:
            print("Você não pode apagar os números originais do puzzle!")
            return False
        
        if self.board[row][col] == 0:
            print("Esta célula já está vazia!")
            return False
        
        self.board[row][col] = 0
        print("Número apagado!")
        return True
    
    def is_complete(self):
        """
        Verifica se o puzzle está completo
        
        Returns:
            bool: True se está completo e correto
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return False
                if self.board[i][j] != self.solution[i][j]:
                    return False
        return True
    
    def get_hint(self):
        """
        Fornece uma dica revelando uma célula vazia
        
        Returns:
            tuple: (row, col, num) ou None se completo
        """
        empty_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    empty_cells.append((i, j))
        
        if not empty_cells:
            return None
        
        row, col = random.choice(empty_cells)
        num = self.solution[row][col]
        return (row, col, num)
    
    def show_solution(self):
        """Mostra a solução completa"""
        print("\nSolução:")
        self.print_board(self.solution)
    
    def reset(self):
        """Gera um novo puzzle"""
        self.generate_puzzle()


def main():
    """Função principal para demonstrar o uso da classe"""
    print("Bem-vindo ao Sudoku!")
    print("\nEscolha a dificuldade:")
    print("1 - Fácil")
    print("2 - Médio")
    print("3 - Difícil")
    
    choice = input("\nEscolha (1-3): ").strip()
    difficulty_map = {'1': 'easy', '2': 'medium', '3': 'hard'}
    difficulty = difficulty_map.get(choice, 'medium')
    
    game = Sudoku(difficulty)
    
    print(f"\nSudoku - Nível: {difficulty.capitalize()}")
    game.print_board()
    
    print("\nComandos:")
    print("  jogar <linha> <coluna> <número> - Faz uma jogada (ex: jogar 0 0 5)")
    print("  apagar <linha> <coluna> - Apaga um número que você colocou (ex: apagar 0 0)")
    print("  dica - Mostra uma dica")
    print("  solucao - Mostra a solução completa")
    print("  mostrar - Mostra o tabuleiro atual")
    print("  novo - Gera um novo puzzle")
    print("  sair - Sair do jogo")
    
    while True:
        command = input("\n> ").strip().lower().split()
        
        if not command:
            continue
        
        if command[0] == 'sair':
            print("Até logo!")
            break
        
        elif command[0] == 'jogar' and len(command) == 4:
            try:
                row = int(command[1])
                col = int(command[2])
                num = int(command[3])
                game.play(row, col, num)
                game.print_board()
                
                if game.is_complete():
                    print("Parabéns! Você completou o Sudoku!")
                    break
            except ValueError:
                print("Use números válidos!")
        
        elif command[0] == 'apagar' and len(command) == 3:
            try:
                row = int(command[1])
                col = int(command[2])
                game.erase(row, col)
                game.print_board()
            except ValueError:
                print("Use números válidos!")
        
        elif command[0] == 'dica':
            hint = game.get_hint()
            if hint:
                row, col, num = hint
                print(f"Dica: Linha {row}, Coluna {col} = {num}")
            else:
                print("Não há mais dicas - puzzle completo!")
        
        elif command[0] == 'solucao':
            game.show_solution()
        
        elif command[0] == 'mostrar':
            game.print_board()
        
        elif command[0] == 'novo':
            game.reset()
            print(f"\nNovo Sudoku - Nível: {difficulty.capitalize()}")
            game.print_board()
        
        else:
            print("Comando inválido!")


if __name__ == "__main__":
    main()
