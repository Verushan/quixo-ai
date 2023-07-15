# Compiler
CXX = g++

# Compiler flags
CXXFLAGS = -std=c++11 -Wall -Wextra

# Include directory
INCLUDES = -Iinclude

# Source files directory
SRC_DIR = src

# Source files
SRCS = $(wildcard $(SRC_DIR)/*.cpp)

# Object files directory
OBJ_DIR = obj

# Object files
OBJS = $(patsubst $(SRC_DIR)/%.cpp, $(OBJ_DIR)/%.o, $(SRCS))

# Executable file name
EXECUTABLE = program

# Default rule
all: $(EXECUTABLE)

# Linking object files to generate the executable
$(EXECUTABLE): $(OBJS)
	$(CXX) $(CXXFLAGS) $(OBJS) -o $@

# Compile source files into object files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

# Clean the generated files
clean:
	rm -rf $(OBJ_DIR)/*.o $(EXECUTABLE)
