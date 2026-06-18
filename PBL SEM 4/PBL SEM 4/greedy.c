#define PLATFORM_FEE 10.0
#define TAX_RATE 0.15

int greedyProfit(int prices[], int n) {
    double totalProfit = 0.0;

    for(int i = 1; i < n; i++) {
        if(prices[i] > prices[i-1]) {
            // Calculate the result of the trade
            double grossTxProfit = (prices[i] - PLATFORM_FEE) - (prices[i-1] + PLATFORM_FEE);
            if(grossTxProfit > 0) {
                double tax = grossTxProfit * TAX_RATE;
                totalProfit += (grossTxProfit - tax);
            } else {
                // If the trade lost money to fees, subtract it from total profit
                totalProfit += grossTxProfit; 
            }
        }
    }
    return (int)totalProfit;
}