#include <iostream>
#include "hello.h"

int main() {
    const std::string filename = "helloworld/hello.txt";
    std::string content = read_file(filename);
    if (!content.empty()) {
        std::cout << content << std::endl;
    }
    return 0;
}
