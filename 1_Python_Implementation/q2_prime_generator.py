import time

def generate_primes(n):
    for num in range(2, n+1):
        for i in range(2, int(num**0.5)+1):
            if num % i ==0:
                break
        else:
            print(num, end =" ")


start = time.time()
generate_primes(200)
end = time.time()
print(f"time taken = {start - end} seconds")



    

    