from collections import deque


def string2num(s: str):
    return deque([ord(c) - 65 for c in s])


WALZEN_RECHTS = {
    'I': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
    'II': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
    'III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
    'IV': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
    'V': 'VZBRGITYUPSDNHLXAWMJQOFECK',
    'VI': 'JPGVOUMFYQBENHZRDKASXLICTW',
    'VII': 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
    'VIII': 'FKQHTLXOCBJSPDZRAMEWNIUYGV'
}

UKW = {
    'A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
    'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
    'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL'
}

KERBEN = {
    'I': 'Q',
    'II': 'E',
    'III': 'V',
    'IV': 'J',
    'V': 'Z',
    'VI': 'ZM',
    'VII': 'ZM',
    'VIII': 'ZM'
 }


class Walze:
    def __init__(self, nr: str, ring_pos: int, walzen_pos=None):
        self.ring_pos = ring_pos
        self.walzen_pos = None
        self.walze_rechts = string2num(WALZEN_RECHTS[nr])
        self.walze_links = deque(range(26))
        self.kerben = string2num(KERBEN[nr])
        # adjust ring position in kerben
        for i in range(len(self.kerben)):
            self.kerben[i] = (self.kerben[i] - self.ring_pos) % 26
        if walzen_pos is not None:
            self.set_walzen_pos(walzen_pos)

    def set_walzen_pos(self, walzen_pos):
        assert self.walzen_pos is None
        self.walzen_pos = walzen_pos if type(walzen_pos) is int else ord(walzen_pos) - 65
        self.shift(self.ring_pos - self.walzen_pos)

    def shift(self, offset: int=-1):
        self.walze_links.rotate(offset)
        self.walze_rechts.rotate(offset)
        # take care of shift left walze if kerbe was passed

    def is_kerb(self):
        return self.walze_links[0] in self.kerben

    def __str__(self):
        return ''.join(chr(n + 65) for n in self.walze_links) + "\n" + \
                ''.join(chr(n + 65) for n in self.walze_rechts) + "\n" + \
                ''.join(chr(n + 65) for n in self.kerben) + "\n"

    def encrypt_right(self, n):
        return self.walze_links.index(self.walze_rechts[n])

    def encrypt_left(self, n):
        return self.walze_rechts.index(self.walze_links[n])

class Enigma:
    def __init__(self, walzenlage: str, ringstellung: str, steckerverbindungen: str = '', umkehrwalze: str = 'B'):
        self.walzen = [Walze(nr, int(ring_pos if ring_pos.isnumeric() else ord(ring_pos.upper())-64) - 1) for nr, ring_pos in
                       zip(walzenlage.split(), ringstellung.split())]  # left (slow), mid, right (fast)
        self.umkerhwalze = string2num(UKW[umkehrwalze])
        self.steckerverbindungen = {}
        for p1, p2 in steckerverbindungen.split():
            n1, n2 = ord(p1) - 65, ord(p2) - 65
            self.steckerverbindungen[n1] = n2
            self.steckerverbindungen[n2] = n1

    def set_walzen_pos(self, walzen_pos: str):
        for walze, position in zip(self.walzen, walzen_pos):
            walze.set_walzen_pos(position)

    def rotate(self):
        links, mitte, rechts = self.walzen
        if mitte.is_kerb():
            mitte.shift()
            links.shift()
        elif rechts.is_kerb():
            mitte.shift()
        rechts.shift()

    def convert(self, text):
        new_text = ''
        for c in text.upper():
            n = ord(c) - 65
            if n < 0 or n > 25:
                continue
            self.rotate()
            n = self.steckerverbindungen.get(n, n)
            for walze in reversed(self.walzen):
                n = walze.encrypt_right(n)
            n = self.umkerhwalze[n]
            for walze in self.walzen:
                n = walze.encrypt_left(n)
            n = self.steckerverbindungen.get(n, n)
            new_text += chr(n+65)
        return new_text

e = Enigma('I  II  III', '1 1 1')
e.set_walzen_pos("CAT")
txt = e.convert("Wetter")
print(txt.replace('X', ' ').replace('Q', 'CH'))

e = Enigma('II IV V', '02 21 12', 'AV BS CG DL FU HZ IN KM OW RX')
e.set_walzen_pos('BLA')
txt = e.convert('EDPUD NRGYS ZRCXN UYTPO MRMBO FKTBZ REZKM LXLVE FGUEY SIOZV EQMIK UBPMM YLKLT TDEIS MDICA GYKUA CTCDO MOHWX MUUIA UBSTS LRNBZ SZWNR FXWFY SSXJZ VIJHI DISHP RKLKA YUPAD TXQSP INQMA TLPIF SVKDA SCTAC DPBOP VHJK-')
print(txt.replace('X', ' ').replace('Q', 'CH'))

e = Enigma('II IV V', '02 21 12', 'AV BS CG DL FU HZ IN KM OW RX')
e.set_walzen_pos('LSD')
txt = e.convert('SFBWD NJUSE GQOBH KRTAR EEZMW KPPRB XOHDR OEQGB BGTQV PGVKB VVGBI MHUSZ YDAJQ IROAX SSSNR EHYGG RPISE ZBOVM QIEMM ZCYSG QDGRE RVBIL EKXYQ IRGIR QNRDN VRXCY YTNJR')
print(txt.replace('X', ' ').replace('Q', 'CH'))

e = Enigma('III VI VIII', '01 08 13', 'AN EZ HK IJ LR MQ OT PV SW UX')
e.set_walzen_pos('UZV')
txt = e.convert('YKAE NZAP MSCH ZBFO CUVM RMDP YCOF HADZ IZME FXTH FLOL PZLF GGBO TGOX GRET DWTJ IQHL MXVJ WKZU ASTR')
print(txt.replace('X', ' ').replace('Q', 'CH'))

e = Enigma('II I III', '24 13 22', 'AM FI NV PS TU WZ', 'A')
e.set_walzen_pos('ABL')
txt = e.convert('GCDSE AHUGW TQGRK VLFGX UCALX VYMIG MMNMF DXTGN VHVRM MEVOU YFZSL RHDRR XFJWC FHUHM UNZEF RDISI KBGPM YVXUZ')
print(txt.replace('X', ' ').replace('Q', 'CH'))

e = Enigma('II I V', 'A A A', 'AB IR UX KP')
e.set_walzen_pos('FRA')
txt = e.convert('PCDAONONEBCJBOGLYMEEYGSHRYUBUJHMJOQZLEX')
print(txt.replace('X', ' ').replace('Q', 'CH'))

