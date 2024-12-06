#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <algorithm>
#include <set>
#include <tuple>

using namespace std;

/**
 * Note: This code was implemented using ChatGPT
 *   ChatGPT was used to convert the code in ../06_GuardValiant/main.py from python to C++,
 *   Only minor fixes were performed to ChatGPT output.
 */

// Tokens
const char PATH_TOKEN = 'X';
const char GUARD_TOKEN = '^';
const char OBSTACLE_TOKEN = '#';

// Tipos y funciones auxiliares
using Matrix = vector<vector<char>>;
using Position = pair<int, int>;

Position findGuard(const Matrix &data) {
    for (size_t x = 0; x < data.size(); ++x) {
        for (size_t y = 0; y < data[x].size(); ++y) {
            if (data[x][y] == GUARD_TOKEN) {
                return {x, y};
            }
        }
    }
    return {-1, -1}; // Guard not found
}

char getGuardToken(char dirToken) {
    switch (dirToken) {
        case 'n': return '^';
        case 'e': return '>';
        case 's': return 'v';
        case 'w': return '<';
    }
    return '^';
}

bool isObstacle(const Matrix &data, int x, int y) {
    return data[x][y] == OBSTACLE_TOKEN;
}

char rotate(char dirToken) {
    switch (dirToken) {
        case 'n': return 'e';
        case 'e': return 's';
        case 's': return 'w';
        case 'w': return 'n';
    }
    return 'n';
}

Position getNextCell(int x, int y, char dirToken) {
    if (dirToken == 'n') return {x - 1, y};
    if (dirToken == 'e') return {x, y + 1};
    if (dirToken == 's') return {x + 1, y};
    if (dirToken == 'w') return {x, y - 1};
    return {x, y};
}

bool isCellInData(const Matrix &data, size_t x, size_t y) {
    return x < data.size() && y < data[0].size();
}

void printMap(const Matrix &data) {
    for (const auto &line : data) {
        for (char cell : line) {
            cout << cell;
        }
        cout << endl;
    }
}

pair<Matrix, pair<Position, char>> move(Matrix data, pair<Position, char> guard) {
    auto [x, y] = guard.first;
    char dir = guard.second;

    // Calculate move
    Position nextCell = getNextCell(x, y, dir);
    while (isCellInData(data, nextCell.first, nextCell.second) && isObstacle(data, nextCell.first, nextCell.second)) {
        dir = rotate(dir);
        nextCell = getNextCell(x, y, dir);
    }

    guard = {nextCell, dir};

    // Rotate again if needed
    auto [xt, yt] = guard.first;
    dir = guard.second;
    nextCell = getNextCell(xt, yt, dir);
    while (isCellInData(data, nextCell.first, nextCell.second) && isObstacle(data, nextCell.first, nextCell.second)) {
        dir = rotate(dir);
        nextCell = getNextCell(xt, yt, dir);
    }

    guard.second = dir;

    // Edit MAP
    data[x][y] = PATH_TOKEN;
    if (isCellInData(data, guard.first.first, guard.first.second)) {
        data[guard.first.first][guard.first.second] = getGuardToken(dir);
    }

    return {data, guard};
}

Matrix addObstacle(Matrix data, Position pos) {
    data[pos.first][pos.second] = OBSTACLE_TOKEN;
    return data;
}

bool hasLoop(Matrix data, pair<Position, char> guard) {
    set<pair<Position, char>> history;
    while (isCellInData(data, guard.first.first, guard.first.second)) {
        if (history.count(guard)) {
            return true; // Loop detected
        }
        history.insert(guard);
        tie(data, guard) = move(data, guard);
    }
    return false;
}

int main() {
    // Leer archivo
    string filepath = "00_test.data";
    Matrix initialData;

    ifstream file(filepath);
    if (!file.is_open()) {
        cerr << "Error opening file: " << filepath << endl;
        return 1;
    }

    string line;
    while (getline(file, line)) {
        vector<char> row(line.begin(), line.end());
        initialData.push_back(row);
    }
    file.close();

    // Parte 1: Calcular ruta
    bool PRINT_MAP = false;
    Matrix data = initialData;

    auto guard = make_pair(findGuard(data), 'n');
    cout << "Initial position: (" << guard.first.first << ", " << guard.first.second << "), dir: " << guard.second << endl;

    vector<pair<Position, char>> MainHistory = {guard};

    while (isCellInData(data, guard.first.first, guard.first.second)) {
        if (PRINT_MAP) {
            cout << "Current Map:" << endl;
            printMap(data);
        }
        tie(data, guard) = move(data, guard);
        MainHistory.push_back(guard);
    }

    if (PRINT_MAP) {
        cout << "Final Map:" << endl;
        printMap(data);
    }

    // Calcular posiciones
    int posCount = 0;
    for (const auto &row : data) {
        posCount += count(row.begin(), row.end(), PATH_TOKEN);
    }

    cout << "Guard travelled through " << posCount << " positions." << endl;

    // Parte 2: Detectar bucles
    data = initialData;
    vector<Position> loopPositions;
    loopPositions.reserve(MainHistory.size());
    set<Position> duplicatedPositions;

    auto initialGuard = make_pair(findGuard(data), 'n');

    for (const auto &guardPos : MainHistory) {
        Position nextCell = getNextCell(guardPos.first.first, guardPos.first.second, guardPos.second);
        if (duplicatedPositions.count(nextCell)) {
            continue;
        }
        if (isCellInData(data, nextCell.first, nextCell.second) && !duplicatedPositions.count(nextCell)) {
            Matrix newData = addObstacle(initialData, nextCell);
            if (hasLoop(newData, initialGuard)) {
                loopPositions.push_back(nextCell);
                duplicatedPositions.insert(nextCell);
            }
        }
    }

    cout << "Obstacle positions for loop: " << loopPositions.size() << endl;
    return 0;
}
