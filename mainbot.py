#www.mcozcan.com
import time
# pip install python-binance
from binance.client import Client
from binance.enums import *
# pip install pandas
import pandas as pd
# pip install numpy
import numpy as np
import datetime as DT

import getpass

import logging
import telegram


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
satir=10
print('\n... www.mcozcan.com OTOKRIPTO Kripto Firsat Oto Alim Satim Botu - OTOKRIPTO Crypto Opportunity Auto Trading Bot...\n')
print('\n...www.mcozcan.com Hosgeldiniz - Welcome ...\n')
print('\n...Bu programa giris yaparak tum sartlari kabul etmis olursunuz - By logging into this program you agree to all terms...\n')
for i in range(satir):
    print(' '*(satir-i-1) + '*'*(2*i+1))

print('DIKKAT ! ! ! Guvenlik icin gozukmeyecektir 1 kez kopyalayiniz !  ! !')
print('ATTENTION ! ! ! It will not be visible for security. Copy 1 time! ! !')
user_chat_id = getpass.getpass("Telegram chat id giriniz: ")
#www.mcozcan.com
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)
print('DIKKAT ! ! ! Guvenlik icin gozukmeyecektir 1 kez kopyalayiniz !  ! !')
print('ATTENTION ! ! ! It will not be visible for security. Copy 1 time! ! !')
token = getpass.getpass("Telegram token giriniz: ")
updater = Updater(token, use_context=True)

def computeRSI (data, time_window):
    diff = np.diff(data)
    up_chg = 0 * diff
    down_chg = 0 * diff
    
    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[ diff>0 ]
    
    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[ diff < 0 ]

    up_chg = pd.DataFrame(up_chg)
    down_chg = pd.DataFrame(down_chg)
    
    up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    #www.mcozcan.com
    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    rsi = int(rsi[0].iloc[-1])
    return rsi

##################################################

def MACD():
    klines2 = client.get_klines(symbol=tradePair, interval='5m', limit='60')
    closeVal = [float(entry[4]) for entry in klines2]
    closeVal = pd.DataFrame(closeVal)
    ema12 = closeVal.ewm(span=12).mean()
    ema26 = closeVal.ewm(span=26).mean()
    macd = ema26 - ema12
    signal = macd.ewm(span=9).mean()

    macd = macd.values.tolist()
    signal = signal.values.tolist()
    
    if macd[-1] > signal[-1] and macd[-2] < signal[-2]:
        macdIndicator = 'BUY'
    elif macd[-1] < signal[-1] and macd[-2] > signal[-2]:
        macdIndicator = 'SELL'
    else:
        macdIndicator = 'HOLD'

    return macdIndicator

##################################################

def stopLoss():
    today = DT.date.today()
    week_ago = today - DT.timedelta(days=6)
    week_ago = week_ago.strftime('%d %b, %Y')
    klines2 = client.get_historical_klines(tradePair, Client.KLINE_INTERVAL_1DAY, str(week_ago))
    highVal = [float(entry[2]) for entry in klines2]
    lowVal = [float(entry[3]) for entry in klines2]
    closeVal = [float(entry[4]) for entry in klines2]
    avgDownDrop = (sum(highVal)/len(highVal)-sum(lowVal)/len(lowVal))/(sum(closeVal)/len(closeVal))
    stopVal = closeVal[-2]*(1-avgDownDrop)
    return stopVal
#www.mcozcan.com
####################################www.mcozcan.com###############

#m_apikey = input("Binance api keyi giriniz: ")
#api_key = m_apikey
print('DIKKAT ! ! ! Guvenlik icin gozukmeyecektir 1 kez kopyalayiniz !  ! !')
print('ATTENTION ! ! ! It will not be visible for security. Copy 1 time! ! !')
api_key = getpass.getpass('Binance api key  giriniz: ')
print('DIKKAT ! ! ! Guvenlik icin gozukmeyecektir 1 kez kopyalayiniz !  ! !')
print('ATTENTION ! ! ! It will not be visible for security. Copy 1 time! ! !')
api_secret = getpass.getpass('Binance secret key giriniz: ')

