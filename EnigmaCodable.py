"""
About how Enigma REALLY works, please read the link: http://users.telenet.be/d.rijmenants/en/enigmatech.htm
Parameters
----------
First : type int
    First rotor's information
Second : type int
    Second rotor's information
Third : type int
    Third rotor's information
Four: type int
    Reflector's information
Fifth: type int
    First rotor's position
Six: type int
    Second rotor's position
Seven: type int
    Third rotor's position
Eighth: type String
    Plugboard's information, A connects with T: "AT", each is seperated by a white space. Example: "AT GX BJ SE XM"
Ninth: type String
    Plaintext that needs encryption. Must be in UPPERCASE.
"""


class Enigma:
    def __init__(self):
        pass

    @staticmethod
    def run(rotorOne, rotorTwo, rotorThree, reflector, rotorPosiOne, rotorPosiTwo, rotorPosiThree, plugBoard,
            plaintext):
        def switchRing(ring):  # Switch Ring function
            swap = ring[0]
            del ring[0]
            ring.append(swap)  # Append the list with the first character (that is already deleted)

        def removeSpace(thelist):  # Remove white spaces from the list
            leng = len(thelist)
            m = 0
            while m < leng:
                if thelist[m] == " ":
                    thelist.remove(thelist[m])
                    leng -= 1
                m += 1  # Remove white spaces in the input

        def plugboard(letter, plugswap1, plugswap2):  # Swap letters using Plugboard
            if len(plugswap1) != 0:
                while True:
                    try:
                        index1 = plugswap1.index(letter)
                    except ValueError:
                        pass
                    else:
                        letter = plugswap2[index1]
                        break

                    try:
                        index2 = plugswap2.index(letter)
                    except ValueError:
                        pass
                        break
                    else:
                        letter = plugswap1[index2]
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
        message = []  # Declare list for output message
        RotorNotches = []  # Get Rotors' notches
        space = []  # List for white spaces' indices
        r2, r3 = 0, 0  # First notches of rotors are equal 0

        enigmarotor.append(Rotors[rotorOne - 1])  # Append declared Rotors to the Enigma Machine
        enigmarotor.append(Rotors[rotorTwo - 1])  # Append declared Rotors to the Enigma Machine
        enigmarotor.append(Rotors[rotorThree - 1])  # Append declared Rotors to the Enigma Machine
        RotorNotches.append(Notches[rotorOne - 1])  # Take Rotors' Notches
        RotorNotches.append(Notches[rotorTwo - 1])  # Take Rotors' Notches
        RotorNotches.append(Notches[rotorThree - 1])  # Take Rotors' Notches

        rotor1 = enigmarotor[0].copy()
        rotor2 = enigmarotor[1].copy()
        rotor3 = enigmarotor[2].copy()
        reflector = Reflectors[reflector - 1].copy()

        if rotorPosiOne == 1:
            pass
        else:
            for _ in range(rotorPosiOne - 1):
                switchRing(Alpha)
        if rotorPosiTwo == 1:
            pass
        else:
            for _ in range(rotorPosiTwo - 1):
                switchRing(Beta)
                r2 += 1
        if rotorPosiThree == 1:
            pass
        else:
            for _ in range(rotorPosiThree - 1):
                switchRing(Gamma)
                r3 += 1

        pblist = [c for c in plugBoard]
        swap1, swap2 = [], []
        removeSpace(pblist)
        for i in range(len(pblist)):
            if i % 2 == 0:
                swap1.append(pblist[i])
            else:
                swap2.append(pblist[i])
        savePlaintext = plaintext
        plaintext = [c for c in plaintext]
        for n in range(len(plaintext)):
            if plaintext[n] == " ":
                space.append(n)
        removeSpace(plaintext)
        odd = False  # The real Enigma has an odd case when it skips a character. Please read the document
        for k in range(len(plaintext)):
            if odd:
                switchRing(Alpha)
                switchRing(Beta)
                switchRing(Gamma)
                r2 += 1
                r3 += 1
                odd = False
            elif not odd:
                switchRing(Alpha)  # The rotors move BEFORE the message is encrypted
                if Alpha[0] == chr(ord(RotorNotches[0]) + 1):
                    switchRing(Beta)  # if rotor 1 switches over the notch, the next rotor advances
                    r2 += 1
                    if Beta[0] == chr(ord(RotorNotches[1])):
                        odd = True

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
        length = len(message)
        for c in space:
            message.insert(c, " ")  # Put white spaces in the message
        lengthWithSpace = len(message)
        print("{}".format(savePlaintext))
        print("")
        print("".join(message))  # Print out result
        print("\nNumber of encrypted character: {}".format(length))
        print("Number of encrypted character with space: {}\n".format(lengthWithSpace))


Enigma.run(1, 2, 3, 2, 1, 1, 1, "AT GX BJ", "AAAAAAAAAAAAAAAAAAAAAAAAA")
Enigma.run(3, 2, 1, 1, 3, 6, 4, "BJ SE XC", "GGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
