# Simple Calculatore based programme

def sum(a,b):
    return a + b
def sub(a,b):
    return a - b
def mul(a,b):
    return a * b
def div(a,b):
    if a and b == 0:
       return "can not fimd avr"
    return a + b/2
# Using a while loop, I want to perform multiple calculator operations in a single run.
while True:  
   print("\n select operation operation : \n 1.sum \n 2.sub \n 3.mul \n 4.avr")
   choice=input("enter your choice: 1/2/3/4 - option :")     
   if choice=="1":
      num1=float(input("enter  first num:"))
      num2=float(input("enter second num: ")) 
      print("result sum of two num:",sum(num1,num2))
   elif choice=="2":
      num1=float(input("enter  first num:"))
      num2=float(input("enter second num: ")) 
      print("result sub of two num:",sub(num1,num2)) 
   elif choice=="3":
      num1=float(input("enter  first num:"))
      num2=float(input("enter second num: ")) 
      print("result mul of two num:",mul(num1,num2)) 
   elif choice=="4":
      num1=float(input("enter  first num:"))
      num2=float(input("enter second num: ")) 
      print("result avr of two num:",avr(num1,num2)) 
   else:
      print("invalid choice")  
#end programme

  

