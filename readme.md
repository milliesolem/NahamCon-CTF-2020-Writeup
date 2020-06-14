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

## Homecooked

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

## Unvreakable Vase

```
Ah shoot, I dropped this data and now it's all squished and flat. Can you make any sense of this?
```

In this challenge, we're also given a text file prompt.txt:

```
zmxhz3tkb2vzx3roaxnfzxzlbl9jb3vudf9hc19jcnlwdg9vb30=
```

This looks like Base64, but where are all the upper-case letters? Base64 encoding `flag{` gives us `ZmxhZ3s=`, from that we can deduce that the problem lies with all the upper-case letters being turned to lower case. As a result, decoding the ciphertext results in `ÎlaÏ{dokóÇzèk.ßÏ.ån_co{îuÿas_crypv.oo}`, mostly gibberish, but you can see fragments of the flag. At my first attempt at this, I simply went through all the letters and tested, slowly revealing the flag, but for the purposes of this writeup, I think it's beneficial to look at a more algorithmic solution. Here's a python script that solves for the flag, it's richly commented such that it's easy to follow:

```python
import base64

#declare ciphertext (could do open("prompt.txt","r").read(), but just easier to paste the string)
ct = "zmxhz3tkb2vzx3roaxnfzxzlbl9jb3vudf9hc19jcnlwdg9vb30="
#decode base64
def dec(n):
    return base64.b64decode(n)
#change the casing of a block
def tryCase(n,i):
    #get i as 4-bit binary number
    b =format(i, '#06b')[2:]
    #declare a variable for each character in chunk
    c1=n[0]
    c2=n[1]
    c3=n[2]
    c4=n[3]
    #set them to upper if their respective bit is 1
    if b[0]=='1':
        c1=c1.upper()
    if b[1]=='1':
        c2=c2.upper()
    if b[2]=='1':
        c3=c3.upper()
    if b[3]=='1':
        c4=c4.upper()
    #return the result
    return c1+c2+c3+c4
#check if the decoded b64 falls within valid flag-characters
def isValid(n):
    try:
        #try to decode, if n contains non-ASCII characters, will automatically return false
        b=n.decode()
        #interate through decoded n
        for i in b:
            #if decoded n is less than 32 i.e. where pritable characters start, return false
            if ord(i)<32:
                return False
        #if n gets here, we can be sure it's a good character and we can return true
        return True
    except:
        return False
#split the ciphertext into 4 character blocks (aka 3-character chunks in plaintext)
blocks = [ct[i:i+4] for i in range(0, len(ct), 4)]
#declares plaintext
pt=""
#iterates blocks
for i in blocks:
    #iterates the 16 possible states a block can have (4 characters each either upper- or lower-case)
    for j in range(16):
        #define c as a test-case for the state of the block
        c = dec(tryCase(i,j))
        #check if c is valid
        if isValid(c):
            #if yes, append decoded chunk to plaintext and continue to the next block
            pt+=c.decode()
            break
#print the plaintext
print(pt)

```

Running this script returns the flag:

`flag{does_this_even_count_as_cryptooo}`