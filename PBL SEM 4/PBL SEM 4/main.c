#include <stdio.h>

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

#define MAX 100

int main() {
    int prices[MAX], n;
    int graph[MAX][MAX];
    int gProfit, dProfit, graphProfit;
    int choice, algoChoice;

    printf("==== STOCK BUY-SELL ANALYZER ====\n");

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

        
        while(1) {
            printf("\n--- CURRENT DATA ---\n");
            showPrices(prices, n);
            drawGraphVisual(prices, n);

            buildGraph(prices, n, graph);
            displayGraph(graph, n);

            printf("\nChoose Trading Mode:\n");
            printf("1. Single Transaction (DP)\n");
            printf("2. Multiple Transactions (Greedy)\n");
            printf("3. Compare Both\n");
            printf("4. Change Dataset\n");
            printf("5. Exit Program\n");
            printf("Enter choice: ");
            scanf("%d", &algoChoice);

            if(algoChoice == 1) {
                dProfit = dpProfit(prices, n);
                printf("\nMax Profit (Single Transaction - DP): %d\n", dProfit);
            }
            else if(algoChoice == 2) {
                gProfit = greedyProfit(prices, n);
                printf("\nMax Profit (Multiple Transactions - Greedy): %d\n", gProfit);
                showTransactions(prices, n);
            }
            else if(algoChoice == 3) {
                gProfit = greedyProfit(prices, n);
                dProfit = dpProfit(prices, n);

                printf("\nGreedy Profit: %d\n", gProfit);
                printf("DP Profit: %d\n", dProfit);

                compareAlgorithms(gProfit, dProfit);
                saveResults(gProfit, dProfit);
            }
            else if(algoChoice == 4) {
                break; 
            }
            else if(algoChoice == 5) {
                printf("Exiting Program...\n");
                return 0;
            }
            else {
                printf("Invalid choice!\n");
            }

            
            graphProfit = maxProfitGraph(graph, n);
            printf("Graph-based Max Profit: %d\n", graphProfit);
        }
    }

    return 0;
}