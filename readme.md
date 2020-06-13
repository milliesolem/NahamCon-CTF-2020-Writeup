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

![alt text](https://raw.githubusercontent.com/williamsolem/NahamCon-CTF-2020-Writeup/master/Twinning/formula.png "Reverse Conjugate")

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
