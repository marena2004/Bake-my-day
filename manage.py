from product import Product
import random
from datetime import datetime


class Orders:
    def __init__(self):
        self.__order = {}

    @property
    def order(self):
        return self.__order

    @order.setter
    def order(self, order):
        self.__order = order

    def add_menu(self, choose):
        for data in Product().readfile():
            if choose == data["id"]:
                amount = int(input(f"How many {data['menu']} do you want?: "))
                if Product().check_stock(int(data["stock"]), amount):  # check whether menu available or not
                    Product().update_stock(int(data["stock"]), amount)  # update stock
                    self.__order.update({data["menu"]: {"id": data["id"],
                                                        "quantity": amount,
                                                        "subtotal": int(data["price"]) * amount}})
                    print(f"Add {amount} {data['menu']} to the cart.")
                    return self.__order
                else:
                    return False

    def delete(self, choose):
        for menu, info in self.__order.copy().items():
            if choose == info["id"]:
                self.__order.pop(menu)  # remove unwanted menu from card
                print(f'{menu} has been removed.')

    def cancel(self):
        self.__order.clear()  # delete all orders
        print("Cancel successfully.")

    def subtotal(self):
        total_price = 0
        for menu, info in self.__order.items():
            total_price += int(info["subtotal"])
        return total_price

    def discount(self):
        if self.subtotal() >= 300:
            dis = self.subtotal() * 0.1
            return dis
        return 00.00

    def total(self):
        if self.subtotal() >= 300:
            total = self.subtotal() - self.discount()
            return total
        return self.subtotal()

    def get_id_order(self):
        upper_case = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        number = '1234567890'
        use_for = upper_case + number
        length = 15
        id_order = ''.join(random.sample(use_for, length))  # create id order
        return id_order

    def receipt(self):
        now = datetime.now()
        day = now.date()
        time = now.strftime("%H:%M")
        with open("order_receipt.txt", "w") as f:  # write receipt in text file
            f.write(" " * 25 + "B A K E  M Y  D A Y\n\n")
            f.write(" " * 19 + "Thank you for ordering our product!\n\n")
            f.write(f"Order #{self.get_id_order()}\n\n")
            f.write("Menu" + " " * 30 + "Quantity" + " " * 30 + "Price\n")
            f.write("-" * 80 + "\n")
            for k, v in self.__order.items():
                f.write(f"{k}".ljust(37, " ") + f"{v['quantity']}".ljust(35, " ") + f"{v['subtotal']}.-\n")
            f.write("-" * 80 + "\n")
            pay = input("Do you want to pay by Bank Transfer(b) or Credit Card(c)?: ")
            while True:
                if pay == 'b':
                    f.write(f"Subtotal: {self.subtotal():.2f}฿".ljust(58, " ") + f"Payment: Bank Transfer\n")
                    break
                elif pay == 'c':
                    f.write(f"Subtotal: {self.subtotal():.2f}฿".ljust(58, " ") + f"Payment: Credit Card\n")
                    break
                elif not pay == 'b' or 'c':
                    print("Please enter b or c only")
                    pay = input("Do you want to pay by Bank Transfer(b) or Credit Card(c)?: ")
            f.write(f"Shipping fee: 0.00฿" + " ".ljust(39, " ") + f"Order date: {day}\n")
            f.write(f"Discount: {self.discount():.2f}฿".ljust(58, " ") + f"Time: {time}\n")
            f.write(f"Total: {self.total():.2f}฿\n\n")
            f.write(f"Shipping to:\n")
            name = input("Enter your name: ")
            phone = input("Enter your phone number: ")
            while True:
                if not phone.isdigit():
                    print("Phone number must numbers!")
                    phone = input("Enter your phone number: ")
                elif len(phone) < 10:
                    print("Invalid phone number")
                    phone = input("Enter your phone number: ")
                else:
                    break
            address = input("Enter your address: ")
            f.write(f"{name.title()}\n")
            f.write(f"{phone}\n")
            f.write(f"{address.title()}\n")
            f.write("-" * 80 + "\n")
            f.write(" " * 24 + "H A V E  A  N I C E  D A Y!")
