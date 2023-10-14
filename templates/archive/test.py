import datetime

current_datetime = datetime.datetime.now()
order_number = current_datetime.strftime("%Y%m%d%H%M%S%f") +"5"

print(order_number)