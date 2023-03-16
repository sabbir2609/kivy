num = 500
count = 0

while num >= 25:
    num /= 2
    count += 1
    if num < 25:
        break
print(count - 1)
print(num * 2)
