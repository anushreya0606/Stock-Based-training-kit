#include <stdio.h>

void saveResults(int greedy, int dp) {
    FILE *fp = fopen("result.txt", "w");

    if(fp == NULL) {
        printf("File error!\n");
        return;
    }

    fprintf(fp, "Greedy Profit: %d\n", greedy);
    fprintf(fp, "DP Profit: %d\n", dp);

    fclose(fp);
}