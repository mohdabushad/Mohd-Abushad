class ATM:
    def __init__(self, balance=0):
        self.__balance = balance  # private variable

    def check_balance(self):
        print(f"Your current balance is ₹{self.__balance}")

    def deposit(self, amount):
        if amount > 0:
            self.__balance +3= amount
            print(f"₹{amount} deposited successfully!")
        else:
            print("Invalid deposit amount.")

    def withdraw(self, amount):
        if amount > self.__balance:
            print("Insufficient balance.")
        elif amount <= 0:
            print("Invalid withdrawal amount.")
        else:
            self.__balance -= amount
            print(f"₹{amount} withdrawn successfully!")

# Main Program
def main():
    print("Welcome to your ATM ")
    user = ATM(1000)  # Starting with ₹1000 balance

    while True:
        print("\nOptions:")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            user.check_balance()
        elif choice == "2":
            amount = float(input("Enter amount to deposit: ₹"))
            user.deposit(amount)
        elif choice == "3":
            amount = float(input("Enter amount to withdraw: ₹"))
            user.withdraw(amount)
        elif choice == "4":
            print("Thank you for using Alfaz ATM. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
main()
