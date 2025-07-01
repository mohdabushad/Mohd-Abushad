# Define a class to represent the shop and its items
class Myshop:
    def __init__(self, samosa=15, pizza=100, chola=20):
        # Prices for each item
        self.samosa = samosa
        self.pizza = pizza
        self.chola = chola

    # Method to calculate and print samosa price
    def item_samosa(self, n):
        if n > 0:
            print(f"{n} samosa = {self.samosa * n} rs")
        else:
            print("\n not found")

    # Method to calculate and print pizza price
    def item_pizza(self, n):
        if n > 0:
            print(f"{n} pizza = {self.pizza * n} rs")
        else:
            print("\n not found ")

    # Method to calculate and print chola price
    def item_chola(self, n):
        if n > 0:
            print(f"{n} chola = {self.chola * n} rs")
        else:
            print("\n not found ")

    # Method to calculate and print combo of samosa and chola
    def item_samosa_chola(self, n, m):
        if n > 0 or m > 0:
            total = self.samosa * n + self.chola * m
            print(f"{n} samosa - {m} chola = {total} rs")
        else:
            print("\n not found")


# Main function to run the shop
def main():
    print("\nWelcome to My Shop :")

    # Create an object of Myshop class
    shop = Myshop()

    # Run the menu in an infinite loop until user exits
    while True:
        # Display the menu
        print("\nSelect menu:\n\n1. Samosa (15 rs)\n2. Pizza (100 rs)\n3. Chola (20 rs)\n4. Samosa and Chola\n5. Exit\n")
        
        # Get user's choice
        choice = input("Enter your choice (1-5): ")

        # Based on choice, ask quantity and call the respective method
        if choice == "1":
            n = int(input("Enter how many samosas: "))
            shop.item_samosa(n)

        elif choice == "2":
            n = int(input("Enter how many pizzas: "))
            shop.item_pizza(n)

        elif choice == "3":
            n = int(input("Enter how many cholas: "))
            shop.item_chola(n)

        elif choice == "4":
            n = int(input("Enter how many samosas: "))
            m = int(input("Enter how many cholas: "))
            shop.item_samosa_chola(n, m)
        elif choice == "5":
            print(" Thanks for my shop ")
            break

        else:
            # If invalid choice
            print("Invalid choice ....")


# Call the main function to start the program
main()
   
        
