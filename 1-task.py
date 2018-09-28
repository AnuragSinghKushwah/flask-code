n=input("enter the nth prime ") #please enter the number
num=4
p=2

while p <int(n):
    if all(num%i!=0 for i in range(2,num)):
        p=p+1
    num=num+1

print( "nTH prime number: ",num-1)