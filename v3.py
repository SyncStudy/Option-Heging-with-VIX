# The investment universe consists of a stock/bond portfolio with a proportion of 60-percent stocks and 40-percent bonds.
# Stocks are represented by the SPDR S&P 500 ETF Trust (SPY) and bonds by the iShares 7-10 Year Treasury Bond ETF (IEF). 
# The strategy firstly invests 0-100 basis points (bsp) in the desired VIX call option, then allocates 60 percent of the 
# portfolio to the SPY and the remaining 40 percent to the IEF. The option is bought at the level of 135% of the moneyness
# of the underlying VIX futures price. The strategy is systematically purchasing an equal amount in one-month, two-month, 
# three-month and four-month VIX call options on VIX futures. If the VIX Index is between 15 and 30, the weight of VIX calls 
# in the portfolio is 1%. If the VIX Index is between 30 and 50, the weight in the portfolio is 0,5%. If the VIX Index is over
# 50 or under 15, then the weight of options in the portfolio is 0%. Each month, on the day before expiration, the options are
# rolled to the appropriate expiry. VIX call options are purchased at the offer and sold at the bid to keep the assumptions
# conservative. The options are held to maturity and closed the Tuesday afternoon before the Wednesday morning of VIX futures
# and options expiration. If the contracts have any intrinsic value, they are sold at the bid price, and the cash is used at 
# the end of the month to rebalance the stock/bond portion of the portfolio.

# Advice:
#   - To view algorithm errors, toggle Console view below when in Backtesting
#   - To print out debugging messages (the difference is only in colours), use
#     `self.Debug(...)` or `self.Error(...)` - See LINK 1
#   - To stop backtesting, go to Organisation (tab #2) -> Resources -> Stop

from AlgorithmImports import *

