"""
About how Enigma REALLY works, please read the link: http://users.telenet.be/d.rijmenants/en/enigmatech.htm
"""

class Enigma:
    def __init__(self):
        self.alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.alpha = self.alphabet.copy()
        self.beta = self.alphabet.copy()
        self.gamma = self.alphabet.copy()
        self.RotorI = list("EKMFLGDQVZNTOWYHXUSPAIBRCJ")  # Model 1930, Enigma I
        self.RotorII = list("AJDKSIRUXBLHWTMCQGZNPYFVOE")  # Model 1930, Enigma I
        self.RotorIII = list("BDFHJLCPRTXVZNYEIWGAKMUSQO")  # Model 1930, Enigma I
        self.RotorIV = list("ESOVPZJAYQUIRHXLNFTGKDCMWB")  # Model Dec 1938, M3 Army
        self.RotorV = list("VZBRGITYUPSDNHLXAWMJQOFECK")  # Model Dec 1938, M3 Army
        self.RotorsList = [self.RotorI, self.RotorII, self.RotorIII, self.RotorIV, self.RotorV]
        self.Notches = ["Q", "E", "V", "J", "Z"]
        self.ReflectorA = list("EJMZALYXVBWFCRQUONTSPIKHGD")
        self.ReflectorB = list("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        self.ReflectorC = list("FVPJIAOYEDRZXWGCTKUQSBNMHL")
        self.Reflectors = [self.ReflectorA, self.ReflectorB, self.ReflectorC]

    @staticmethod
    def modulo(add1, add2, min, max):
        modulus = max - min + 1
        return (add1 + add2 - min) % modulus + min

    @staticmethod
    def switchRing(ring):  # Switch Ring function
        swap = ring[0]
        del ring[0]
        ring.append(swap)  # Append the list with the first character (that is already deleted)

    @staticmethod
    def removeSpace(thelist):  # Remove white spaces from the list
        leng = len(thelist)
        m = 0
        while m < leng:
            if thelist[m] == " ":
                thelist.remove(thelist[m])
                leng -= 1
            m += 1  # Remove white spaces in the input

    @staticmethod
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

    def run(self, rotorOne, rotorTwo, rotorThree, reflector, rotorPosiOne, rotorPosiTwo, rotorPosiThree, plugBoard,
            plaintext):

        enigmarotor = []  # Declare list for input rotors
        message = []  # Declare list for output message
        RotorNotches = []  # Get Rotors' notches
        space = []  # List for white spaces' indices
        secondNotch, thirdNotch = 0, 0  # First notches of rotors are equal 0

        enigmarotor.append(self.RotorsList[rotorOne - 1])  # Append declared Rotors to the Enigma Machine
        enigmarotor.append(self.RotorsList[rotorTwo - 1])  # Append declared Rotors to the Enigma Machine
        enigmarotor.append(self.RotorsList[rotorThree - 1])  # Append declared Rotors to the Enigma Machine
        RotorNotches.append(self.Notches[rotorOne - 1])  # Take Rotors' Notches
        RotorNotches.append(self.Notches[rotorTwo - 1])  # Take Rotors' Notches
        RotorNotches.append(self.Notches[rotorThree - 1])  # Take Rotors' Notches

        rotor1 = enigmarotor[0].copy()
        rotor2 = enigmarotor[1].copy()
        rotor3 = enigmarotor[2].copy()
        reflector = self.Reflectors[reflector - 1].copy()  # Get reflector

        if rotorPosiOne != 1:  # if rotor's position is not default
            for _ in range(rotorPosiOne - 1):
                self.switchRing(self.alpha)
        if rotorPosiTwo != 1:
            for _ in range(rotorPosiTwo - 1):
                self.switchRing(self.beta)
                secondNotch += 1
        if rotorPosiThree != 1:
            for _ in range(rotorPosiThree - 1):
                self.switchRing(self.gamma)
                thirdNotch += 1

        pblist = list(plugBoard)
        swap1, swap2 = [], []  # Plugboard swap list
        self.removeSpace(pblist)  # Remove white spaces
        for i in range(len(pblist)):
            if i % 2 == 0:
                swap1.append(pblist[i])
            else:
                swap2.append(pblist[i])

        savePlaintext = plaintext  # save plaintext for later use
        plaintext = [c for c in plaintext]
        for n in range(len(plaintext)):
            if plaintext[n] == " ":
                space.append(n)  # save white space
        self.removeSpace(plaintext)  # remove white space
        oddCase = False  # The real Enigma has an odd case when it skips a character. Please read the document

        for k in range(len(plaintext)):
            if oddCase:  # three rings are switched
                self.switchRing(self.alpha)
                self.switchRing(self.beta)
                self.switchRing(self.gamma)
                secondNotch += 1
                thirdNotch += 1
                oddCase = False
            elif not oddCase:
                self.switchRing(self.alpha)  # The rotors moves BEFORE the message is encrypted
                if self.alpha[0] == chr(ord(RotorNotches[0]) + 1):
                    self.switchRing(self.beta)  # if rotor 1 switches over the notch, the next rotor advances
                    secondNotch += 1
                    if self.beta[0] == chr(ord(RotorNotches[1])):
                        oddCase = True

            plaintext[k] = self.plugboard(plaintext[k], swap1, swap2)  # Plugboard comes first

            inputChar = self.alphabet.index(plaintext[k])  # Get the position of the input in the alphabet

            ring1in = self.alpha[inputChar]  # input into first ring
            rotor1in = self.alphabet.index(ring1in) # rotor
            ring1out = self.alpha.index(rotor1[rotor1in])  # Output of first ring

            ring2in = self.beta[ring1out]
            rotor2in = rotor2[(self.beta.index(ring2in) + secondNotch) % 26]  # Output of the second rotor
            ring2out = self.beta.index(rotor2in)

            ring3in = self.gamma[ring2out]  # Input of the third ring
            rotor3in = rotor3[(self.gamma.index(ring3in) + thirdNotch) % 26]  # Output of the third rotor
            ring3out = self.gamma.index(rotor3in)

            reflectorInput = reflector[ring3out]  # Reflector
            reflectorOutput = self.modulo(ord(reflectorInput), thirdNotch, 65,
                                          90)  # Between 65 and 90 in ASCII

            reverseRotor3 = rotor3.index(chr(reflectorOutput))  # from reflector to rotor 3

            reverseRing3 = self.gamma[(reverseRotor3 - thirdNotch) % 26]

            temp1 = self.modulo(ord(reverseRing3), secondNotch, 65, 90)

            reverseRing2Out = self.beta.index(chr(temp1))  # output from ring 2
            temp2 = self.modulo(reverseRing2Out, 65 + secondNotch - thirdNotch, 65, 90)

            reverseRing2 = rotor2.index(chr(temp2))

            reverseRing1Out = self.alpha[(reverseRing2 - secondNotch) % 26]
            reverseRotor1Out = rotor1.index(reverseRing1Out)

            revout = self.alphabet[reverseRotor1Out]  # Rotor 1 re-input
            revoutput = self.alphabet[self.alpha.index(revout)]
            revoutput = self.plugboard(revoutput, swap1, swap2)  # Plugboard again
            message.append(revoutput)  # Append the message
        length = len(message)
        for c in space:
            message.insert(c, " ")  # Put white spaces in the message
        lengthWithSpace = len(message)
        print("Plaintext: {}".format(savePlaintext))
        print("")
        print("Encrypted Text: {} ".format("".join(message)))  # Print out result
        print("\nNumber of encrypted character: {}".format(length))
        print("Number of encrypted character with space: {}\n".format(lengthWithSpace))


# 3 test cases
Enigma().run(1, 2, 3, 2, 1, 1, 1, "AT GX BJ", "AAAAAAAAAAAAAAAAAAAAAAAAA")
Enigma().run(3, 2, 1, 1, 1, 1, 3, "BJ SE XC", "GGGGGGGGGGGGGGGGGGGGGGGGG")
Enigma().run(2, 1, 3, 3, 6, 7, 2, "NW QX ZJ", "MOTHER THE FOLK FROM ABOVE CALLS ME")
