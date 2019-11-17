def switchRing(ring):  # Switch the ring
    swap = ring[0]
    del ring[0]
    ring.append(swap)


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
space = []
r2, r3 = 0, 0  # First notches of rotors are equal 0

print("Welcome to Enigma Machine\nSelect 3 rotors of your choice:")
for i in range(3):
    rotor = int(input("Select your {} Rotor: from I to V by pressing 1 to 5\n".format(Position[i])))
    enigmarotor.append(Rotors[rotor - 1])  # Append declared Rotors to the Enigma Machine
    if i < 2:
        RotorNotches.append(Notches[rotor - 1])  # Take Rotors' Notches
    else:
        continue

rotor1 = enigmarotor[0].copy()
rotor2 = enigmarotor[1].copy()
rotor3 = enigmarotor[2].copy()  # Take Rotors' information

reflect = int(input("Select one reflector from the list: A, B, C by pressing 1 to 3:\n"))
reflector = Reflectors[reflect - 1].copy()

plaintext = [c for c in input("Input the message you want to encrypt: \n")]

m, n = 0, 0  # For white spaces thingy
length = len(plaintext)

while n < length:
    if plaintext[n] == " ":
        space.append(n)
    n += 1  # Get white spaces of the input text

while m < length:
    if plaintext[m] == " ":
        plaintext.remove(plaintext[m])
        length -= 1
        continue
    m += 1  # Remove white spaces in the input

for k in range(len(plaintext)):

    switchRing(Alpha)  # The rotors move BEFORE the message is encrypted
    if Alpha[0] == chr(ord(RotorNotches[0])+1):
        switchRing(Beta) # if rotor 1 switches over the notch, the next rotor advances
        r2 += 1
        if Beta[0] == chr(ord(RotorNotches[1])+1):
            switchRing(Gamma) # if Rotor 1 switches over the notch, and so does rotor 2, then rotor 3 advances
            r3 += 1

    theinput = Alphabet.index(plaintext[k])  # Get the position of the input in the alphabet

    ring1in = Alpha[theinput]  # Put the input into first rotor's position
    rotor1in = Alphabet.index(ring1in)
    rotor1out = rotor1[rotor1in]  # Output of the first rotor
    ring1out = Alpha.index(rotor1out)  # Output of first rotor when it passes the ring

    ring2in = Beta[ring1out]
    rotor2in = rotor2[(Beta.index(ring2in) + r2) % 26]  # Output of the second rotor
    ring2out = Beta.index(rotor2in)

    ring3in = Gamma[ring2out]  # Input of the third ring
    rotor3in = rotor3[(Gamma.index(ring3in)+r3) % 26]  # Output of the third rotor
    ring3out = Gamma.index(rotor3in)

    ref = reflector[ring3out]  # Reflector

    rrr = ord(ref) + r3
    while rrr > 90:
        rrr = (rrr - 90) + 64  # To make sure the value does not go below 65 and above 90

    revrotor3 = rotor3.index(chr(rrr))
    revring3 = Gamma[(revrotor3-r3) % 26]

    g = ord(revring3)+r2
    while g > 90:
        g = (g - 90) + 64  # Same reason above

    revring2out = Beta.index(chr(g))
    h = revring2out + 65 + r2 - r3
    while h > 90:
        h = (h - 90) + 64
    while h < 65:
        h = (h + 26)
    lol = chr(h)
    revrotor2 = rotor2.index(lol)

    revring1out = Alpha[(revrotor2-r2) % 26]
    revrotor1 = rotor1.index(revring1out)

    revout = Alphabet[revrotor1]
    revoutput = Alphabet[Alpha.index(revout)]
    message.append(revoutput)


for c in space:
    message.insert(c, " ")  # Put white spaces in the message
print("".join(message))  # Print out result
