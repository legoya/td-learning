class Display:

    CELL_WIDTH = 5
    VERTICAL_DIVIDER = "|"
    HORIZONTAL_DIVIDER = "-"
    PLAYER_1_MARKER = "X"
    PLAYER_2_MARKER = "O"

    def __init__(self, size):
        self.size = size
        self.total_row_width = Display.CELL_WIDTH * self.size + (self.size-1) * len(Display.VERTICAL_DIVIDER)

        self.display_str = self.__init_display_str(size, self.total_row_width)

    def add_move_marker(self, player, row, col):
        marker = Display.PLAYER_1_MARKER if player == 1 else Display.PLAYER_2_MARKER

        len_of_row_and_divider = (self.total_row_width + 1) * 2  # +1 to account for newline char in display_str rows

        # number of chars to skip to get to the display row that will add the marker
        index_for_start_of_cell_row = row * len_of_row_and_divider

        # number of chars to skip chars at start of col
        index_in_column = (Display.CELL_WIDTH + 1) * col + (Display.CELL_WIDTH // 2)  # marker in middle of cell

        market_index = index_for_start_of_cell_row + index_in_column

        self.display_str = self.display_str[:market_index] + marker + self.display_str[market_index+1:]

    @staticmethod
    def __init_display_str(size, total_row_width):
        cell = " " * Display.CELL_WIDTH
        empty_row = (cell + Display.VERTICAL_DIVIDER) * (size - 1) + cell + "\n"
        vertical_divider_row = Display.HORIZONTAL_DIVIDER * total_row_width + "\n"

        display_str = (empty_row + vertical_divider_row) * (size-1) + empty_row

        return display_str
