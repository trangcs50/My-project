n = list(map(int, input("Type in a list of number: ").split()))

max = min(n)
total = 0
for i in n:
    total += i
    if total > max:
        max = total
    if total < 0:
        total = 0
print(max)