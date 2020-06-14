# NahamCon CTF 2020 Writeup

I found that this CTF had a few particularly interesting challenges, so I felt like a small writeup was due.

## Twinning

```
These numbers wore the same shirt! LOL, #TWINNING!

Connect with:
nc jh2i.com 50013
```

Netcatting to the server gives us this:

```
$ nc jh2i.com 50013
Generating public and private key...
Public Key in the format (e,n) is: (65537,7136206991423)
The Encrypted PIN is 4647953841890
What is the PIN?
```
Looks like RSA but with wayyy too small numbers, but they also have another weakness...

This challenge will definitely stick with me, as it is the first time ever that a small formula I came up with a while ago actually became useful:

![alt text](twinning/formula.png "Reverse Conjugate")

The essence of this formula is that it's able to factorize the factor of two primes `p` and `q` when `p` and `q` are consecutive (twin primes) or at least very close. The way I came up with this formula was when trying to find some way to apply the conjugate rule backwards in order to factorize `n`. I was somewhat successful, however it does diminish in accuracy quite gravely the futher away `p` and `q` are from eachother. Do note that `m` does NOT refer to the variable `m` in RSA, it is merely an intermediete variable to make the math a little more elegant. I guess you could say it's a very fancy way of doing the square root of `n`, and is pretty much useless in any practical contexts. (Though if any math geeks know a way to improve it to have accuracy across a wider range of primes, please let me know)

Anyhow, we can write this formula as a python script:

```python

def factor(n):
  sqrt=n**0.5
  m=(int(sqrt+1)**2-n)**0.5
  return [int(int(sqrt)-m+1),int(int(sqrt)+m+1)]

while True:
  n = int(input("Enter n:"))
  print(factor(n))

```

Using this program we can factor `n`:

```
Enter n:7136206991423
[2671367, 2671369]
```

We can multiply `p` and `q` together to check, and sure enough, `2671367 * 2671369 = 7136206991423`.

Now let's get to decrypting. Here's a python script to do that:

```python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m


p = 2671367
q = 2671369
ct = 4647953841890
e = 65537
phi = (p - 1) * (q - 1)
d = modinv(e, phi)
m = pow(ct, d, p * q)
print(m)
```
Running the script gives us that the PIN is `4565`, and sure enough, entering the PIN gives us the flag:

```
$ nc jh2i.com 50013
Generating public and private key...
Public Key in the format (e,n) is: (65537,7136206991423)
The Encrypted PIN is 4647953841890
What is the PIN?
4565
Good job you won!
flag{thats_the_twinning_pin_to_win}
```

##Homecooked

```
I cannot get this to decrypt!

Download the file below.
```

In this challenge, we're given a python script decrypt.py:

```python
import base64
num = 0
count = 0
cipher_b64 = b"MTAwLDExMSwxMDAsOTYsMTEyLDIxLDIwOSwxNjYsMjE2LDE0MCwzMzAsMzE4LDMyMSw3MDIyMSw3MDQxNCw3MDU0NCw3MTQxNCw3MTgxMCw3MjIxMSw3MjgyNyw3MzAwMCw3MzMxOSw3MzcyMiw3NDA4OCw3NDY0Myw3NTU0MiwxMDAyOTAzLDEwMDgwOTQsMTAyMjA4OSwxMDI4MTA0LDEwMzUzMzcsMTA0MzQ0OCwxMDU1NTg3LDEwNjI1NDEsMTA2NTcxNSwxMDc0NzQ5LDEwODI4NDQsMTA4NTY5NiwxMDkyOTY2LDEwOTQwMDA="

def a(num):
    if (num > 1):
        for i in range(2,num):
            if (num % i) == 0:
                return False
                break
        return True
    else:
        return False
       
def b(num):
    my_str = str(num)
    rev_str = reversed(my_str)
    if list(my_str) == list(rev_str):
       return True
    else:
       return False


cipher = base64.b64decode(cipher_b64).decode().split(",")

while(count < len(cipher)):
    if (a(num)):
        if (b(num)):
            print(chr(int(cipher[count]) ^ num), end='', flush=True)
            count += 1
            if (count == 13):
                num = 50000
            if (count == 26):
                num = 500000
    else:
        pass
    num+=1

print()
```

Running this file prints chunks of the flag, but eventually just stops with only a partial chunk of the flag visible. Looking at the functions, it quickly becomes apparent that `a` is a very crude implementation of a primality test; going through every number from 2 through `n` to check if they're divisible by `n`. This will obviously take a long time for numbers that are large primes or have large prime factors. On the [Wikipedia](https://en.wikipedia.org/wiki/Primality_test#Pseudocode) article about primality tests we find a bit more efficient algorithm:

```
function is_prime(n)
    if n ≤ 3 then
        return n > 1
    else if n mod 2 = 0 or n mod 3 = 0
        return false

    let i ← 5

    while i × i ≤ n do
        if n mod i = 0 or n mod (i + 2) = 0
            return false
        i ← i + 6

    return true
```
And here's the algorithm written in python:

```python
def a(n):
    if n <= 3:
        return n > 1
    elif n % 2 == 0 or n % 3 == 0:
        return False

    i = 5

    while i * i <= n:
        if n % i == 0 or n %(i + 2) == 0:
            return False
        i += 6

    return True
```

Implementing the new function and running the script now quickly reveals the entire flag:

`flag{pR1m3s_4re_co0ler_Wh3n_pal1nDr0miC}`