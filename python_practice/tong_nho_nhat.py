n = list(map(int, input("Type in numbers of a list: ").split()))

Max = min(n)
total = 0

for i in n:
    total += i
    if total < Max:
        Max = total
    elif total > 0:
        total = 0
print(Max)