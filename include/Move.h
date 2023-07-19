#include <string>

enum Direction { North, South, East, West };

class Move {
  private:
    int mStartSquare;
    Direction mDirection;

  public:
    Move(int startSquare, Direction direction);

    int getStartSquare() const;

    Direction getDirection() const;
};