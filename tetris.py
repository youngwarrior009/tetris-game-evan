#!/usr/bin/env python3
"""
Tetris Game - Creator: Evan
A fully functional Tetris game with player names and high score storage.
"""

import pygame
import random
import json
import os
from enum import Enum
from collections import deque

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30
GAME_SPEED = 30  # Lower is faster

# Colors (Original Tetris style)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (128, 128, 128)
COLOR_DARK_GRAY = (64, 64, 64)
COLOR_CYAN = (0, 255, 255)      # I piece
COLOR_BLUE = (0, 0, 255)        # J piece
COLOR_ORANGE = (255, 165, 0)    # L piece
COLOR_YELLOW = (255, 255, 0)    # O piece
COLOR_GREEN = (0, 255, 0)       # S piece
COLOR_PURPLE = (128, 0, 128)    # T piece
COLOR_RED = (255, 0, 0)         # Z piece

PIECE_COLORS = [COLOR_CYAN, COLOR_BLUE, COLOR_ORANGE, COLOR_YELLOW, 
                COLOR_GREEN, COLOR_PURPLE, COLOR_RED]

# Tetromino shapes
TETROMINOS = [
    # I piece
    [[1, 1, 1, 1]],
    # O piece
    [[1, 1], [1, 1]],
    # T piece
    [[0, 1, 0], [1, 1, 1]],
    # S piece
    [[0, 1, 1], [1, 1, 0]],
    # Z piece
    [[1, 1, 0], [0, 1, 1]],
    # J piece
    [[1, 0, 0], [1, 1, 1]],
    # L piece
    [[0, 0, 1], [1, 1, 1]]
]

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
    SCORE_ENTRY = 4

class TetrisGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris - Creator: Evan")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
        
        self.scores_file = "scores.json"
        self.player_scores = self.load_scores()
        
        self.state = GameState.MENU
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.current_color = None
        self.piece_x = GRID_WIDTH // 2 - 1
        self.piece_y = 0
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.fall_speed = GAME_SPEED
        self.fall_counter = 0
        self.player_name = ""
        self.game_over = False
        self.game_over_time = 0
        
        self.spawn_piece()
    
    def load_scores(self):
        """Load scores from file"""
        if os.path.exists(self.scores_file):
            try:
                with open(self.scores_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_scores(self):
        """Save scores to file"""
        with open(self.scores_file, 'w') as f:
            json.dump(self.player_scores, f, indent=4)
    
    def add_score(self, name, score, lines):
        """Add a new score to the list"""
        self.player_scores.append({
            "name": name,
            "score": score,
            "lines": lines
        })
        self.player_scores.sort(key=lambda x: x["score"], reverse=True)
        self.player_scores = self.player_scores[:10]  # Keep top 10
        self.save_scores()
    
    def spawn_piece(self):
        """Spawn a new Tetromino piece"""
        piece_index = random.randint(0, len(TETROMINOS) - 1)
        self.current_piece = [row[:] for row in TETROMINOS[piece_index]]
        self.current_color = PIECE_COLORS[piece_index]
        self.piece_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0
        
        if self.collision():
            self.game_over = True
            self.state = GameState.GAME_OVER
    
    def collision(self, dx=0, dy=0, piece=None):
        """Check if current piece collides with grid or boundaries"""
        if piece is None:
            piece = self.current_piece
        
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.piece_x + x + dx
                    grid_y = self.piece_y + y + dy
                    
                    if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y >= GRID_HEIGHT:
                        return True
                    
                    if grid_y >= 0 and self.grid[grid_y][grid_x]:
                        return True
        
        return False
    
    def rotate_piece(self):
        """Rotate the current piece 90 degrees clockwise"""
        rotated = [[self.current_piece[len(self.current_piece) - 1 - j][i] 
                    for j in range(len(self.current_piece))] 
                   for i in range(len(self.current_piece[0]))]
        
        if not self.collision(piece=rotated):
            self.current_piece = rotated
    
    def place_piece(self):
        """Place the current piece on the grid"""
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.piece_x + x
                    grid_y = self.piece_y + y
                    if 0 <= grid_y < GRID_HEIGHT and 0 <= grid_x < GRID_WIDTH:
                        self.grid[grid_y][grid_x] = self.current_color
        
        self.clear_lines()
        self.spawn_piece()
    
    def clear_lines(self):
        """Clear completed lines"""
        lines_to_clear = []
        
        for y, row in enumerate(self.grid):
            if all(cell for cell in row):
                lines_to_clear.append(y)
        
        for y in reversed(lines_to_clear):
            del self.grid[y]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            # Score calculation
            line_count = len(lines_to_clear)
            if line_count == 1:
                self.score += 100
            elif line_count == 2:
                self.score += 300
            elif line_count == 3:
                self.score += 500
            elif line_count == 4:
                self.score += 800
            
            self.level = 1 + self.lines_cleared // 10
            self.fall_speed = max(5, GAME_SPEED - self.level * 2)
    
    def move_piece(self, dx):
        """Move piece left or right"""
        if not self.collision(dx=dx):
            self.piece_x += dx
    
    def drop_piece(self):
        """Drop piece one line"""
        if not self.collision(dy=1):
            self.piece_y += 1
        else:
            self.place_piece()
    
    def handle_input(self):
        """Handle keyboard input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.start_game()
                    elif event.key == pygame.K_h:
                        self.show_high_scores()
                    elif event.key == pygame.K_q:
                        return False
                
                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_LEFT:
                        self.move_piece(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece(1)
                    elif event.key == pygame.K_DOWN:
                        self.drop_piece()
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        while not self.collision(dy=1):
                            self.piece_y += 1
                        self.drop_piece()
                    elif event.key == pygame.K_p:
                        # Pause functionality could be added here
                        pass
                
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.state = GameState.SCORE_ENTRY
                        self.player_name = ""
                    elif event.key == pygame.K_RETURN:
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        self.state = GameState.MENU
                        self.reset_game()
                
                elif self.state == GameState.SCORE_ENTRY:
                    if event.key == pygame.K_RETURN:
                        if self.player_name.strip():
                            self.add_score(self.player_name, self.score, self.lines_cleared)
                            self.state = GameState.MENU
                            self.reset_game()
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif event.unicode.isprintable():
                        if len(self.player_name) < 20:
                            self.player_name += event.unicode
        
        return True
    
    def start_game(self):
        """Start a new game"""
        self.state = GameState.PLAYING
        self.reset_game()
    
    def reset_game(self):
        """Reset game state"""
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.fall_speed = GAME_SPEED
        self.game_over = False
        self.player_name = ""
        self.spawn_piece()
    
    def show_high_scores(self):
        """Display high scores (for future enhancement)"""
        pass
    
    def update(self):
        """Update game state"""
        if self.state != GameState.PLAYING:
            return
        
        self.fall_counter += 1
        
        if self.fall_counter >= self.fall_speed:
            self.fall_counter = 0
            self.drop_piece()
    
    def draw(self):
        """Draw the game"""
        self.screen.fill(COLOR_BLACK)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        elif self.state == GameState.SCORE_ENTRY:
            self.draw_score_entry()
        
        pygame.display.flip()
    
    def draw_menu(self):
        """Draw the main menu"""
        title = self.font_large.render("TETRIS", True, COLOR_CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        creator = self.font_small.render("Creator: Evan", True, COLOR_WHITE)
        creator_rect = creator.get_rect(center=(SCREEN_WIDTH // 2, 180))
        self.screen.blit(creator, creator_rect)
        
        start = self.font_medium.render("Press SPACE to Start", True, COLOR_GREEN)
        start_rect = start.get_rect(center=(SCREEN_WIDTH // 2, 350))
        self.screen.blit(start, start_rect)
        
        high_scores = self.font_small.render("Press H for High Scores", True, COLOR_YELLOW)
        high_scores_rect = high_scores.get_rect(center=(SCREEN_WIDTH // 2, 450))
        self.screen.blit(high_scores, high_scores_rect)
        
        quit_text = self.font_small.render("Press Q to Quit", True, COLOR_RED)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, 550))
        self.screen.blit(quit_text, quit_rect)
        
        if self.player_scores:
            top_score = self.font_small.render(
                f"Top Score: {self.player_scores[0]['name']} - {self.player_scores[0]['score']}",
                True, COLOR_WHITE
            )
            top_score_rect = top_score.get_rect(center=(SCREEN_WIDTH // 2, 700))
            self.screen.blit(top_score, top_score_rect)
    
    def draw_game(self):
        """Draw the main game"""
        # Draw grid background
        grid_x = (SCREEN_WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2
        grid_y = 50
        
        # Draw border
        pygame.draw.rect(self.screen, COLOR_WHITE, 
                        (grid_x - 2, grid_y - 2, GRID_WIDTH * BLOCK_SIZE + 4, GRID_HEIGHT * BLOCK_SIZE + 4), 3)
        
        # Draw grid cells
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                rect = pygame.Rect(grid_x + x * BLOCK_SIZE, grid_y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                if cell:
                    pygame.draw.rect(self.screen, cell, rect)
                    pygame.draw.rect(self.screen, COLOR_DARK_GRAY, rect, 1)
                else:
                    pygame.draw.rect(self.screen, COLOR_DARK_GRAY, rect, 1)
        
        # Draw current piece
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        grid_x + (self.piece_x + x) * BLOCK_SIZE,
                        grid_y + (self.piece_y + y) * BLOCK_SIZE,
                        BLOCK_SIZE, BLOCK_SIZE
                    )
                    pygame.draw.rect(self.screen, self.current_color, rect)
                    pygame.draw.rect(self.screen, COLOR_WHITE, rect, 2)
        
        # Draw info panel
        info_x = grid_x + GRID_WIDTH * BLOCK_SIZE + 40
        
        score_text = self.font_small.render("SCORE", True, COLOR_WHITE)
        self.screen.blit(score_text, (info_x, 50))
        score_value = self.font_medium.render(str(self.score), True, COLOR_YELLOW)
        self.screen.blit(score_value, (info_x, 90))
        
        level_text = self.font_small.render("LEVEL", True, COLOR_WHITE)
        self.screen.blit(level_text, (info_x, 180))
        level_value = self.font_medium.render(str(self.level), True, COLOR_CYAN)
        self.screen.blit(level_value, (info_x, 220))
        
        lines_text = self.font_small.render("LINES", True, COLOR_WHITE)
        self.screen.blit(lines_text, (info_x, 310))
        lines_value = self.font_medium.render(str(self.lines_cleared), True, COLOR_GREEN)
        self.screen.blit(lines_value, (info_x, 350))
    
    def draw_game_over(self):
        """Draw game over screen"""
        self.draw_game()  # Draw the game board first
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("GAME OVER", True, COLOR_RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.font_medium.render(f"Score: {self.score}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        lines_text = self.font_medium.render(f"Lines: {self.lines_cleared}", True, COLOR_WHITE)
        lines_rect = lines_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(lines_text, lines_rect)
        
        save_text = self.font_small.render("Press SPACE to Save Score", True, COLOR_GREEN)
        save_rect = save_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        self.screen.blit(save_text, save_rect)
        
        menu_text = self.font_small.render("Press Q for Menu", True, COLOR_YELLOW)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))
        self.screen.blit(menu_text, menu_rect)
    
    def draw_score_entry(self):
        """Draw score entry screen"""
        self.screen.fill(COLOR_BLACK)
        
        title = self.font_large.render("NEW HIGH SCORE!", True, COLOR_CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        score_text = self.font_medium.render(f"Score: {self.score}", True, COLOR_YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(score_text, score_rect)
        
        name_label = self.font_small.render("Enter Your Name:", True, COLOR_WHITE)
        name_rect = name_label.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(name_label, name_rect)
        
        name_box = self.font_medium.render(self.player_name + "_", True, COLOR_GREEN)
        name_box_rect = name_box.get_rect(center=(SCREEN_WIDTH // 2, 480))
        self.screen.blit(name_box, name_box_rect)
        
        continue_text = self.font_small.render("Press ENTER to Continue", True, COLOR_GRAY)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, 600))
        self.screen.blit(continue_text, continue_rect)
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()
