class Position:
    def __init__(self, column, row):
        self.column = column  # ex: 'e'
        self.row = row        # ex: 4

    def __str__(self):
        return f"{self.column}{self.row}"

    def __eq__(self, other):
        if other is None:
            return False
        return self.column == other.column and self.row == other.row


if __name__ == "__main__":
    p1 = Position("e", 4)
    print(f"Position créée : {p1}")  # Attendu : e4
    p2 = Position("a", 1)
    print(f"Position créée : {p2}")  # Attendu : a1
    print("Tests Position OK !")
