import chess
import chess.pgn
from typing import List, Tuple, Optional

class OCRCorrector:
    def __init__(self):
        self.board = chess.Board()
        self.moves = []
        self.move_history: List[Tuple[str, List[Tuple[float, str]]]] = []  # (accepted_move, candidates)
        
    def display_current_state(self) -> None:
        print("\nCurrent position:")
        print(self.board)
        print("\nMove history:")
        for i, (move, _) in enumerate(self.move_history):
            if i % 2 == 0:
                print(f"{i//2 + 1}. {move}", end=" ")
            else:
                print(move)
    
    def try_candidates(self, candidates: List[Tuple[float, str]]) -> Optional[str]:
        for _, san in candidates:
            try:
                _ = self.board.parse_san(san)
                return san
            except:
                continue
        return None
    
    def reconstruct_game_to_move(self, history_index: int) -> None:
        self.board = chess.Board()
        for i in range(history_index):
            try:
                self.board.push_san(self.move_history[i][0])
            except chess.IllegalMoveError as e:
                print(f"Error reconstructing game at move {i//2 + 1}{'.' if i%2==0 else '...'}: {e}")
                raise
    
    def update_board_to_current(self) -> None:
        self.reconstruct_game_to_move(len(self.move_history))
    
    def edit_move(self, move_number: int, is_white: bool) -> bool:
        history_index = (move_number - 1) * 2 + (0 if is_white else 1)
        
        if history_index < 0 or history_index >= len(self.move_history):
            print(f"Invalid move number. No {'white' if is_white else 'black'} move exists for move {move_number}.")
            return False
            
        # Create temporary board for move validation
        temp_board = chess.Board()
        for i in range(history_index):
            temp_board.push_san(self.move_history[i][0])
            
        print(f"\nPosition before move {move_number}{'.' if is_white else '...'}")
        print(temp_board)
        print(f"Current move: {self.move_history[history_index][0]}")
        print("Original candidates:", [san for _, san in self.move_history[history_index][1]])
        
        new_move = input("Enter the correct move: ")
        try:
            # Validate the move on temporary board
            temp_board.push_san(new_move)
            
            # If move is legal, update the history and reconstruct the game
            self.move_history[history_index] = (new_move, self.move_history[history_index][1])
            # Truncate move history to remove all moves after the edited move
            self.move_history = self.move_history[:history_index + 1]
            
            # Reconstruct the board to the current position
            self.reconstruct_game_to_move(len(self.move_history))
            return True
            
        except chess.IllegalMoveError:
            print("Invalid move.")
            return False
    
    def process_moves(self, move_candidates: List[List[Tuple[float, str]]]) -> None:
        move_num = 0
        while move_num < len(move_candidates):
            candidates = move_candidates[move_num]
            current_move = (move_num // 2) + 1
            is_white = move_num % 2 == 0
            
            # Try to find a legal move among candidates
            legal_move = self.try_candidates(candidates)
            
            if legal_move:
                self.board.push_san(legal_move)
                self.move_history.append((legal_move, candidates))
                move_num += 1
                continue
                
            # No legal moves found among candidates
            self.display_current_state()
            print(f"\nNo legal moves found for move {current_move}{'.' if is_white else '...'}")
            print("Candidates were:", [san for _, san in candidates])
            
            while True:
                action = input("\nOptions:\n1. Enter correct move\n2. Edit previous move\n3. Show current position\nChoice (1-3): ")
                
                if action == "1":
                    new_move = input(f"Enter the correct move for {'white' if is_white else 'black'}: ")
                    try:
                        self.board.push_san(new_move)
                        self.move_history.append((new_move, candidates))
                        move_num += 1
                        break
                    except:
                        print("Invalid move. The move might be illegal, or there might be an error in a previous move.")
                
                elif action == "2":
                    move_number = int(input("Enter move number: "))
                    color_input = input("White or Black? (w/b): ").lower()
                    if color_input not in ['w', 'b', 'white', 'black']:
                        print("Invalid color. Please enter 'w' or 'b'.")
                        continue
                    
                    is_white_move = color_input.startswith('w')
                    if self.edit_move(move_number, is_white_move):
                        # Reset move_num to continue from the edited move
                        history_index = (move_number - 1) * 2 + (0 if is_white_move else 1)
                        move_num = history_index + 1
                        break
                    
                elif action == "3":
                    self.update_board_to_current()
                    self.display_current_state()
                
                else:
                    print("Invalid choice.")
    
    def get_pgn(self) -> str:
        pgn = ""
        for i in range(0, len(self.move_history), 2):
            pgn += f" {i//2 + 1}. "
            white_move = self.move_history[i][0]
            pgn += white_move + " "
            if i+1 < len(self.move_history):
                black_move = self.move_history[i+1][0]
                pgn += black_move
        return pgn
    
    def get_lichess_url(self) -> str:
        moves = [move for move, _ in self.move_history]
        return 'https://lichess.org/analysis/pgn/' + '_'.join(moves)
    

# def error_correct1(move_candidates):
#     moves = []
#     board = chess.Board()
#     for candidate_list in move_candidates:
#         color = 'white' if board.turn == chess.WHITE else 'black'
#         for _, san in candidate_list:
#             try:
#                 move = board.parse_san(san)
#                 board.push(move)
#                 moves.append(san)
#                 break
#             except:
#                 continue
#         else:
#             #raise Exception("No legal move detected:", candidate_list)
#             print(moves)
#             #print(candidate_list)
#             manual_san = input(f"What move did {color} make on move {board.fullmove_number}?\n{board}\n\n")
#             try:
#                 move = board.push_san(manual_san)
#                 moves.append(manual_san)
#             except:
#                 print("Invalid move. Either you entered an illegal move, or a move was incorrectly recognized in an earlier move.")

#     return moves

# def error_correct(move_candidates):
#     moves = []
#     boards = [chess.Board()]  # Keep track of board states after each move
    
#     for candidate_list in move_candidates:
#         while True:
#             board = boards[-1].copy()  # Use the last valid board state
#             color = 'white' if board.turn == chess.WHITE else 'black'
            
#             for _, san in candidate_list:
#                 try:
#                     move = board.parse_san(san)
#                     board.push(move)
#                     moves.append(san)
#                     boards.append(board)
#                     break
#                 except:
#                     continue
#             else:
#                 # When no valid move is detected, ask for user input
#                 print("Moves so far:", moves)
#                 manual_san = input(f"What move did {color} make on move {board.fullmove_number}?\n{board}\n\n")
#                 try:
#                     move = board.push_san(manual_san)
#                     moves.append(manual_san)
#                     boards.append(board)
#                     break
#                 except:
#                     print("Invalid move. Either you entered an illegal move, or a move was incorrectly recognized earlier.")
#                     # Allow the user to edit earlier moves
#                     edit_index = input("Enter the move number you'd like to edit, or press Enter to retry: ").strip()
#                     if edit_index.isdigit():
#                         edit_index = int(edit_index) - 1
#                         if 0 <= edit_index < len(moves):
#                             print(f"Editing move {edit_index + 1}: {moves[edit_index]}")
#                             new_san = input("Enter the corrected move: ").strip()
#                             try:
#                                 # Rebuild from the start to ensure validity
#                                 moves = moves[:edit_index] + [new_san]
#                                 boards = [chess.Board()]
#                                 for san in moves:
#                                     boards[-1].push_san(san)
#                                     boards.append(boards[-1].copy())
#                                 break
#                             except:
#                                 print("Invalid correction. The move sequence is still invalid.")
#                         else:
#                             print("Invalid move number. Try again.")
#                     else:
#                         print("Retrying the same turn.")
#     return moves

# def make_pgn(moves):
#     pgn = ""
#     for i in range(0, len(moves), 2):
#         pgn += f" {i//2 + 1}. "
#         white_move = moves[i]
#         pgn += white_move + " "
#         if i+1 < len(moves):
#             black_move = moves[i+1]
#             pgn += black_move
#     return pgn


# def make_lichess_url(moves):
#     return 'https://lichess.org/analysis/pgn/' + '_'.join(moves)
