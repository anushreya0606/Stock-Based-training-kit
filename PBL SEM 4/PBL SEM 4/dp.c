#define PLATFORM_FEE 10.0
#define TAX_RATE 0.15

int dpProfit(int prices[], int n) {
    double minBuyCost = prices[0] + PLATFORM_FEE; 
    double maxNetProfit = 0.0;

    for(int i = 1; i < n; i++) {
        // Net value if we sell today
        double grossSellValue = prices[i] - PLATFORM_FEE;
        double currentGrossProfit = grossSellValue - minBuyCost;

        if(currentGrossProfit > 0) {
            double tax = currentGrossProfit * TAX_RATE;
            double netProfit = currentGrossProfit - tax;
            if(netProfit > maxNetProfit) {
                maxNetProfit = netProfit;
            }
        }

        // Keep track of the lowest buying entry point cost
        if((prices[i] + PLATFORM_FEE) < minBuyCost) {
            minBuyCost = prices[i] + PLATFORM_FEE;
        }
    }

    return (int)maxNetProfit;
}