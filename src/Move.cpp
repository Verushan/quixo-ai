#include "Move.h"

Move::Move(int startSquare, Direction direction) {
    this->mStartSquare = startSquare;
    this->mDirection = direction;
}

int Move::getStartSquare() const { return mStartSquare; }

Direction Move::getDirection() const { return mDirection; }