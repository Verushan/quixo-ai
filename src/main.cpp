#include "Board.h"
#include <iostream>
#include <vector>

using namespace std;

int main() {
    string testFen = "X3O/OOXX1/OOOXX/XO1XO/1O2X X 17";
    Board board(testFen);
    board.display();
    return 0;
}