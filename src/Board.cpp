#include "Board.h"
#include <sstream>

const std::string Board::STARTING_FEN = "5/5/5/5/5 X 0";

const int Board::OUTER_INDICES[Board::NUM_OUTER_INDICES] = {
    0, 1, 2, 3, 4, 9, 14, 19, 24, 23, 22, 21, 20, 15, 10, 5};

std::vector<Direction> Board::mValidDirections[Board::NUM_OUTER_INDICES];

Board::Board() { mBoard = std::vector<Piece>(BOARD_LENGTH, Piece::EMPTY); }

Board::Board(const std::string &fen) : Board() {
    std::stringstream fenParts(fen);
    std::string sBoard;

    fenParts >> sBoard;

    std::string sSideToPlay;
    fenParts >> sSideToPlay;

    mSideToPlay = (sSideToPlay == "X" ? X : O);

    std::string sMoveCount;
    fenParts >> sMoveCount;

    mMoveCount = std::stoi(sMoveCount);

    int file = 0;
    int rank = BOARD_DIM - 1;

    for (char c : sBoard) {
        if (c == '/') {
            file = 0;
            --rank;
            continue;
        }

        if ('1' <= c && c <= '5') {
            file += (c - '0');
            continue;
        }

        switch (c) {
        case 'X':
            mBoard[rank * BOARD_DIM + file] = Piece::X;
            break;

        case 'O':
            mBoard[rank * BOARD_DIM + file] = Piece::O;
            break;

        default:
            mBoard[rank * BOARD_DIM + file] = Piece::EMPTY;
        }

        ++file;
    }
}

std::vector<Move> Board::generateMoves() {
    std::vector<Move> moves;

    for (int indice : OUTER_INDICES) {
        if (mBoard[indice] == mSideToPlay || mBoard[indice] == EMPTY) {
        }
    }

    return moves;
}

void Board::display() {
    for (int i = BOARD_DIM - 1; i >= 0; --i) {
        for (int j = 0; j < BOARD_DIM; ++j) {
            Piece piece = mBoard[i * BOARD_DIM + j];

            if (piece == Piece::X) {
                printf("X ");
            } else if (piece == Piece::O) {
                printf("O ");
            } else {
                printf("_ ");
            }
        }

        printf("\n");
    }

    printf("Move count: %d\n", mMoveCount);

    if (mSideToPlay == X) {
        printf("Side to play: X\n");
    } else {
        printf("Side to play: O\n");
    }
}