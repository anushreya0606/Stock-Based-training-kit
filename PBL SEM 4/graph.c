#include <stdio.h>

void buildGraph(int prices[], int n, int graph[100][100]) {
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < n; j++) {
            if(j > i)
                graph[i][j] = prices[j] - prices[i];
            else
                graph[i][j] = 0;
        }
    }
}

void displayGraph(int graph[100][100], int n) {
    printf("\n--- Graph (Profit Matrix) ---\n");
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < n; j++)
            printf("%4d ", graph[i][j]);
        printf("\n");
    }
}

int maxProfitGraph(int graph[100][100], int n) {
    int max = 0;

    for(int i = 0; i < n; i++) {
        for(int j = i+1; j < n; j++) {
            if(graph[i][j] > max)
                max = graph[i][j];
        }
    }

    return max;
}