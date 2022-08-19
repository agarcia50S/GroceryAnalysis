def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

print(factorial(5) // (factorial(3) * factorial(2)))

def k_groups(n, sub_seqs):
    numerator = factorial(n)
    denominator = 1
    for i in sub_seqs:
        denominator *= factorial(i)
    return numerator // denominator
    
        
numer, denom = k_groups(6, [2, 2, 2]), k_groups(3, [1])

print(numer, '/', denom, '=', numer / denom)
print(k_groups(8, [2, 2, 2]))