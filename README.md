# Task2-OKLink

## Adjust These Variable

TOKEN_ADDRESS = "TOKEN_ADDRESS"  # Replace with token address that you want to research

OK_ACCESS_KEY = "YOUR_OKLinkAPIKey"  # Replace with your OKLink access key

token_decimal = 18 #Adjust Token's Decimal

## Researched Tokens

BlockGames(BLOCK - 0x8fc17671d853341d9e8b001f5fc3c892d09cb53a) - Reason to choose this because selected by Google to join its exclusive Web3 startup program.

JC Coin(JCC - 0x03a9d7c8caf836de35666c5f7e317306b54fdd4e) - Good Performance in past few days

Open GPU(oGPU - 0x067def80d66fb69c276e53b641f37ff7525162f6) - Demand for cloud computing and GPU resources continues to rise, positioning oGPU within a potentially lucrative market.

## Analysis Approach

Token Research:

Basic Information: The token_info() function fetches fundamental token details like name, symbol, website, Twitter, and whitepaper. These form the basis for understanding the project behind the token.
   
Price Analysis:

Historical Price Data: The token_price_data() function retrieves past price information. This is presented in a table (using PrettyTable) to potentially visualize trends, volatility, or price anomalies.

Distribution Analysis:

Token Holders: The fetch_holding_data() function analyzes how the token supply is distributed. It lists holders by address, quantity held, and the proportion of the total supply they control. Understanding concentrated holdings is crucial for market analysis.

Liquidity Analysis:

Trading Activity: The fetch_liquidity_data() function looks at the token's overall trading activity. 24-hour transaction count and trading volume offer indicators of the token's liquidity.

Large Transaction Analysis:

Whale Tracking: The fetch_token_large_tx() function specifically focuses on transactions exceeding a significant threshold. This highlights potential 'whale' activity that might heavily influence the token's price.