m_token1 = input("1. Tokeni giriniz (BNB-BTC vs.): ")
trdPair1 = m_token1

m_token2 = input("2. Tokeni giriniz (BNB-BTC vs.): ")
trdPair2 = m_token2

m_token3 = input("3. Tokeni giriniz (BNB-BTC vs.): ")
trdPair3 = m_token3

m_token4 = input("4. Tokeni giriniz (BNB-BTC vs.): ")
trdPair4 = m_token4

m_token5= input("Stable Tokeni giriniz (USDT-BUSD vs.): ")
trdPair5 = m_token5

m_winrate = input("Kazanc % giriniz: - Enter % of earnings: ")
m_winrate2 = float(m_winrate)
winRate = 1 + (m_winrate2/100)

print("Bot baslarken hesabinizda USDT olmalidir !")
print("You must have USDT in your account when the bot starts")
bakiye = input("Kac USD ile islem yapmak istersiniz?: - How many USD would you like to trade?: ")
use_balance = int(bakiye)


m_oran= input("Bakiyenizin % kacini kullanmak istersiniz?: - What % of your balance would you like to use? ")
m_oran2 = float(m_oran)
bakiyeorani = m_oran2 /100





client = Client(api_key,api_secret)


# Console header


#################www.mcozcan.com##################################

# Main loop
while True:
    try:
        coitime = client.get_server_time()
        coitime = time.strftime('%m/%d/%Y %H:%M:%S',
                                time.gmtime(coitime['serverTime']/1000.))
        i = 0
        j = 0
        k = 0
        l = 0
        rsi_token1 = 0
        rsi_token2 = 0
        rsi_token3 = 0
        rsi_token4 = 0
        #satin alma algoritmasi
        #purchase algorithm
      #www.mcozcan.com
        if lastrade == trdPair5:
            
            while i<2:
                        # Initial values
                tradePair = trdPair1 + trdPair5
                price = client.get_ticker(symbol=tradePair)
                sigNum = len(str(int(float(price['askPrice']))))
                sigNumOfCoin = '.' + str(len(str(int(float(price['askPrice']))))) + 'f'
                btcCount = client.get_asset_balance(asset = trdPair1)
                btcCount = float(btcCount['free'])*float(price['askPrice'])
                busdCount = client.get_asset_balance(asset = trdPair5)
                busdCount = float(busdCount['free'])

                # Find last price
                trades = client.get_my_trades(symbol=tradePair)
                trades = trades[len(trades)-1]
                lasprice = float(trades['price'])
        
                klines = client.get_klines(symbol=tradePair, interval='5m', limit='500')
                klines2 = client.get_historical_klines(tradePair, Client.KLINE_INTERVAL_1DAY, "1 day ago UTC")
                close = [float(entry[4]) for entry in klines]
                close_array = np.asarray(close)
                close_finished = close_array[:-1]

                # Indicators
                rsi_token1 = computeRSI (close_finished, 14)
                i = 3
                # Price & Server Time
                coitime = client.get_server_time()
                coitime = time.strftime('%m/%d/%Y %H:%M:%S',
                                        time.gmtime(coitime['serverTime']/1000.))

            while j<2:
                        # Initial values
                tradePair = trdPair2 + trdPair5
                price = client.get_ticker(symbol=tradePair)
                sigNum = len(str(int(float(price['askPrice']))))
                sigNumOfCoin = '.' + str(len(str(int(float(price['askPrice']))))) + 'f'
                btcCount = client.get_asset_balance(asset = trdPair2)
                btcCount = float(btcCount['free'])*float(price['askPrice'])
                busdCount = client.get_asset_balance(asset = trdPair5)
                busdCount = float(busdCount['free'])

                # Find last price
                trades = client.get_my_trades(symbol=tradePair)
                trades = trades[len(trades)-1]
                lasprice = float(trades['price'])
        
                klines = client.get_klines(symbol=tradePair, interval='5m', limit='500')
                klines2 = client.get_historical_klines(tradePair, Client.KLINE_INTERVAL_1DAY, "1 day ago UTC")
                close = [float(entry[4]) for entry in klines]
                close_array = np.asarray(close)
                close_finished = close_array[:-1]
