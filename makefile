CXX = g++

CXXFLAGS = -std=c++11 -Wall -Wextra

INCLUDES = -Iinclude

SRC_DIR = src

SRCS = $(wildcard $(SRC_DIR)/*.cpp)

OBJ_DIR = obj

OBJS = $(patsubst $(SRC_DIR)/%.cpp, $(OBJ_DIR)/%.o, $(SRCS))

EXECUTABLE = main

all: $(EXECUTABLE)

$(EXECUTABLE): $(OBJS)
	$(CXX) $(CXXFLAGS) $(OBJS) -o $@

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

clean:
	rm -rf $(OBJ_DIR)/*.o $(EXECUTABLE)

.PHONY: all create_directories clean