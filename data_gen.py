# import json

# letters = ['A','B','C','D']
# rooms = {}
# for letter in letters:
#     rooms[letter] = []
#     for floor in range(1,7):
#         for number in range(1,11):
#             if number >= 10:
#                 room = f"{letter}{floor}{number}"
#                 rooms[letter].append(room)
#                 continue
#             room = f"{letter}{floor}0{number}"
#             rooms[letter].append(room)

# with open('room-data.json', 'w') as file:
#     json.dump(rooms, file, indent=4)

# from decimal import Decimal,getcontext

# x = Decimal('0.05')
# y = Decimal(0).quantize(Decimal('0.01'))
# z = 2
# t = 2
# print(str(y))
# import datetime



# print(datetime.datetime.today())

import requests

# url = 'http://127.0.0.1:8000/sub-plan-payments/get-plan-prices/'
# url = 'http://127.0.0.1:9000/payment_api/payment-gateway/'
# url = 'http://127.0.0.1:9000/payment_api/price-per-day-inquiry/'
# url = 'http://127.0.0.1:8000/sub-plan-payments/payment-result/'
# p = requests.post(url=url, data={'lo':'po'})
# print(p.json())
# print('io')