#www.mcozcan.com
                # Indicators
                rsi_token2 = computeRSI (close_finished, 14)
                j = 3
                # Price & Server Time
                coitime = client.get_server_time()
                coitime = time.strftime('%m/%d/%Y %H:%M:%S',
                                        time.gmtime(coitime['serverTime']/1000.))

            while k<2:
                        # Initial values
                tradePair = trdPair3 + trdPair5
                price = client.get_ticker(symbol=tradePair)
                sigNum = len(str(int(float(price['askPrice']))))
                sigNumOfCoin = '.' + str(len(str(int(float(price['askPrice']))))) + 'f'
                btcCount = client.get_asset_balance(asset = trdPair3)
                btcCount = float(btcCount['free'])*float(price['askPrice'])
                busdCount = client.get_asset_balance(asset = trdPair5)
                busdCount = float(busdCount['free'])

                # Find last price
                trades = client.get_my_trades(symbol=tradePair)
                trades = trades[len(trades)-1]
                lasprice = float(trades['price'])
        
                klines = client.get_klines(symbol=tradePair, interval='5m', limit='500')
                klines2 = client.get_historical_klines(tradePair, Client.KLINE_INTERVAL_1DAY, "1 day ago UTC")
                close = [float(entry[4]) for entry in klines]
                close_array = np.asarray(close)
                close_finished = close_array[:-1]

                # Indicators
                rsi_token3 = computeRSI (close_finished, 14)
                k = 3
                # Price & Server Time
                coitime = client.get_server_time()
                coitime = time.strftime('%m/%d/%Y %H:%M:%S',
                                        time.gmtime(coitime['serverTime']/1000.))
        
            while l<2:
                        # Initial values
                tradePair = trdPair4 + trdPair5
                price = client.get_ticker(symbol=tradePair)
                sigNum = len(str(int(float(price['askPrice']))))
                sigNumOfCoin = '.' + str(len(str(int(float(price['askPrice']))))) + 'f'
                btcCount = client.get_asset_balance(asset = trdPair4)
                btcCount = float(btcCount['free'])*float(price['askPrice'])
                busdCount = client.get_asset_balance(asset = trdPair5)
                busdCount = float(busdCount['free'])

                # Find last price
                trades = client.get_my_trades(symbol=tradePair)
                trades = trades[len(trades)-1]
                lasprice = float(trades['price'])
        
                klines = client.get_klines(symbol=tradePair, interval='5m', limit='500')
                klines2 = client.get_historical_klines(tradePair, Client.KLINE_INTERVAL_1DAY, "1 day ago UTC")
                close = [float(entry[4]) for entry in klines]
                close_array = np.asarray(close)
                close_finished = close_array[:-1]

                # Indicators
                rsi_token4 = computeRSI (close_finished, 14)
                l = 3
                # Price & Server Time
                coitime = client.get_server_time()
                coitime = time.strftime('%m/%d/%Y %H:%M:%S',
                                        time.gmtime(coitime['serverTime']/1000.))     
        
        
            #False degeri rsi en kucuk ise ----True degeri rsi en buyuk ise 
            siralama = [rsi_token1,rsi_token2,rsi_token3,rsi_token4]
            siralama.sort(reverse = False)
            if siralama[0] == rsi_token1:
                tradePair = trdPair1 + trdPair5
                coiprice = format(float(price['askPrice']), '.4f')
                if rsi_token1<30:
                    stat = 'buy'
                    order = client.order_market_buy(
                        symbol=tradePair,
                        quantity=use_balance,
                        )
                    lastrade = trdPair1
                    lasprice = coiprice
                    prntInfo = '****BUY - ALIS ISLEMI****' "\n" + coitime + "\n" + trdPair1  + 'Alindi' +  "\n"  +  'Fiyat' + coiprice + ' ' 
                    updater.dispatcher.bot.send_message(chat_id=user_chat_id, text=prntInfo)
