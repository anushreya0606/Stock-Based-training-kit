#include <stdio.h>

void compareAlgorithms(int greedy, int dp) {
    printf("\n--- Comparison ---\n");

    if(greedy > dp)
        printf("Greedy gives higher profit\n");
    else if(dp > greedy)
        printf("DP gives higher profit\n");
    else
        printf("Both give same profit\n");
}