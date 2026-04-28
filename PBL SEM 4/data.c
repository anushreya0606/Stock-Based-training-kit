#include <stdio.h>

// -------- SAMPLE DATA --------
void loadSampleData(int prices[], int *n) {
    int choice;

    while(1) {
        printf("\nSelect Sample Dataset:\n");
        printf("1. Increasing Prices (Bull Market)\n");
        printf("2. Decreasing Prices (Bear Market)\n");
        printf("3. Fluctuating Prices\n");
        printf("4. Random Mixed Data\n");
        printf("5. Small Dataset\n");
        printf("Enter choice: ");
        scanf("%d", &choice);

        switch(choice) {
            case 1: {
                int sample[] = {100,150,200,250,300,350};
                *n = 6;
                for(int i=0;i<*n;i++) prices[i]=sample[i];
                break;
            }
            case 2: {
                int sample[] = {300,250,200,150,100};
                *n = 5;
                for(int i=0;i<*n;i++) prices[i]=sample[i];
                break;
            }
            case 3: {
                int sample[] = {100,180,260,310,40,535,695};
                *n = 7;
                for(int i=0;i<*n;i++) prices[i]=sample[i];
                break;
            }
            case 4: {
                int sample[] = {120,90,150,80,200,50,300};
                *n = 7;
                for(int i=0;i<*n;i++) prices[i]=sample[i];
                break;
            }
            case 5: {
                int sample[] = {100,110,90,120};
                *n = 4;
                for(int i=0;i<*n;i++) prices[i]=sample[i];
                break;
            }
            default:
                printf("Invalid choice!\n");
                continue;
        }
        break;
    }
}

// -------- USER INPUT --------
void inputData(int prices[], int *n) {
    printf("Enter number of days: ");
    scanf("%d", n);

    printf("Enter prices:\n");
    for(int i = 0; i < *n; i++) {
        scanf("%d", &prices[i]);
    }
}

// -------- FILE INPUT --------
void loadFromFile(int prices[], int *n) {
    FILE *fp = fopen("prices.txt", "r");

    if(fp == NULL) {
        printf("Error opening file!\n");
        return;
    }

    *n = 0;
    while(fscanf(fp, "%d", &prices[*n]) != EOF) {
        (*n)++;
    }

    fclose(fp);

    printf("Data loaded from file successfully!\n");
}