"""The code to check the results is provided by NSA on GitHub, for free:
https://github.com/NationalSecurityAgency/enigma-simulator
About how Enigma REALLY works, please read the link: http://users.telenet.be/d.rijmenants/en/enigmatech.htm
WARNING: cryptii.com encrypts wrong when both Rotor 1 and 2 go pass the notches. Please do not use it."""


def switchRing(ring):  # Switch Ring function
    swap = ring[0]
    del ring[0]
    ring.append(swap)  # Append the list with the first character (that is already deleted)


def removeSpace(list):  # Remove white spaces from the list
    length = len(list)
    m = 0
    while m < length:
        if list[m] == " ":
            list.remove(list[m])
            length -= 1
        m += 1  # Remove white spaces in the input


def plugboard(letter, swap1, swap2):  # Swap letters using Plugboard
    if len(swap1) != 0:
        while True:
            try:
                index1 = swap1.index(letter)
            except ValueError:
                pass
            else:
                letter = swap2[index1]
                break

            try:
                index2 = swap2.index(letter)
            except ValueError:
                pass
                break
            else:
                letter = swap1[index2]
                break
    return letter


Alphabet = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
Alpha = Alphabet.copy()  # First ring
Beta = Alphabet.copy()  # Second ring
Gamma = Alphabet.copy()  # Third ring
RotorI = [c for c in "EKMFLGDQVZNTOWYHXUSPAIBRCJ"]  # Model 1930, Enigma I
RotorII = [c for c in "AJDKSIRUXBLHWTMCQGZNPYFVOE"]  # Model 1930, Enigma I
RotorIII = [c for c in "BDFHJLCPRTXVZNYEIWGAKMUSQO"]  # Model 1930, Enigma I
RotorIV = [c for c in "ESOVPZJAYQUIRHXLNFTGKDCMWB"]  # Model Dec 1938, M3 Army
RotorV = [c for c in "VZBRGITYUPSDNHLXAWMJQOFECK"]  # Model Dec 1938, M3 Army

Rotors = [RotorI, RotorII, RotorIII, RotorIV, RotorV]
Notches = ["Q", "E", "V", "J", "Z"]

RefA = [c for c in "EJMZALYXVBWFCRQUONTSPIKHGD"]
RefB = [c for c in "YRUHQSLDPXNGOKMIEBFZCWVJAT"]
RefC = [c for c in "FVPJIAOYEDRZXWGCTKUQSBNMHL"]
Reflectors = [RefA, RefB, RefC]
Position = ["Right", "Middle", "Left"]

enigmarotor = []  # Declare list for input rotors
reflector = []  # Declare list for reflector
message = []  # Declare list for output message
RotorNotches = []  # Get Rotors' notches
space = []  # List for white spaces' indices
r2, r3 = 0, 0  # First notches of rotors are equal 0

print("Welcome to Enigma Machine, Model Wermarcht Machine I\nSelect 3 rotors of your choice:")
for i in range(3):
    rotor = int(input("Select your {} Rotor: from I to V by pressing 1 to 5\n".format(Position[i])))
    enigmarotor.append(Rotors[rotor - 1])  # Append declared Rotors to the Enigma Machine
    if i < 2:
        RotorNotches.append(Notches[rotor - 1])  # Take Rotors' Notches
    else:
        continue

# Take Rotors' information
rotor1 = enigmarotor[0].copy()
rotor2 = enigmarotor[1].copy()
rotor3 = enigmarotor[2].copy()

reflect = int(input("Select one reflector from the list: A, B, C by choosing one from 1 to 3:\n"))
reflector = Reflectors[reflect - 1].copy()

for i in range(3):
    r = int(input("Input the {} rotor positions you want to assign as the first, from A to Z, by choosing one from 1 "
                  "to 26.\n".format(Position[i])))
    if r == 1:
        continue
    else:
        for k in range(r - 2):
            if i == 0:
                switchRing(Alpha)
            elif i == 1:
                switchRing(Beta)
                r2 += 1
            elif i == 2:
                switchRing(Gamma)
                r3 += 1

pb = input("Input the of plugboards you want, in the format: if A connects with T, type \"AT\", each separated by a "
           "white space:")  # Plugboard input

pblist = [c for c in pb]
swap1, swap2 = [], []
removeSpace(pblist)
for i in range(len(pblist)):
    if i % 2 == 0:
        swap1.append(pblist[i])
    else:
        swap2.append(pblist[i])

plaintext = [c for c in input("Input the message you want to encrypt: \n")]

for n in range(len(plaintext)):
    if plaintext[n] == " ":
        space.append(n)

removeSpace(plaintext)

# The Enigma is ready to run!
for k in range(len(plaintext)):
    switchRing(Alpha)  # The rotors move BEFORE the message is encrypted
    if Alpha[0] == chr(ord(RotorNotches[0]) + 1):
        switchRing(Beta)  # if rotor 1 switches over the notch, the next rotor advances
        r2 += 1
        if Beta[0] == chr(ord(RotorNotches[1]) + 1):
            switchRing(Gamma)  # if Rotor 1 switches over the notch, and so does rotor 2, then rotor 3 advances
            r3 += 1

    plaintext[k] = plugboard(plaintext[k], swap1, swap2)  # Plugboard comes first

    theinput = Alphabet.index(plaintext[k])  # Get the position of the input in the alphabet

    ring1in = Alpha[theinput]  # Put the input into first rotor's position
    rotor1in = Alphabet.index(ring1in)
    rotor1out = rotor1[rotor1in]  # Output of the first rotor
    ring1out = Alpha.index(rotor1out)  # Output of first rotor when it passes the ring

    ring2in = Beta[ring1out]
    rotor2in = rotor2[(Beta.index(ring2in) + r2) % 26]  # Output of the second rotor
    ring2out = Beta.index(rotor2in)

    ring3in = Gamma[ring2out]  # Input of the third ring
    rotor3in = rotor3[(Gamma.index(ring3in) + r3) % 26]  # Output of the third rotor
    ring3out = Gamma.index(rotor3in)

    ref = reflector[ring3out]  # Reflector

    refreturn = ord(ref) + r3  # Value that returns to Rotor 3
    while refreturn > 90:
        refreturn = (refreturn - 90) + 64  # To make sure the value does not go below 65 and above 90

    revrotor3 = rotor3.index(chr(refreturn))
    revring3 = Gamma[(revrotor3 - r3) % 26]

    g = ord(revring3) + r2
    while g > 90:
        g = (g - 90) + 64  # Same reason above

    revring2out = Beta.index(chr(g))
    h = revring2out + 65 + r2 - r3
    while h > 90:
        h = (h - 90) + 64
    while h < 65:
        h = (h + 26)
    lol = chr(h)  # Value that goes into Rotor 2
    revrotor2 = rotor2.index(lol)

    revring1out = Alpha[(revrotor2 - r2) % 26]
    revrotor1 = rotor1.index(revring1out)

    revout = Alphabet[revrotor1]  # Rotor 1 re-input
    revoutput = Alphabet[Alpha.index(revout)]
    revoutput = plugboard(revoutput, swap1, swap2)  # Plugboard again
    message.append(revoutput)  # Append the message

for c in space:
    message.insert(c, " ")  # Put white spaces in the message
print("".join(message))  # Print out result