#www.mcozcan.com

                elif siralama[0] == rsi_token2:
                    coiprice = format(float(price['askPrice']), '.4f')
                    tradePair = trdPair2 + trdPair5
                    if rsi_token2<30:
                        stat = 'buy'
                        order = client.order_market_buy(
                            symbol=tradePair,
                            quantity=use_balance,
                            )
                        lastrade = trdPair2
                        lasprice = coiprice
                        prntInfo = '****BUY - ALIS ISLEMI****' "\n" + coitime + "\n" + trdPair2     + 'Alindi' +  "\n"  +  'Fiyat' + coiprice + ' ' 
                        updater.dispatcher.bot.send_message(chat_id=user_chat_id, text=prntInfo)   
                        
                elif siralama[0] == rsi_token3:
                    coiprice = format(float(price['askPrice']), '.4f')
                    tradePair = trdPair3 + trdPair5
                    if rsi_token2<30:
                        stat = 'buy'
                        order = client.order_market_buy(
                            symbol=tradePair,
                            quantity=use_balance,
                            )
                        lastrade = trdPair3
                        lasprice = coiprice
                        prntInfo = '****BUY - ALIS ISLEMI****' "\n" + coitime + "\n" + trdPair3  + 'Alindi' +  "\n"  +  'Fiyat' + coiprice + ' ' 
                        updater.dispatcher.bot.send_message(chat_id=user_chat_id, text=prntInfo)
                        #
                        #
                    
                elif siralama[0] == rsi_token4:
                    coiprice = format(float(price['askPrice']), '.4f')
                    tradePair = trdPair4 + trdPair5
                    if rsi_token2<30:
                        stat = 'buy'
                        order = client.order_market_buy(
                            symbol=tradePair,
                            quantity=use_balance,
                            )
                        lastrade = trdPair4
                        lasprice = coiprice
                        prntInfo = '****BUY - ALIS ISLEMI****' "\n" + coitime + "\n" + trdPair4 + 'Alindi' +  "\n"  +  'Fiyat' + coiprice + ' ' 
                        updater.dispatcher.bot.send_message(chat_id=user_chat_id, text=prntInfo)
                        #
                    
                    
            # satma algoritmasi             
            else:
                if lastrade == trdPair1:
                    tradePair = trdPair1 + trdPair5
                    balance = client.get_asset_balance(asset = trdPair1)
                    coiNumber = format(float(balance['free']) - 5*10**-sigNum, sigNumOfCoin) 
                    coiprice = format(float(price['askPrice']), '.4f')
                    if (float(coiprice) > float(lasprice) * winRate) :
                        stat = 'sell'
                        ## order the sell comand            
                        order = client.order_market_sell(
                            symbol=tradePair,
                            quantity= float(coiNumber),
                           )
                #www.mcozcan.com
                        lastrade = trdPair5
                        lasprice = coiprice

                        prntInfo = coitime + ' ' + 'SELL - SAT:' + ' ' + coiprice + ' ' + 'Bakiye:' + ' ' + balance['free']
                        updater.dispatcher.bot.send_message(chat_id=user_chat_id, text='***SATIS***'+ "\n" +prntInfo)
                    elif float(coiprice) < stopLoss():
                        stat = 'STOPLOSS'
                        order = client.order_market_sell(
                            symbol=tradePair,
                            quantity= float(coiNumber),
                            )

                        lastrade = trdPair5
                        lasprice = coiprice
                        prntInfo = coitime + ' ' + 'StopLoss :((( :' + ' ' + coiprice + ' ' + 'Bakiye:' + ' ' + balance['free']
                        updater.dispatcher.bot.send_message(chat_id=user_chat_id, text=prntInfo)
                    else:
            
                        #stat ='TUT-' + trdPair1 + '  ' + str(lasprice*winRate) +' -->bu fiyattan satilacak-->(eger rsi>70 ya da macd = sat)'
                        t_text = 'HOLD - TUTULUYOR-' + trdPair1 + "\n" + '  ' + str(lasprice*winRate) +' -->bu fiyattan kesin satilacak-->(ya da rsi>70 ya da macd = sat)'+  "\n" + ' rsi= ' + str(rsi) + ' macd= ' + MACD() +  "\n" + ' Anlik Deger: '+coiprice
                        updater.dispatcher.bot.send_message(chat_id=user_chat_id, text=t_text)

                elif lastrade == trdPair2:
                    tradePair = trdPair1 + trdPair2
                    balance = client.get_asset_balance(asset = trdPair2)
                    coiNumber = format(float(balance['free']) - 5*10**-sigNum, sigNumOfCoin) 
                    coiprice = format(float(price['askPrice']), '.4f')
                    if (float(coiprice) > float(lasprice) * winRate) :
                        stat = 'sell'
                        ## order the sell comand            
                        order = client.order_market_sell(
                            symbol=tradePair,
                            quantity= float(coiNumber),
                           )
                
                        lastrade = trdPair5
                        lasprice = coiprice

                        prntInfo = coitime + ' ' + 'SELL - SAT:' + ' ' + coiprice + ' ' + 'Bakiye:' + ' ' + balance['free']
                        updater.dispatcher.bot.send_message(chat_id=user_chat_id, text='***SATIS***'+ "\n" +prntInfo)
                    elif float(coiprice) < stopLoss():
                        stat = 'STOPLOSS'
                        order = client.order_market_sell(
                            symbol=tradePair,
                            quantity= float(coiNumber),
                            )

                        lastrade = trdPair5
                        lasprice = coiprice
                        #prntInfo = coitime + ' ' + 'StopLoss :((( :' + ' ' + coiprice + ' ' + 'Bakiye:' + ' ' + balance['free']
                        #updater.dispatcher.bot.send_message(chat_id=user_chat_id, text=prntInfo)
                    else:
            #www.mcozcan.com
                        #stat ='TUT-' + trdPair1 + '  ' + str(lasprice*winRate) +' -->bu fiyattan satilacak-->(eger rsi>70 ya da macd = sat)'
                        t_text = 'HOLD - TUTULUYOR-' + trdPair1 + "\n" + '  ' + str(lasprice*winRate) +' -->bu fiyattan kesin satilacak-->(ya da rsi>70 ya da macd = sat)'+  "\n" + ' rsi= ' + str(rsi) + ' macd= ' + MACD() +  "\n" + ' Anlik Deger: '+coiprice
                        updater.dispatcher.bot.send_message(chat_id=user_chat_id, text=t_text)


                elif lastrade == trdPair3:
                    tradePair = trdPair1 + trdPair3
                    balance = client.get_asset_balance(asset = trdPair3)
                    coiNumber = format(float(balance['free']) - 5*10**-sigNum, sigNumOfCoin) 
                    coiprice = format(float(price['askPrice']), '.4f')
                    if (float(coiprice) > float(lasprice) * winRate) :
                        stat = 'sell'
                        ## order the sell comand            
                        order = client.order_market_sell(
                            symbol=tradePair,
                            quantity= float(coiNumber),
                           )
                
                        lastrade = trdPair5
                        lasprice = coiprice

                        prntInfo = coitime + ' ' + 'SELL - SAT:' + ' ' + coiprice + ' ' + 'Bakiye:' + ' ' + balance['free']
                        updater.dispatcher.bot.send_message(chat_id=user_chat_id, text='***SATIS***'+ "\n" +prntInfo)
                    elif float(coiprice) < stopLoss():
                        stat = 'STOPLOSS'
                        order = client.order_market_sell(
                            symbol=tradePair,
                            quantity= float(coiNumber),
                            )

                        lastrade = trdPair5
                        lasprice = coiprice
                        #prntInfo = coitime + ' ' + 'StopLoss :((( :' + ' ' + coiprice + ' ' + 'Bakiye:' + ' ' + balance['free']
                        #updater.dispatcher.bot.send_message(chat_id=user_chat_id, text=prntInfo)
                    else:
            
                        stat ='TUT-' + trdPair1 + '  ' + str(lasprice*winRate) +' -->bu fiyattan satilacak - will be sold at this price -->(eger rsi>70 ya da macd = sat)'
                        t_text = 'HOLD- TUTULUYOR-' + trdPair1 + "\n" + '  ' + str(lasprice*winRate) +' -->bu fiyattan kesin satilacak - Will sell for sure at this price-->(ya da rsi>70 ya da macd = sat)'+  "\n" + ' rsi= ' + str(rsi) + ' macd= ' + MACD() +  "\n" + ' Anlik Deger: '+coiprice
                        updater.dispatcher.bot.send_message(chat_id=user_chat_id, text=t_text)


                elif lastrade == trdPair4:
                    tradePair = trdPair1 + trdPair4
                    balance = client.get_asset_balance(asset = trdPair4)
                    coiNumber = format(float(balance['free']) - 5*10**-sigNum, sigNumOfCoin) 
                    coiprice = format(float(price['askPrice']), '.4f')
                    if (float(coiprice) > float(lasprice) * winRate) :
                        stat = 'sell'
                        ## order the sell comand            
                        order = client.order_market_sell(
                            symbol=tradePair,
                            quantity= float(coiNumber),
                           )
                
                        lastrade = trdPair5
                        lasprice = coiprice

                        prntInfo = coitime + ' ' + 'SELL - SAT:' + ' ' + coiprice + ' ' + 'Bakiye:' + ' ' + balance['free']
                        updater.dispatcher.bot.send_message(chat_id=user_chat_id, text='***SATIS***'+ "\n" +prntInfo)
                    elif float(coiprice) < stopLoss():
                        stat = 'STOPLOSS'
                        order = client.order_market_sell(
                            symbol=tradePair,
                            quantity= float(coiNumber),
                            )

                        lastrade = trdPair5
                        lasprice = coiprice
                        prntInfo = coitime + ' ' + 'StopLoss :((( :' + ' ' + coiprice + ' ' + 'Bakiye:' + ' ' + balance['free']
                        updater.dispatcher.bot.send_message(chat_id=user_chat_id, text=prntInfo)
                    else:
            
                        stat ='TUT-' + trdPair1 + '  ' + str(lasprice*winRate) +' -->bu fiyattan satilacak-->(eger rsi>70 ya da macd = sat)'
                        t_text = 'HOLD - TUTULUYOR-' + trdPair1 + "\n" + '  ' + str(lasprice*winRate) +' -->bu fiyattan kesin satilacak-->(ya da rsi>70 ya da macd = sat)'+  "\n" + ' rsi= ' + str(rsi) + ' macd= ' + MACD() +  "\n" + ' Anlik Deger: '+coiprice
                        updater.dispatcher.bot.send_message(chat_id=user_chat_id, text=t_text)

#www.mcozcan.com
                                    
    except:
        print(coitime + ' ' + 'sunucuda hata olustu hata kodu 331 Error occurred on server error code 331')
        stat = 'sunucuda hata olustu hata kodu 331 - Error occurred on server error code 331'
        updater.dispatcher.bot.send_message(chat_id=user_chat_id, text=stat)
    # Repeat the code every 1 minute
    time.sleep(60)
