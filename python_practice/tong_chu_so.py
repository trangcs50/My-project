def main():
        while True:
            try:
                n = int(input("Type in a number: "))
                if n > 0:
                    break
                else:
                     print("Please enter a positve number: ")
            except ValueError:           
                print("Invalid input. Please enter an integer")
        print(each_digit(n))

def each_digit(n):
    total = 0
    while n > 0:
        each_digit = n % 10
        n //= 10
        total += each_digit
    return total
main()