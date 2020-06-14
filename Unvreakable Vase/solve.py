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
