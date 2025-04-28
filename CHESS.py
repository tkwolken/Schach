import tkinter as tk


# Funktion zum Zeichnen des Schachbretts
def draw_board(canvas, square_size):
    dark_color = "#FFD700"  # Goldgelb
    light_color = "#e393b9"  # Rosa
    for row in range(8):
        for col in range(8):
            x1, y1 = col * square_size, row * square_size
            x2, y2 = x1 + square_size, y1 + square_size #FFD700
            color = dark_color if (row + col) % 2 == 0 else light_color
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)
    # Zeichne die Figuren basierend auf der `pieces`-Liste
    for row in range(8):  #das "in" hier ist keine Wahrheitsabfrage
        for col in range(8):
            piece = pieces[row][col]
            if piece:
                place_piece(canvas, piece, row, col, square_size)


# Funktion zum Platzieren einer Schachfigur auf dem Schachbrett
def place_piece(canvas, piece_type, row, col, square_size):
    x, y = col * square_size, row * square_size
    piece_color = "white" if piece_type.isupper() else "black"
    canvas.create_text(x + square_size / 2, y + square_size / 2, text=piece_type, fill=piece_color)


# Fenster erstellen
root = tk.Tk()
root.title("Schachspiel")
# Canvas erstellen und Schachbrett zeichnen
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()
# Größe jedes Schachbrettfelds in Pixel
square_size = 50
# Standard-Schachaufstellung
pieces = [
    ["R", "N", "B", "BEBIK", "TOBAI", "B", "N", "R"],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["r", "n", "b", "bebik", "tobai", "b", "n", "r"]
]
# Initialisiere Auswahl
selected_piece = None
selected_row, selected_col = None, None


# Funktion zur Überprüfung des Pfads für lineare Bewegungen
def is_path_clear(start_row, start_col, end_row, end_col):
    step_row = (end_row - start_row) // max(1, abs(end_row - start_row))
    step_col = (end_col - start_col) // max(1, abs(end_col - start_col))
    current_row, current_col = start_row + step_row, start_col + step_col
    while (current_row, current_col) != (end_row, end_col):
        if pieces[current_row][current_col] != "":
            return False
        current_row += step_row
        current_col += step_col
    return True


# Funktion zur Überprüfung der Bewegungsregeln
def is_valid_move(piece, start_row, start_col, end_row, end_col):
    delta_row = end_row - start_row
    delta_col = end_col - start_col
    if piece.lower() == "p":  # Bauer
        direction = 1 if piece.isupper() else -1
        if delta_col == 0 and delta_row == direction and pieces[end_row][end_col] == "":
            return True
        elif delta_col == 0 and delta_row == 2 * direction and start_row in (1, 6) and pieces[end_row][end_col] == "":
            return True
        elif abs(delta_col) == 1 and delta_row == direction and pieces[end_row][end_col] != "":
            return True
    elif piece.lower() == "r":  # Turm
        if (delta_row == 0 or delta_col == 0) and is_path_clear(start_row, start_col, end_row, end_col):
            return True
    elif piece.lower() == "b":  # Läufer
        if abs(delta_row) == abs(delta_col) and is_path_clear(start_row, start_col, end_row, end_col):
            return True
    elif piece.lower() == "bebik":  # Dame
        if (delta_row == 0 or delta_col == 0 or abs(delta_row) == abs(delta_col)) and is_path_clear(start_row,
                                                                                                    start_col, end_row,
                                                                                                    end_col):
            return True
    elif piece.lower() == "tobai":  # König
        if abs(delta_row) <= 1 and abs(delta_col) <= 1:
            return True
    elif piece.lower() == "n":  # Springer
        if (abs(delta_row), abs(delta_col)) in [(2, 1), (1, 2)]:
            return True
    return False


# Funktion für Klickereignis
def handle_click(event):
    global selected_piece, selected_row, selected_col
    col = event.x // square_size
    row = event.y // square_size
    if selected_piece is None:
        selected_piece = pieces[row][col]
        selected_row, selected_col = row, col
    else:
        if is_valid_move(selected_piece, selected_row, selected_col, row, col):
            target_piece = pieces[row][col]
            # Verhindere, dass eigene Figuren geschlagen werden
            if target_piece != "" and (selected_piece.isupper() == target_piece.isupper()):
                selected_piece = None
                return
            pieces[row][col] = selected_piece
            pieces[selected_row][selected_col] = ""
            draw_board(canvas, square_size)
        selected_piece = None


# Tkinter-Ereignisbindung für Mausklicks auf das Canvas
canvas.bind("<Button-1>", handle_click)
# Schachbrett zeichnen
draw_board(canvas, square_size)
# Fenster starten
root.mainloop()

