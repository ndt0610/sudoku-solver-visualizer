import sys
import pygame
from typing import List, Optional, Set, Tuple

# --- Sudoku logic with MRV backtracking ------------------------------------
Grid = List[List[int]]

def clone_grid(grid: Grid) -> Grid:
    return [row[:] for row in grid]

def row_conflict(row: int, num: int, grid: Grid) -> bool:
    return any(grid[row][c] == num for c in range(9))

def col_conflict(col: int, num: int, grid: Grid) -> bool:
    return any(grid[r][col] == num for r in range(9))

def box_conflict(row: int, col: int, num: int, grid: Grid) -> bool:
    br = (row // 3) * 3
    bc = (col // 3) * 3
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            if grid[r][c] == num:
                return True
    return False

def is_valid_move(row: int, col: int, num: int, grid: Grid) -> bool:
    if num < 1 or num > 9:
        return False
    if grid[row][col] not in (0, num):
        return False
    prev = grid[row][col]
    grid[row][col] = 0
    ok = not row_conflict(row, num, grid) and not col_conflict(col, num, grid) and not box_conflict(row, col, num, grid)
    grid[row][col] = prev
    return ok

def grid_has_conflicts(grid: Grid) -> bool:
    for r in range(9):
        for c in range(9):
            num = grid[r][c]
            if num == 0:
                continue
            if not is_valid_move(r, c, num, grid):
                return True
    return False

def candidates(row: int, col: int, grid: Grid) -> Set[int]:
    if grid[row][col] != 0:
        return set()
    taken = set(grid[row])
    taken.update(grid[r][col] for r in range(9))
    br = (row // 3) * 3
    bc = (col // 3) * 3
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            taken.add(grid[r][c])
    return {n for n in range(1, 10) if n not in taken}

def find_mrv_cell(grid: Grid) -> Optional[Tuple[int, int, Set[int]]]:
    best: Optional[Tuple[int, int, Set[int]]] = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                cand = candidates(r, c, grid)
                if not cand:
                    return None
                if best is None or len(cand) < len(best[2]):
                    best = (r, c, cand)
                    if len(cand) == 1:
                        return best
    return best

def solve_all(grid: Grid, max_solutions: int = 300) -> List[Grid]:
    solutions: List[Grid] = []
    work = clone_grid(grid)
    if grid_has_conflicts(work):
        return solutions

    def backtrack() -> None:
        if len(solutions) >= max_solutions:
            return
        mrv = find_mrv_cell(work)
        if mrv is None:
            if all(work[r][c] != 0 for r in range(9) for c in range(9)):
                solutions.append(clone_grid(work))
            return
        r, c, cand = mrv
        for num in sorted(cand):
            if is_valid_move(r, c, num, work):
                work[r][c] = num
                backtrack()
                work[r][c] = 0

    backtrack()
    return solutions

# --- Sample puzzles (5) -----------------------------------------------------
SAMPLE_PUZZLES: List[Grid] = [
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ],
    [
        [0, 2, 0, 6, 0, 8, 0, 0, 0],
        [5, 8, 0, 0, 0, 9, 7, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [3, 7, 0, 0, 0, 0, 5, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 4],
        [0, 0, 8, 0, 0, 0, 0, 1, 3],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 9, 8, 0, 0, 0, 3, 6],
        [0, 0, 0, 3, 0, 6, 0, 9, 0],
    ],
    [
        [1, 0, 0, 0, 0, 7, 0, 9, 0],
        [0, 3, 0, 0, 2, 0, 0, 0, 8],
        [0, 0, 9, 6, 0, 0, 5, 0, 0],
        [0, 0, 5, 3, 0, 0, 9, 0, 0],
        [0, 1, 0, 0, 8, 0, 0, 0, 2],
        [6, 0, 0, 0, 0, 4, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 4, 1, 0, 0, 0, 0, 0, 7],
        [0, 0, 7, 0, 0, 0, 3, 0, 0],
    ],
    [
        [0, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 8, 0, 0, 0, 7, 0, 9, 0],
        [6, 0, 2, 0, 0, 0, 5, 0, 0],
        [0, 7, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 9, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 4, 0],
        [0, 0, 5, 0, 0, 0, 6, 0, 3],
        [0, 9, 0, 4, 0, 0, 0, 7, 0],
        [0, 0, 6, 0, 0, 0, 0, 0, 0],
    ],
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
]

# --- Pygame UI -------------------------------------------------------------
CELL_SIZE = 60
GRID_SIZE = CELL_SIZE * 9
INFO_HEIGHT = 170
WIDTH, HEIGHT = GRID_SIZE, GRID_SIZE + INFO_HEIGHT
BG_COLOR = (15, 18, 25)
GRID_COLOR = (80, 90, 110)
BOLD_GRID_COLOR = (210, 210, 230)
TEXT_COLOR = (245, 245, 245)
CLUE_COLOR = (180, 200, 255)
USER_COLOR = (255, 235, 200)
SELECT_COLOR = (70, 100, 170)
ERROR_COLOR = (210, 80, 80)
HINT_COLOR = (120, 200, 140)

def draw_grid(screen: pygame.Surface) -> None:
    for i in range(10):
        thickness = 3 if i % 3 == 0 else 1
        color = BOLD_GRID_COLOR if i % 3 == 0 else GRID_COLOR
        pygame.draw.line(screen, color, (0, i * CELL_SIZE), (GRID_SIZE, i * CELL_SIZE), thickness)
        pygame.draw.line(screen, color, (i * CELL_SIZE, 0), (i * CELL_SIZE, GRID_SIZE), thickness)

def draw_numbers(screen: pygame.Surface, grid: Grid, locked: List[List[bool]], font: pygame.font.Font) -> None:
    for r in range(9):
        for c in range(9):
            num = grid[r][c]
            if num:
                color = CLUE_COLOR if locked[r][c] else USER_COLOR
                text = font.render(str(num), True, color)
                rect = text.get_rect(center=(c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, rect)

def highlight_selected(screen: pygame.Surface, selected: Optional[Tuple[int, int]]) -> None:
    if selected is None:
        return
    r, c = selected
    rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, SELECT_COLOR, rect, 3)

def draw_error_overlay(screen: pygame.Surface) -> None:
    overlay = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    overlay.fill((ERROR_COLOR[0], ERROR_COLOR[1], ERROR_COLOR[2], 70))
    screen.blit(overlay, (0, 0))

def draw_message(screen: pygame.Surface, lines: List[str], font: pygame.font.Font) -> None:
    y = GRID_SIZE + 8
    for line in lines:
        text = font.render(line, True, TEXT_COLOR)
        screen.blit(text, (10, y))
        y += text.get_height() + 4

def load_sample(index: int) -> Tuple[Grid, List[List[bool]]]:
    g = clone_grid(SAMPLE_PUZZLES[index])
    locked = [[cell != 0 for cell in row] for row in g]
    return g, locked

def lock_current(grid: Grid) -> List[List[bool]]:
    return [[cell != 0 for cell in row] for row in grid]

def hint_for_cell(grid: Grid, locked: List[List[bool]], selected: Optional[Tuple[int, int]]) -> Tuple[Grid, List[str]]:
    if selected is None:
        return grid, ["Chọn một ô trống để gợi ý."]
    r, c = selected
    if locked[r][c]:
        return grid, ["Ô đã khóa (givens). Không gợi ý."]
    if grid[r][c] != 0:
        return grid, ["Ô đã có số. Xóa hoặc chọn ô trống khác."]
    cand = sorted(candidates(r, c, grid))
    if not cand:
        return grid, ["Ô này không có ứng viên hợp lệ (bảng đang mâu thuẫn)."]
    if len(cand) == 1:
        grid[r][c] = cand[0]
        return grid, [f"Gợi ý: chỉ có {cand[0]}, đã điền tự động."]
    return grid, ["Ứng viên: " + " ".join(str(x) for x in cand)]

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku Solver - Backtracking (Pygame)")
    font_big = pygame.font.SysFont("consolas", 32)
    font_small = pygame.font.SysFont("consolas", 20)

    grid, locked = load_sample(0)
    solutions: List[Grid] = []
    current_solution_idx = 0
    selected: Optional[Tuple[int, int]] = None
    message: List[str] = ["Chuột trái chọn ô; gõ 1-9 để nhập."]

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if x < GRID_SIZE and y < GRID_SIZE:
                    selected = (y // CELL_SIZE, x // CELL_SIZE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key in (pygame.K_BACKSPACE, pygame.K_DELETE, pygame.K_0):
                    if selected:
                        r, c = selected
                        if not locked[r][c]:
                            grid[r][c] = 0
                            solutions = []
                            message = ["Đã xóa ô."]
                        else:
                            message = ["Ô bị khóa, không xóa được."]
                if pygame.K_1 <= event.key <= pygame.K_9:
                    if selected:
                        num = event.key - pygame.K_0
                        r, c = selected
                        if locked[r][c]:
                            message = ["Ô bị khóa, không sửa được."]
                        else:
                            old = grid[r][c]
                            grid[r][c] = num
                            if grid_has_conflicts(grid):
                                grid[r][c] = old
                                message = ["Sai ràng buộc (hàng/cột/ô 3x3)."]
                            else:
                                solutions = []
                                message = [f"Đã nhập {num}."]
                if event.key in (pygame.K_s, pygame.K_RETURN):
                    if grid_has_conflicts(grid):
                        message = ["Bảng đang vi phạm luật. Sửa trước khi giải."]
                        solutions = []
                    else:
                        message = ["Đang giải bằng backtracking (MRV)..."]
                        pygame.display.flip()
                        solutions = solve_all(grid)
                        if not solutions:
                            message = ["Không tìm thấy nghiệm."]
                        else:
                            grid = clone_grid(solutions[0])
                            current_solution_idx = 0
                            extra = " (đã chặn 300)" if len(solutions) >= 300 else ""
                            message = [f"Tìm được {len(solutions)} nghiệm{extra}.", "Nhấn N để xem nghiệm tiếp."]
                if event.key == pygame.K_n:
                    if solutions:
                        current_solution_idx = (current_solution_idx + 1) % len(solutions)
                        grid = clone_grid(solutions[current_solution_idx])
                        message = [f"Đang xem nghiệm {current_solution_idx + 1}/{len(solutions)}"]
                if event.key == pygame.K_r:
                    grid, locked = load_sample(4)
                    solutions = []
                    message = ["Bảng trống, tự nhập rồi nhấn L để khóa givens."]
                if event.key == pygame.K_l:
                    locked = lock_current(grid)
                    message = ["Đã khóa các ô có số thành givens."]
                if event.key == pygame.K_h:
                    grid, message = hint_for_cell(grid, locked, selected)
                    solutions = []
                if event.key in (pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5):
                    idx = event.key - pygame.K_F1
                    grid, locked = load_sample(idx)
                    solutions = []
                    message = [f"Đã tải đề mẫu {idx + 1}. Nhấn S để giải."]

        screen.fill(BG_COLOR)
        highlight_selected(screen, selected)
        draw_grid(screen)
        draw_numbers(screen, grid, locked, font_big)
        if grid_has_conflicts(grid):
            draw_error_overlay(screen)

        help_lines = [
            "Chuột: chọn ô | 1-9: nhập | 0/Delete: xóa",
            "S/Enter: giải tất cả (tối đa 300); N: nghiệm kế",
            "R: bảng trống | L: khóa các ô đang có số",
            "H: gợi ý ô chọn | F1-F5: 5 đề mẫu",
        ]
        status = [f"Nghiệm: {len(solutions)}" + (f" (đang xem {current_solution_idx + 1})" if solutions else "")]
        draw_message(screen, help_lines + status + message, font_small)

        pygame.display.flip()

if __name__ == "__main__":
    main()
