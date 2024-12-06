## This makefile was produced using ChatGPT

# Nombre del ejecutable
TARGET = guard_path

# Compilador
CXX = g++

# Flags de compilación
CXXFLAGS = -std=c++17 -Wall -Wextra -O2

# Archivos fuente y objeto
SRC = main.cpp
OBJ = $(SRC:.cpp=.o)

# Regla principal
all: $(TARGET)

# Regla para compilar el ejecutable
$(TARGET): $(OBJ)
	$(CXX) $(CXXFLAGS) -o $@ $^

# Regla para compilar los archivos fuente en objetos
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Limpiar los archivos generados
clean:
	rm -f $(OBJ) $(TARGET)

# Ejecutar el programa
run: $(TARGET)
	./$(TARGET)