class PortfolioHedgingUsingVIXOptions(QCAlgorithm):

    def Initialize(self):
        # TODO 1: (LINK 2)
        # Set up conditions:
        #   - cash (1000000)
        #   - start date (1/1/2010)
        
        self.SetStartDate(2010,1,1)
        self.SetCash(1000000)
        
        # TODO 2: (API)
        # Set up holdings:
        #   - on S&P ("SPY")
        #   - with minutely resolution
        #   - with leverage of 5 (LINK 3)
        # Do the same for IEF(bond)
        # Links: _1_ _2_
        
        data = self.AddEquity("SPY",Resolution.Minute)
        data.SetLeverage(5)
        self.spy = data.Symbol
        
        data = self.AddEquity("IEF",Resolution.Minute)
        data.SetLeverage(5)
        self.ief = data.Symbol 
        
        # TODO 3: Add VIX options with option filter(LINK4, ~5 lines)
        #   - Use ticker 'VIXY' for both options and VIX
        #   - For VIX itself, set leverage for it to 5, and save it as self.vix.
        #   - Minute resolution
        #   - Option filter: minStrike = -20, maxStrike = 20, minExpiry = 25, maxExpiry = 35
        
        # data =self.AddOption("VIXY",Resolution.Minute)
        data =self.AddEquity("VIXY",Resolution.Minute)
        data.SetLeverage(5)
        self.vix = data.Symbol
        
        option=self.AddOption("VIXY",Resolution.Minute)
        #option.SetFilter(minStrike = -20, maxStrike = 20, minExpiry = 25, maxExpiry = 35)
        option.SetFilter(-20,20,25,35)

        
    def OnData(self,slice):
        for i in slice.OptionChains:
            chains = i.Value

            # invested is a list of all instruments that the strategy is currently invested in.
            invested = [x.Key for x in self.Portfolio if x.Value.Invested]
            
            # TODO 4: Write a code to check if you hold options or not (~ 2 more lines)
            #   - hint: having a maximum of 2 positions means SPY and IEF are opened, which means options expired.??
            #   - If you do not , this means the current option holdings have expired.
            #   - In this case, get the list of all eligible call options. If none, return.
            #   - LINK 5
            # if len(invested) <= 2:
            #     # return invested
            #     # calls = 
            #     call = [x for x in chain if x.Right == OptionRight.Call] #??
            # # call = [x for x in chain if x.Right == OptionRight.Call]


            if len(invested) <= 2:
            # No options are currently held; look for eligible call options
                eligible_calls = []
                calls= list(filter(lambda x: x.Right == OptionRight.Call,chains))
                if not calls: return
            #???

            # Loop through the option chain
            for option in chains:
                # Check for call options
                if option.Right == OptionRight.Call:
                    # Add eligible call options to the list
                    # You can add more criteria here to filter for 'eligible' options
                    eligible_calls.append(option)

            # If there are no eligible call options, return
            if not eligible_calls:
                return
            #??
                # OptionChains.get(self.option_symbol)
            ## else: 

                
                # TODO 5: Execute strategy (~12 lines)
                #   (1) Gets options underlying price + expiries + strike price
                #   (2) Filter according to expiry date(closest to 1 month, 2 month, 3 month, 4 month)
                #   (3) Further filter out OTM options with level of moneyness closest to 135% of underlying(VIX)
                #   (4) Calculate weighting of the call options based on underlying:
                #           - 1% if underlying belongs to [15,30]
                #           - 0.5% if underlying belongs to [30,50]
                #           - 0 otherwise

                # Gets options underlying price + expiries + strike price
                underlying_price = self.Securities[self.vix].Price
                expiries = [i.Expiry for i in calls]
                strikes = [i.Strike for i in calls]


                # # for optionContract in chain:
                #     # Add the expiry date of the option to our list
                #     expiries.append(optionContract.Expiry)

                #     # Add the strike price of the option to our list
                #     strikes.append(optionContract.Strike)
                # # Filter according to expiry date(closest to 1 month, 2 month, 3 month, 4 month)


                # Determine out-of-the-money strike.
                # Further filter out OTM options with level of moneyness closest to 135% of underlying(VIX)
                otm_strike = min(strikes, key = lambda x:abs(x - (float(1.35) * underlying_price)))

                # Option weighting.
                 #   (4) Calculate weighting of the call options based on underlying:
                #           - 1% if underlying belongs to [15,30]
                #           - 0.5% if underlying belongs to [30,50]
                #           - 0 otherwise

                # if 15 <= underlying_price <= 30:
                #     weight = 0.01
                # elif 30 < underlying_price <= 50:
                #     weight = 0.005
                # else:
                #     weight = 0
                # weight = 
                # 

                weight=0.0
                options_q=0

                if 15 <= underlying_price <= 30:
                    weight = 0.01
                elif 30 < underlying_price <= 50:
                    weight= 0.005
                if weight!=0:
                    options_q = int(self.Portfolio.MarginRemaining*weight) / (underlying_price * 100)


                
                # TODO 6: Execute strategy (~10 lines)
                #   (1) Get options corresponding to each expiry date.
                #   (2) Loop through the options based on expiry date, and
                #   (3) Purchase accordingly. Set maximum leverage to 5(using BuyingPowerModel(), LINK 3).
                expiry = min (expiries, key = lambda x: abs((x.date()-self.Time.date()).days-30))
                expiry2= min (expires, key = lambda x: abs((x.date()-self.Time.date()).days-60))
                expiry3= min(expires,key=lambda x: abs((x.date()-self.Time.date()).days-90))
                expiry4=min(expires,key=lambda x:abs((x.date()-self.Time.date()).days-120))
                filtered_expires=[expiry, expiry2,expiry3,expiry4]
                otm_calls=[[i for i in calls if i.Expiry == expiry and i.Strike == otm_strike] for expiry in filtered_expires]

                for otm_calls in otm_calls:
                    if otm_calls:
                    #Set max leverage
                        self.Securities[otm_call[0].Symbol].MarginModel = BuyingPowerModel(5)
                        #Sell out of the money call
                        self.Buy(otm_calls[0].Symbol.options_q)
                
                # #Filter out the expiries
                # desired_expiry_months = [1, 2, 3, 4]
                # today = self.Time
                # filtered_expiries = [expiry for expiry in expiries if (expiry - today).days // 30 in desired_expiry_months]

                # for expiry in filtered_expiries:
                #     # Get options for this expiry
                #     options_for_expiry = [option for option in eligible_calls if option.Expiry == expiry]

                #     for option in options_for_expiry:
                #         # Purchase the option if it meets the criteria
                #         if option.Strike == otm_strike:
                #             # Set maximum leverage
                #             self.Securities[option.Symbol].SetBuyingPowerModel(BuyingPowerModel(5))

                #             # Calculate quantity based on weight
                #             quantity = int(self.Portfolio.MarginRemaining * weight / (option.Price * 100))

                #             # Purchase the option
                #             self.Buy(option.Symbol, quantity)

                # for...
                #     if ...
                #     elif ...
                #     if weight != 0:
                #         options_q = ...
                #         self.Securities[...] = ...
                #         self.Buy(...)
                
                # TODO 7: Execute strategy (LINK 6, ~2 lines)
                # Buy spx and ief after buying options in 60:40 ratio of the left-over margin.
                self.SetHoldings(self.spy,0.6)
                self.SetHoldings(self.ief,0.4)
                # self.SetHoldings(targets, liquidateExistingHoldings, tag, orderProperties)

                    
                
                
          
#LINKS:
#1: https://www.quantconnect.com/docs/v2/cloud-platform/projects/debugging
#2: https://www.quantconnect.com/docs/v2/writing-algorithms/initialization?ref=v1
#3: https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/buying-power
#4: https://www.quantconnect.com/tutorials/introduction-to-options/quantconnect-options-api
#5: https://www.w3schools.com/python/ref_func_filter.asp
#6: https://www.quantconnect.com/docs/v2/writing-algorithms/trading-and-orders/position-sizing
