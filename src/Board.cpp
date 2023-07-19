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
            mBoard[rank * BOARD_DIM + file] = X;
            break;

        case 'O':
            mBoard[rank * BOARD_DIM + file] = O;
            break;

        default:
            mBoard[rank * BOARD_DIM + file] = EMPTY;
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
            mValidDirections[index].push_back(row == 0 ? North : South);

            if (col > 0 && col < BOARD_DIM - 1) {
                mValidDirections[index].push_back(East);
                mValidDirections[index].push_back(West);
            } else {
                mValidDirections[index].push_back(col == 0 ? East : West);
            }

        } else {
            mValidDirections[index].push_back(col == 0 ? East : West);

            if (row > 0 && row < BOARD_DIM - 1) {
                mValidDirections[index].push_back(North);
                mValidDirections[index].push_back(South);
            } else {
                mValidDirections[index].push_back(row == 0 ? North : South);
            }
        }

        ++index;
    }
}

std::vector<Move> Board::generateValidMoves() {
    std::vector<Move> moves;
    int index = 0;

    for (int indice : OUTER_INDICES) {
        if (mBoard[indice] == mSideToPlay || mBoard[indice] == EMPTY) {
            for (Direction dir : mValidDirections[index]) {
                moves.emplace_back(Move(indice, dir));
            }
        }

        ++index;
    }

    return moves;
}

void Board::makeMove(const Move &move) {
    int start = move.getStartSquare();
    int end = 0, step = 0;

    Piece movingPiece = mBoard[start];
    Direction movingDirection = move.getDirection();

    printf("Piece at row %d col %d moving ", start / BOARD_DIM,
           start % BOARD_DIM);

    switch (movingDirection) {
    case North:
        step = BOARD_DIM;
        end = NORTH_ROW_START_INDEX + start % BOARD_DIM;
        printf("North\n");
        break;
    case South:
        step = BOARD_DIM;
        end = SOUTH_ROW_START_INDEX + start % BOARD_DIM;
        printf("South\n");
        break;
    case East:
        step = 1;
        end = EAST_ROW_START_INDEX + start / BOARD_DIM * BOARD_DIM;
        printf("East\n");
        break;
    case West:
        step = 1;
        end = WEST_ROW_START_INDEX + start / BOARD_DIM * BOARD_DIM;
        printf("West\n");
        break;
    }

    if (movingDirection == North || movingDirection == East) {
        for (int i = start; i < end; i += step) {
            mBoard[i] = mBoard[i + step];
        }
    } else {
        for (int i = start; i > end; i -= step) {
            mBoard[i] = mBoard[i - step];
        }
    }

    if (movingPiece == EMPTY) {
        movingPiece = mSideToPlay;
    }

    mSideToPlay = (mSideToPlay == X ? O : X);
    ++mMoveCount;

    mBoard[end] = movingPiece;
}

void Board::printValidMoves() {
    std::vector<Move> moves = generateValidMoves();
    std::vector<std::vector<std::string>> output(
        BOARD_DIM, std::vector<std::string>(BOARD_DIM));

    for (auto move : moves) {
        int startSquare = move.getStartSquare();
        Direction direction = move.getDirection();

        int row = startSquare / BOARD_DIM;
        int col = startSquare % BOARD_DIM;

        switch (direction) {
        case North:
            output[row][col] += "N";
            break;
        case South:
            output[row][col] += "S";
            break;
        case East:
            output[row][col] += "E";
            break;
        case West:
            output[row][col] += "W";
            break;
        }
    }

    for (int i = BOARD_DIM - 1; i >= 0; --i) {
        for (int j = 0; j < BOARD_DIM; ++j) {
            std::string value = output[i][j];

            while (value.length() < 3) {
                value += "_";
            }

            std::cout << value << " ";
        }

        std::cout << "\n";
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