#include <stdio.h>

// Global constants for real-world transaction friction
#define PLATFORM_FEE 10.0
#define TAX_RATE 0.15 // 15% Short-Term Capital Gains Tax (STCG)
#define MAX 100

// Function declarations (Updated to accept double for net calculations where necessary)
void loadSampleData(int prices[], int *n);
void inputData(int prices[], int *n);
void loadFromFile(int prices[], int *n);

int greedyProfit(int prices[], int n);
int dpProfit(int prices[], int n);

void showPrices(int prices[], int n);
void drawGraphVisual(int prices[], int n);
void showTransactions(int prices[], int n);

void buildGraph(int prices[], int n, int graph[100][100]);
void displayGraph(int graph[100][100], int n);
int maxProfitGraph(int graph[100][100], int n);

void compareAlgorithms(int greedy, int dp);
void saveResults(int greedy, int dp);

// New features for tax analysis
void calculateThreshold(int currentBuyPrice);

int main() {
    int prices[MAX], n;
    int graph[MAX][MAX];
    int gProfit, dProfit, graphProfit;
    int choice, algoChoice;

    printf("==== REAL-WORLD STOCK BUY-SELL ANALYZER ====\n");
    printf("     (Includes Platform Fees & Capital Gains Tax)\n");

    while(1) {
        // -------- DATASET MENU --------
        printf("\n1. Load Sample Data\n");
        printf("2. Enter Custom Data\n");
        printf("3. Load From File\n");
        printf("4. Exit\n");
        printf("Enter choice: ");
        scanf("%d", &choice);

        if(choice == 4) {
            printf("Exiting Program...\n");
            break;
        }

        if(choice == 1)
            loadSampleData(prices, &n);
        else if(choice == 2)
            inputData(prices, &n);
        else if(choice == 3)
            loadFromFile(prices, &n);
        else {
            printf("Invalid choice!\n");
            continue;
        }

        // -------- AFTER DATA LOAD --------
        while(1) {
            printf("\n--- CURRENT DATA ---\n");
            showPrices(prices, n);
            drawGraphVisual(prices, n);

            buildGraph(prices, n, graph);
            displayGraph(graph, n);

            printf("\nChoose Trading Mode:\n");
            printf("1. Single Transaction (DP) [Smart Multi-Tax Optimization]\n");
            printf("2. Multiple Transactions (Greedy) [Brute Force High-Friction]\n");
            printf("3. Compare Both & Run Risk Threshold Analysis\n");
            printf("4. Change Dataset\n");
            printf("5. Exit Program\n");
            printf("Enter choice: ");
            scanf("%d", &algoChoice);

            if(algoChoice == 1) {
                dProfit = dpProfit(prices, n);
                printf("\nMax Net Profit (Single Transaction - DP): %d INR\n", dProfit);
            }
            else if(algoChoice == 2) {
                gProfit = greedyProfit(prices, n);
                printf("\nMax Net Profit (Multiple Transactions - Greedy): %d INR\n", gProfit);
                showTransactions(prices, n);
            }
            else if(algoChoice == 3) {
                gProfit = greedyProfit(prices, n);
                dProfit = dpProfit(prices, n);

                printf("\nNet Greedy Profit (High Transaction Count): %d INR\n", gProfit);
                printf("Net DP Profit (Strategic Single Position): %d INR\n", dProfit);

                compareAlgorithms(gProfit, dProfit);
                saveResults(gProfit, dProfit);
                
                // Triggers threshold logic using the initial price step as baseline anchor
                calculateThreshold(prices[0]);
            }
            else if(algoChoice == 4) {
                break; // Go back to dataset menu
            }
            else if(algoChoice == 5) {
                printf("Exiting Program...\n");
                return 0;
            }
            else {
                printf("Invalid choice!\n");
            }

            // Graph-based calculation acts as a theoretical reference limit
            graphProfit = maxProfitGraph(graph, n);
            printf("Raw Graph-based Gross Max Profit (Before Taxes/Fees): %d\n", graphProfit);
        }
    }

    return 0;
}

// -------- GREEDY ALGORITHM (UPDATED) --------
// int greedyProfit(int prices[], int n) {
//     double totalProfit = 0.0;

//     for(int i = 1; i < n; i++) {
//         if(prices[i] > prices[i-1]) {
//             // Evaluates real-world entry costs vs platform exit deductions per individual cycle
//             double grossTxProfit = (prices[i] - PLATFORM_FEE) - (prices[i-1] + PLATFORM_FEE);
            
//             if(grossTxProfit > 0) {
//                 double tax = grossTxProfit * TAX_RATE;
//                 totalProfit += (grossTxProfit - tax);
//             }
//         }
//     }
//     return (int)totalProfit;
// }

// // -------- DP ALGORITHM (UPDATED) --------
// int dpProfit(int prices[], int n) {
//     double minBuyCost = prices[0] + PLATFORM_FEE; 
//     double maxNetProfit = 0.0;

//     for(int i = 1; i < n; i++) {
//         double grossSellValue = prices[i] - PLATFORM_FEE;
//         double currentGrossProfit = grossSellValue - minBuyCost;

//         if(currentGrossProfit > 0) {
//             double tax = currentGrossProfit * TAX_RATE;
//             double netProfit = currentGrossProfit - tax;
//             if(netProfit > maxNetProfit) {
//                 maxNetProfit = netProfit;
//             }
//         }

//         if((prices[i] + PLATFORM_FEE) < minBuyCost) {
//             minBuyCost = prices[i] + PLATFORM_FEE;
//         }
//     }
//     return (int)maxNetProfit;
// }

// -------- NEW FUNCTION: NET BREAKEVEN THRESHOLD --------
// void calculateThreshold(int currentBuyPrice) {
//     // Round-trip overhead (Buy platform fee + Sell platform fee)
//     double absoluteOverhead = 2 * PLATFORM_FEE; 
//     double netBreakevenPrice = currentBuyPrice + absoluteOverhead;

//     printf("\n=======================================================\n");
//     printf("   REAL-WORLD TRANSACTION FRICTION & BREAKEVEN MATRIX\n");
//     printf("=======================================================\n");
//     printf(" Baseline Purchase Entry  : %d INR\n", currentBuyPrice);
//     printf(" Structural Entry/Exit Fee: %.2f INR (Round-Trip)\n", absoluteOverhead);
//     printf(" Target Net Profit Line   : > %.2f INR\n\n", netBreakevenPrice);
//     printf(" STRATEGY VERDICT:\n");
//     printf(" * Stock price must expand by over %.2f INR just to cover overhead.\n", absoluteOverhead);
//     printf(" * High-frequency micro-trading (Greedy) will bleed performance into fee nodes.\n");
//     printf(" * Target Exit: Sell above %.2f INR for positive yield; cut loss early if asset slides.\n", netBreakevenPrice);
//     printf("=======================================================\n");
// }