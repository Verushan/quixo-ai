enum Direction { North, South, East, West };

class Move {
  public:
    int startSquare;
    Direction direction;

    Move(int startSquare, Direction direction) {
        this->startSquare = startSquare;
        this->direction = direction;
    }
};