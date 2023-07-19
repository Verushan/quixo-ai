#include "Board.h"
#include <iostream>
#include <vector>

using namespace std;

int main() {
    Board board("X3O/OOXX1/OOOXX/XO1XO/1O2X X 17");
    board.display();
    Move move(14, West);
    board.makeMove(move);
    board.display();
    return 0;
}