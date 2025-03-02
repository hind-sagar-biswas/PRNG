
#include <iostream>
#include <cstdlib>
#include <ctime>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cout << "Usage: " << argv[0] << " n" << std::endl;
        return 1;
    }
    int n = std::atoi(argv[1]);
    std::srand(std::time(0));
    for (int i = 0; i < n; i++) {
        float num = static_cast<float>(std::rand()) / RAND_MAX;
        std::cout << num << " ";
    }
    std::cout << std::endl;
    return 0;
}
