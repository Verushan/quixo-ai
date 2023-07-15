#include "Board.h"
#include <iostream>
#include <sstream>

const std::string Board::STARTING_FEN = "5/5/5/5/5 X 0";

const int Board::OUTER_INDICES[Board::NUM_OUTER_INDICES] = {
    0, 1, 2, 3, 4, 9, 14, 19, 24, 23, 22, 21, 20, 15, 10, 5};

std::vector<Direction> Board::mValidDirections[Board::NUM_OUTER_INDICES];

Board::Board() {
    mBoard = std::vector<Piece>(BOARD_LENGTH, EMPTY);
    precomputeDirections();
    loadBoardAsFen(STARTING_FEN);
}

Board::Board(const std::string &fen) : Board() { loadBoardAsFen(fen); }

void Board::loadBoardAsFen(const std::string &fen) {
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

void Board::precomputeDirections() {
    int index = 0;

    for (int indice : OUTER_INDICES) {
        int row = indice / BOARD_DIM;
        int col = indice % BOARD_DIM;

        if (row == 0 || row == BOARD_DIM - 1) {
            if (row == 0) {
                mValidDirections[index].push_back(North);
            } else {
                mValidDirections[index].push_back(South);
            }

            if (col > 0 && col < BOARD_DIM - 1) {
                mValidDirections[index].push_back(East);
                mValidDirections[index].push_back(West);
            } else if (col == 0) {
                mValidDirections[index].push_back(East);
            } else {
                mValidDirections[index].push_back(West);
            }
        } else {
            if (col == 0) {
                mValidDirections[index].push_back(East);
            } else {
                mValidDirections[index].push_back(West);
            }

            if (row > 0 && row < BOARD_DIM - 1) {
                mValidDirections[index].push_back(North);
                mValidDirections[index].push_back(South);
            } else if (row == 0) {
                mValidDirections[index].push_back(North);
            } else {
                mValidDirections[index].push_back(South);
            }
        }

        ++index;
    }
}

std::vector<Move> Board::generateMoves() {
    std::vector<Move> moves;
    int index = 0;

    for (int indice : OUTER_INDICES) {
        if (mBoard[indice] == mSideToPlay || mBoard[indice] == EMPTY) {
            for (Direction dir : mValidDirections[index++]) {
                moves.emplace_back(Move(indice, dir));
            }
        }
    }

    return moves;
}

void Board::printMoves() {
    std::vector<Move> moves = generateMoves();

    for (auto move : moves) {
        int row = move.startSquare / BOARD_DIM;
        int col = move.startSquare % BOARD_DIM;

        printf("{%d, %d} ->", row, col);

        switch (move.direction) {
        case North:
            printf("N\n");
            break;
        case South:
            printf("S\n");
            break;
        case East:
            printf("E\n");
            break;
        case West:
            printf("W\n");
            break;
        }
    }

    printf("Number of valid moves: %ld\n", moves.size());
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