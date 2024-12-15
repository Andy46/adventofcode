#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cmath>
#include <regex>
#include <algorithm>

struct Button {
    std::vector<int> moves;
    int tokens;
};

struct Machine {
    std::vector<Button> buttons;
    std::vector<int> prize;
};

// Funciones auxiliares
bool achievedPrize(const std::vector<int>& pos, const std::vector<int>& prize) {
    return std::equal(pos.begin(), pos.end(), prize.begin());
}

bool overflowPrize(const std::vector<int>& pos, const std::vector<int>& prize) {
    return std::any_of(pos.begin(), pos.end(), [&prize, i = 0](int x) mutable {
        return x > prize[i++];
    });
}

int determineMinimumTokens(const Button& buttonA, const Button& buttonB, const std::vector<int>& prize) {
    std::vector<std::pair<int, int>> combinations;
    std::vector<int> posA(2, 0);
    int countA = 0;

    // Calcular todas las combinaciones posibles
    while (!overflowPrize(posA, prize) && !achievedPrize(posA, prize)) {
        std::vector<int> leftForB(2);
        std::transform(prize.begin(), prize.end(), posA.begin(), leftForB.begin(), std::minus<int>());

        std::vector<double> dividedB(2);
        std::transform(leftForB.begin(), leftForB.end(), buttonB.moves.begin(), dividedB.begin(), [](int a, int b) {
            return b != 0 ? static_cast<double>(a) / b : 0.0;
        });

        std::vector<double> modedB(2);
        std::transform(dividedB.begin(), dividedB.end(), buttonB.moves.begin(), modedB.begin(), [](double x, int) {
            return std::fmod(x, 1.0);
        });

        if (std::all_of(modedB.begin(), modedB.end(), [](double x) { return x == 0.0; }) && dividedB[0] == dividedB[1]) {
            combinations.emplace_back(countA, static_cast<int>(dividedB[0]));
        }

        std::transform(posA.begin(), posA.end(), buttonA.moves.begin(), posA.begin(), std::plus<int>());
        ++countA;
    }

    // Agregar combinación final si se logra el premio
    if (achievedPrize(posA, prize)) {
        combinations.emplace_back(countA, 0);
    }

    // Calcular los tokens para cada combinación
    std::vector<int> combinationsTokens;
    for (const auto& [countA, countB] : combinations) {
        combinationsTokens.push_back(buttonA.tokens * countA + buttonB.tokens * countB);
    }

    // Obtener el mínimo número de tokens
    return !combinationsTokens.empty() ? *std::min_element(combinationsTokens.begin(), combinationsTokens.end()) : 0;
}

int main() {
    std::string filepath = "00_test.data"; // Cambiar al archivo correspondiente
    std::ifstream file(filepath);

    if (!file.is_open()) {
        std::cerr << "No se pudo abrir el archivo: " << filepath << std::endl;
        return 1;
    }

    std::vector<Machine> initialData;
    std::string line;

    Machine machine;
    std::vector<Button> buttons;

    std::cout << "Reading data..." << std::endl;
    while (std::getline(file, line)) {
        line.erase(std::remove(line.begin(), line.end(), '\n'), line.end());
        
        if (line.find("Button") != std::string::npos) {
            Button newButton;
            std::smatch match;
            std::regex nameRegex("Button (.*):");
            std::regex movesRegex("(.\\+\\d+)");

            if (std::regex_search(line, match, nameRegex)) {
                std::string name = match[1];
                if (name == "A") {
                    newButton.tokens = 3;
                } else if (name == "B") {
                    newButton.tokens = 1;
                }

                std::sregex_iterator it(line.begin(), line.end(), movesRegex);
                std::sregex_iterator end;
                while (it != end) {
                    std::string move = (*it).str();
                    newButton.moves.push_back(std::stoi(move.substr(2))); // Ignorar el signo
                    ++it;
                }
                buttons.push_back(newButton);
            }
        } else if (line.find("Prize") != std::string::npos) {
            std::vector<int> prize;
            std::smatch match;
            std::regex locRegex("(.=\\d+)");

            std::sregex_iterator it(line.begin(), line.end(), locRegex);
            std::sregex_iterator end;
            while (it != end) {
                std::string loc = (*it).str();
                prize.push_back(std::stoi(loc.substr(2)) + 10000000000000);
                ++it;
            }

            machine.buttons = buttons;
            machine.prize = prize;
            initialData.push_back(machine);

            machine = Machine();
            buttons.clear();
        }
    }

    file.close();

    int totalTokens = 0;

    std::cout << "Calculating machines..." << std::endl;
    int id = 0;
    int machineCount = initialData.size();
    for (const auto& machine : initialData) {
        id++;
        std::cout << "Machine " << id << "/" << machineCount << "..." << std::endl;
        const auto& buttons = machine.buttons;
        const auto& prize = machine.prize;
        totalTokens += determineMinimumTokens(buttons[0], buttons[1], prize);
    }

    std::cout << "Total tokens: " << totalTokens << std::endl;

    return 0;
}
