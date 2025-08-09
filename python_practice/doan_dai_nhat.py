n = list(map(int, input("Type in numbers of a list: ").split()))
k = int(input("Type in k: "))

current_sum = 0
length = 0
start = 0
end = 0

for end in range(len(n)):
    current_sum += n[end]
    if current_sum > k:
        while current_sum > k:
            current_sum -= n[start]
            start += 1
    if current_sum <= k:
        length = max(length, end - start + 1)
print(length)