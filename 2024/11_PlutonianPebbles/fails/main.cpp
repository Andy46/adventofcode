#include <vector>
#include <string>
#include <iostream>

typedef std::vector<uint64_t> vector_t;

vector_t readData(std::string filename)
{
    return vector_t ({125, 17});
}

vector_t blink(uint64_t pebble)
{
    if (pebble == 0)
    {
        return vector_t({1});
    }
    else 
    {
        std::string str {std::to_string(pebble)};
        if (str.length() % 2 == 0)
        {
            auto pebble_A = str.substr(0, str.length()/2);
            auto pebble_B = str.substr(str.length()/2);
            return vector_t({std::stoul(pebble_A), std::stoul(pebble_B)});
        }
        else
        {
            return vector_t({pebble*2024});
        }
    }
}


void calcPebbles(vector_t& initial, vector_t& final)
{
    final.clear();
    for (const auto& pebble : initial)
    {
        auto newPebbles = blink(pebble);
        final.insert(std::end(final), std::begin(newPebbles), std::end(newPebbles));        
    }
    // for (const auto& pebble : final)
    // {
    //     std::cout << pebble << std::endl;
    // }
}

int main()
{
    vector_t initialPebbles {readData("00_example1.data")};

    vector_t finalPebbles;
    finalPebbles.reserve(1000000);

    // std::vector<>
    for (int i=0; i<50; i++)
    {
        std::cout << "Iteration" << i << ": ";
        if (i%2 == 0)
        {
            calcPebbles(initialPebbles, finalPebbles);
            std::cout << ": "  << finalPebbles.size();
        }
        else
        {
            calcPebbles(finalPebbles, initialPebbles);
            std::cout << ": "  << initialPebbles.size();
        }
        std::cout << std::endl;
    }

    return 0;
}