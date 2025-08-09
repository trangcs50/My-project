def main():
    while True:
        try:
            n = int(input("Nhap vao mot so n: "))
            if n > 1:
                break
        except ValueError:
            pass
    if nguyen_to(n):
        print("Day la so nguyen to")
    if not nguyen_to(n):
        for i in range(n):
            left = nguyen_to(n - i)
            right = nguyen_to(n + i)
            if left:
                lft = n - i
                s1 = n - lft
            if right:
                rt = n + i
                s2 = rt - n
            if s1 < s2:
                print(s1)
            elif s1 > s2:
                print(s2)
            else:
                print("Draw")

def nguyen_to(n):
    for i in range(n - 1):
        if n % i != 0:
            return True
    return False

main()