#include <stdio.h>

void showPrices(int prices[], int n) {
    printf("\nPrices:\n");
    for(int i = 0; i < n; i++)
        printf("%d ", prices[i]);
    printf("\n");
}

void drawGraphVisual(int prices[], int n) {
    printf("\n--- Price Visualization ---\n");

    for(int i = 0; i < n; i++) {
        printf("Day %d | ", i+1);
        for(int j = 0; j < prices[i]/10; j++)
            printf("*");
        printf(" (%d)\n", prices[i]);
    }
}

void showTransactions(int prices[], int n) {
    printf("\n--- Transactions ---\n");

    for(int i = 1; i < n; i++) {
        if(prices[i] > prices[i-1]) {
            printf("BUY Day %d (%d)\n", i, prices[i-1]);
            printf("SELL Day %d (%d)\n\n", i+1, prices[i]);
        }
    }
}

