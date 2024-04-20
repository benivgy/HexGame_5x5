import copy
import random
import math
import json
import os
import pygame
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam
import sys


class DisjointSet:
    def __init__(self, elements):
        self.parent = {element: element for element in elements}

    def find(self, element):
        if self.parent[element] != element:
            self.parent[element] = self.find(self.parent[element])
        return self.parent[element]

    def union(self, element1, element2):
        root1 = self.find(element1)
        root2 = self.find(element2)
        self.parent[root1] = root2


class RandomComputer:
    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self, game):
        empty_cells = [(row, col) for row in range(5) for col in range(5) if game.board[row][col] == 0]
        return random.choice(empty_cells)


class SmartComputer:
    def __init__(self, symbol, board_score_dicts):
        self.symbol = symbol
        self.board_score_dicts = board_score_dicts

    def make_move(self, game):
        empty_cells = [(row, col) for row in range(5) for col in range(5) if game.board[row][col] == 0]
        best_move = random.choice(empty_cells)
        enough_boards = sum(1 for row, col in empty_cells if self.count_next_boards(game, row, col) >= 5) >= len(
            empty_cells) * 0.7

        if enough_boards:
            max_score = -1

            for row, col in empty_cells:
                game_copy = copy.deepcopy(game)
                game_copy.play(row, col)

                board_state = ''.join(str(cell) for row in game_copy.board for cell in row)
                move_count = sum(1 for cell in board_state if cell != '0')
                move_range_start = min(((move_count - 1) // 5) * 5 + 1, 21)
                move_range_end = min(move_range_start + 6, 25)
                move_range_key = (move_range_start, move_range_end)

                board_scores = self.board_score_dicts[move_range_key]
                score, count = board_scores.get(board_state, (-1, -1))
                if score > max_score:
                    max_score = score
                    best_move = (row, col)

        return best_move

    def count_next_boards(self, game, row, col):
        count = 0
        game_copy = copy.deepcopy(game)
        game_copy.play(row, col)
        board_state = ''.join(str(cell) for row in game_copy.board for cell in row)
        move_count = sum(1 for cell in board_state if cell != '0')
        move_range_start = min(((move_count - 1) // 5) * 5 + 1, 21)
        move_range_end = min(move_range_start + 4, 25)
        move_range_key = (move_range_start, move_range_end)
        board_scores = self.board_score_dicts[move_range_key]

        for nei_row, nei_col in [(row + 1, col), (row + 1, col - 1), (row, col + 1), (row, col - 1), (row - 1, col),
                                 (row - 1, col + 1)]:
            if 0 <= nei_row < 5 and 0 <= nei_col < 5 and game_copy.board[nei_row][nei_col] == 0:
                game_copy_copy = copy.deepcopy(game_copy)
                game_copy_copy.play(nei_row, nei_col)
                board_state = ''.join(str(cell) for row in game_copy_copy.board for cell in row)
                if board_state in board_scores and board_scores[board_state][1] >= 5:
                    count += 1

        return count


class NeuralNetwork:
    def __init__(self, symbol, game_instances):
        self.model = self.build_model()
        self.symbol = symbol
        self.game_instances = game_instances
        self.train()

    def build_model(self):
        model = Sequential([
            Flatten(input_shape=(5, 5)),
            Dense(64, activation='relu'),
            Dense(128, activation='relu'),
            Dense(64, activation='relu'),
            Dense(1)
        ])
        model.compile(optimizer=Adam(), loss='mse')
        return model

    def train(self):
        X_train = []
        y_train = []
        for game in self.game_instances:
            encoded_board = self.encode_board(game)
            X_train.append(encoded_board)
            y_train.append(self.score_board(game))

        X_train = np.array(X_train)
        y_train = np.array(y_train)

        X_train = np.reshape(X_train, (-1, 5, 5))

        self.model.fit(X_train, y_train, epochs=150, verbose=0)

    def encode_board(self, board):
        encoded_board = np.zeros((5, 5))
        for i in range(5):
            for j in range(5):
                if board[i][j] == 1:
                    encoded_board[i][j] = 2
                elif board[i][j] == 0:
                    encoded_board[i][j] = 1
        return encoded_board

    def score_board(self, board):
        encoded_board = self.encode_board(board)
        encoded_board = np.expand_dims(encoded_board, axis=0)
        score = self.model.predict(encoded_board)[0][0]
        return score

    def make_move(self, game):
        empty_cells = [(row, col) for row in range(5) for col in range(5) if game.board[row][col] == 0]
        best_move = random.choice(empty_cells)
        max_score = float('-inf')

        for row, col in empty_cells:
            game_copy = copy.deepcopy(game)
            game_copy.play(row, col)
            score = self.score_board(game_copy.board)
            if score > max_score:
                max_score = score
                best_move = (row, col)

        return best_move


class Games:
    def __init__(self):
        self.move_ranges = [(1, 5), (6, 10), (11, 15), (16, 20), (21, 25)]
        self.board_score_dicts = self.load_board_scores()
        self.game_instance = None
        # Prepare game instances for neural network training
        self.game_instances = self.prepare_game_instances()

    def prepare_game_instances(self):
        game_instances = []
        for board_range in self.board_score_dicts.values():
            for board_state, _ in board_range.items():
                game = HexGame()
                game.board = [[int(cell) for cell in board_state[i:i + 5]] for i in range(0, len(board_state), 5)]
                game_instances.append(game.board)
        return game_instances

    def load_board_scores(self):
        board_score_dicts = {}
        for move_range_start, move_range_end in self.move_ranges:
            filename = os.path.join('json_files', f'Hex_board_scores_{move_range_start}-{move_range_end}.json')
            if os.path.exists(filename):
                with open(filename, 'r') as json_file:
                    board_score_dicts[(move_range_start, move_range_end)] = json.load(json_file)
            else:
                board_score_dicts[(move_range_start, move_range_end)] = {}
        return board_score_dicts

    def get_filename(self, move_range):
        return os.path.join('json_files', f'Hex_board_scores_{move_range[0]}-{move_range[1]}.json')

    def play_random_vs_human_game(self):
        self.game_instance = HexGame()
        random_comp = RandomComputer(2)
        human_player = HumanPlayer(1, self.game_instance)
        self.play_game(random_comp, human_player)


    def play_smart_vs_human_game(self):
        self.game_instance = HexGame()
        smart_comp = SmartComputer(2, self.board_score_dicts)
        human_player = HumanPlayer(1, self.game_instance)
        self.play_game(smart_comp, human_player)

    def play_neural_network_vs_human_game(self):
        self.game_instance = HexGame()
        neural_net = NeuralNetwork(2, self.game_instances)
        human_player = HumanPlayer(1, self.game_instance)
        self.play_game(neural_net, human_player)

    def play_game(self, computer, human):
        pygame.init()
        size = width, height = 800, 600
        screen = pygame.display.set_mode(size)
        cell_size = 50
        x_offset = 100
        clock = pygame.time.Clock()


        while not self.game_instance.winner:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.game_instance.current_player == 'red':
                row, col = computer.make_move(self.game_instance)
                self.game_instance.play(row, col)
            else:
                index = human.make_move()
                if index !=None:
                    row,col = index
                    self.game_instance.play(row, col)


            screen.fill((0, 0, 0))
            self.game_instance.draw_board(screen, cell_size, x_offset)
            pygame.display.flip()
            clock.tick(60)

        if self.game_instance.winner == 2:
            self.display_message(screen, "You win!", width // 2, height // 2)
        else:
            self.display_message(screen, "Opponent wins", width // 2, height // 2)

        self.display_message(screen, "Press any key to play again", width // 2, height // 2 + 50)
        pygame.display.flip()

        self.wait_for_key()
        pygame.quit()

    def display_message(self, screen, text, x, y):
        font = pygame.font.Font(None, 36)
        message = font.render(text, True, (255, 255, 255))
        message_rect = message.get_rect(center=(x, y))
        screen.blit(message, message_rect)

    def wait_for_key(self):
        pygame.event.clear()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False


class HexGame:
    def __init__(self, n=5):
        self.n = n
        self.board = [[0] * n for _ in range(n)]
        self.cells = [(i, j) for i in range(n) for j in range(n)]
        self.top_node = (-1, 0)
        self.bottom_node = (n, 0)
        self.left_node = (0, -1)
        self.right_node = (0, n)
        self.ds_red = DisjointSet(self.cells + [self.top_node, self.bottom_node])
        self.ds_blue = DisjointSet(self.cells + [self.left_node, self.right_node])
        for i in range(n):
            self.ds_red.union((0, i), self.top_node)
            self.ds_red.union((n - 1, i), self.bottom_node)
            self.ds_blue.union((i, 0), self.left_node)
            self.ds_blue.union((i, n - 1), self.right_node)
        self.winner = None
        self.current_player = 'blue'

    def play(self, i, j):
        assert 0 <= i < self.n and 0 <= j < self.n and self.board[i][j] == 0
        code = 1 if self.current_player == 'red' else 2
        self.board[i][j] = code
        for nei_i, nei_j in [(i + 1, j), (i + 1, j - 1), (i, j + 1), (i, j - 1), (i - 1, j), (i - 1, j + 1)]:
            if 0 <= nei_i < self.n and 0 <= nei_j < self.n and code == self.board[nei_i][nei_j]:
                if self.current_player == 'red':
                    self.ds_red.union((nei_i, nei_j), (i, j))
                else:
                    self.ds_blue.union((nei_i, nei_j), (i, j))
        if self.ds_red.find(self.top_node) == self.ds_red.find(self.bottom_node):
            self.winner = 1
        elif self.ds_blue.find(self.left_node) == self.ds_blue.find(self.right_node):
            self.winner = 2
        self.current_player = 'blue' if self.current_player == 'red' else 'red'
        return self.winner

    def hex_to_pixel(self, row, col, size, x_offset):
        x = size * 1.5 * col + x_offset
        y = size * (math.sqrt(3) * row + math.sqrt(3) / 2 * col)
        return x, y

    def draw_board(self, screen, cell_size, x_offset):
        for row in range(5):
            for col in range(5):
                x, y = self.hex_to_pixel(row, col, cell_size, x_offset)
                hexagon_points = [
                    (x, y),
                    (x + cell_size, y),
                    (x + 1.5 * cell_size, y + math.sqrt(3) / 2 * cell_size),
                    (x + cell_size, y + math.sqrt(3) * cell_size),
                    (x, y + math.sqrt(3) * cell_size),
                    (x - 0.5 * cell_size, y + math.sqrt(3) / 2 * cell_size),
                ]
                pygame.draw.polygon(screen, (200, 200, 200), hexagon_points, 1)
                if self.board[row][col] == 1:
                    pygame.draw.polygon(screen, (255, 0, 0), hexagon_points)
                elif self.board[row][col] == 2:
                    pygame.draw.polygon(screen, (0, 0, 255), hexagon_points)


class HumanPlayer:
    def __init__(self, symbol, game_instance):
        self.symbol = symbol
        self.game_instance = game_instance

    def make_move(self):
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pressed[0]:
            x, y = mouse_pos
            col = int((x - 100) // 86)
            row = int((y - 50) // 100)
            if 0 <= row < 5 and 0 <= col < 5 and self.game_instance.board[row][col] == 0:
                return row, col
        return None



def main():
    game = Games()
    while True:
        menu = Menu()
        choice = menu.run_menu()

        if choice == 1:
            game.play_random_vs_human_game()
        elif choice == 2:
            game.play_smart_vs_human_game()
        elif choice == 3:
            game.play_neural_network_vs_human_game()
        elif choice == 4:
            pygame.quit()
            sys.exit()


class Menu:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode(self.size)
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

    def run_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return 1
                    elif event.key == pygame.K_2:
                        return 2
                    elif event.key == pygame.K_3:
                        return 3

            self.screen.fill((0, 0, 0))
            self.display_message("Hex Game Menu", self.width // 2, 50)
            self.display_message("1. Easy Mode (Random vs. Human)", self.width // 2, 225)
            self.display_message("2. Medium Mode (Smart vs. Human)", self.width // 2, 325)
            self.display_message("3. Hard Mode (Neural Network vs. Human)", self.width // 2, 425)
            pygame.display.flip()
            self.clock.tick(60)

    def display_message(self, text, x, y):
        message = self.font.render(text, True, (255, 255, 255))
        message_rect = message.get_rect(center=(x, y))
        self.screen.blit(message, message_rect)


if __name__ == "__main__":
    main()
