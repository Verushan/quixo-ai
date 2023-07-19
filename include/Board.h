#include "Move.h"
#include "Piece.h"
#include <string>
#include <vector>

class Board {
  private:
    std::vector<Piece> mBoard;
    Piece mSideToPlay;
    int mMoveCount;

    const static int NUM_OUTER_INDICES = 16;
    const static int OUTER_INDICES[NUM_OUTER_INDICES];
    static std::vector<Direction> mValidDirections[NUM_OUTER_INDICES];

    void precomputeDirections();

  public:
    const static int BOARD_DIM = 5;

    const static int NORTH_ROW_START_INDEX = 20;
    const static int SOUTH_ROW_START_INDEX = 0;
    const static int EAST_ROW_START_INDEX = 4;
    const static int WEST_ROW_START_INDEX = 0;

    const static int BOARD_LENGTH = BOARD_DIM * BOARD_DIM;
    const static std::string STARTING_FEN;

    Board();

    Board(const std::string &fen);

    void loadBoardAsFen(const std::string &fen);

    std::vector<Move> generateValidMoves();

    void makeMove(const Move &move);

    void display();

    void printValidMoves();
};