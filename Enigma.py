def switchRing(rotor):
    swap = rotor[0]
    del rotor[0]
    rotor.append(swap)


Alphabet = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
# Alpha = Alphabet.copy()
# Beta = Alphabet.copy()
# Gamma = Alphabet.copy()
RotorI = [c for c in "EKMFLGDQVZNTOWYHXUSPAIBRCJ"]  # Model 1930, Enigma I
RotorII = [c for c in "AJDKSIRUXBLHWTMCQGZNPYFVOE"]  # Model 1930, Enigma I
RotorIII = [c for c in "BDFHJLCPRTXVZNYEIWGAKMUSQO"]  # Model 1930, Enigma I
RotorIV = [c for c in "ESOVPZJAYQUIRHXLNFTGKDCMWB"]  # Model Dec 1938, M3 Army
RotorV = [c for c in "VZBRGITYUPSDNHLXAWMJQOFECK"]  # Model Dec 1938, M3 Army
RotorVI = [c for c in "JPGVOUMFYQBENHZRDKASXLICTW"]  # Model 1939, M3 & M4 Naval(FEB 1942)
RotorVII = [c for c in "NZJHGRCXMYSWBOUFAIVLPEKQDT"]  # Model 1939, M3 & M4 Naval(FEB 1942)
RotorVIII = [c for c in "FKQHTLXOCBJSPDZRAMEWNIUYGV"]  # Model 1939, M3 & M4 Naval(FEB 1942)
Rotors = [RotorI, RotorII, RotorIII, RotorIV, RotorV, RotorVI, RotorVII, RotorVIII]
Notches = [[17], [5], [22], [10], [0], [0, 13], [0, 13], [0, 13]]

RefA = [c for c in "EJMZALYXVBWFCRQUONTSPIKHGD"]
RefB = [c for c in "YRUHQSLDPXNGOKMIEBFZCWVJAT"]
RefC = [c for c in "FVPJIAOYEDRZXWGCTKUQSBNMHL"]
Reflectors = [RefA, RefB, RefC]

enigmarotor = []  # Declare list for input rotors
reflector = []  # Declare list for reflector
message = []  # Declare list for output message
RotorNotches = []  # Get Rotors' notches
space = []
r1, r2, r3 = 0, 0, 0 # First notches are equal 0
k2, k3 = 0, 0

print("Welcome to Enigma Machine\nSelect 3 rotors of your choice:")
for i in range(3):
    rotor = int(input("Select your {} Rotor: from I to VII by pressing 1 to 8\n".format(i + 1)))
    enigmarotor.append(Rotors[rotor - 1])  # Append declared Rotors to the Enigma Machine
    if i<2:
        RotorNotches.append(Notches[rotor - 1])  # Take Rotors' Notches
    else:
        continue

rotor1 = enigmarotor[0].copy()
rotor2 = enigmarotor[1].copy()
rotor3 = enigmarotor[2].copy()  # Take Rotors' information

reflect = int(input("Select one reflector from the list: A, B, C by pressing 1 to 3:\n"))
reflector = Reflectors[reflect - 1].copy()

plaintext = [c for c in input("Input the message you want to encrypt: \n")]

m, n = 0, 0
length = len(plaintext)

while n < length:
    if plaintext[n] == " ":
        space.append(n)
    n += 1

while m < length:
    if plaintext[m] == " ":
        plaintext.remove(plaintext[m])
        length -= 1
        continue
    m += 1

for k in range(len(plaintext)):
    zero = (ord(plaintext[k]) + 1 + r1 - 65) % 26
    first = (ord(rotor1[zero]) - 1 - r1 + k2 - 65) % 26
    second = (ord(rotor2[first]) - 65 - k2) % 26
    third = (ord(rotor3[second]) - 65) % 26
    indexthird = rotor3.index(reflector[third])
    revthird = Alphabet[indexthird]
    indexsecond = rotor2.index(chr(ord(revthird)+k2))
    revsecond = Alphabet[indexsecond]
    indexfirst = rotor1.index(revsecond)
    revfirst = rotor1.index(Alphabet[(indexsecond + 1 + r1-k2) % 26])
    message.append(Alphabet[(revfirst - 1 - r1) % 26])

    r1 += 1
    for x in range (len(RotorNotches[0])):
        if (r1+1) % RotorNotches[0][x] == 0:
            r2 += 1
            k2 += 1
        if (r2+1) % RotorNotches[1][x] == 0:
            r3 += 1


for c in space:
    message.insert(c, " ")
print("".join(message))
