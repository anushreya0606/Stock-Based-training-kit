#include <stdio.h>

#define PLATFORM_FEE 10.0

// Handles the comparison option
void compareAlgorithms(int greedy, int dp) {
    printf("\n--- Comparison ---\n");

    if(greedy > dp)
        printf("Greedy gives higher profit\n");
    else if(dp > greedy)
        printf("DP gives higher profit\n");
    else
        printf("Both give same profit\n");
}

// Handles the threshold option
void calculateThreshold(int currentBuyPrice) {
    double absoluteOverhead = 2 * PLATFORM_FEE; 
    double netBreakevenPrice = currentBuyPrice + absoluteOverhead;

    printf("\n=======================================================\n");
    printf("   REAL-WORLD TRANSACTION FRICTION & BREAKEVEN MATRIX\n");
    printf("=======================================================\n");
    printf(" Baseline Purchase Entry  : %d INR\n", currentBuyPrice);
    printf(" Structural Entry/Exit Fee: %.2f INR (Round-Trip)\n", absoluteOverhead);
    printf(" Target Net Profit Line   : > %.2f INR\n\n", netBreakevenPrice);
    printf(" STRATEGY VERDICT:\n");
    printf(" * Stock price must expand by over %.2f INR just to cover overhead.\n", absoluteOverhead);
    printf(" * High-frequency micro-trading (Greedy) will bleed performance into fee nodes.\n");
    printf(" * Target Exit: Sell above %.2f INR for positive yield; cut loss early if asset slides.\n", netBreakevenPrice);
    printf("=======================================================\n");
}