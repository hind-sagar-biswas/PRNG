
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s n\n", argv[0]);
        return 1;
    }
    int n = atoi(argv[1]);
    srand(time(NULL));
    for (int i = 0; i < n; i++) {
        float num = (float)rand() / (float)RAND_MAX;
        printf("%f ", num);
    }
    printf("\n");
    return 0;
}
