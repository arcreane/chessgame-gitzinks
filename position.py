class Position:
    def __init__(self, column: str, row: int):
        self.column = column
        self.row = row

    def __str__(self):
        return f"{self.column}{self.row}"

if __name__ == "__main__":
    p1 = Position("e", 4)
    print(f"Position créée: {p1}")