# Conversion decimal - IEE 754 32/64 bit Dawid Borys

# Funkcje pomocnicze
# Konwersja części całkowitej na jej reprezentację binarną
def wholeToBin(whole):
    bin = ""
    if whole == 0:
        return "0"
    else:
        while whole > 0:
            bin += str(whole % 2)
            whole //= 2
        return bin[::-1] # Odwraca wynik aby otrzymać właściwą liczbę binarną
    
# Konwersja części ułamkowej na jej reprezentację binarną
def decToBin(dec):
    bin = ""
    if dec == 0:
        return "0"
    else:
        while dec > 0:
            dec *= 2
            if dec >= 1:
                bin += "1"
                dec -= 1
            else:
                bin += "0"
        return bin # Nie odwracamy ponieważ w tym wypadku mnożymy a nie dzielimy

# Ustalamy znak liczby czyli nasz pierwszy bit
def firstBit(number):
    if number >= 0: return "0"
    else: return "1"

# Główna funkcja
def convert(number, precision):
    # Zwracamy liczbę jeżeli jestm zerem, ilość zer zależy od wybranej precyzji
    if number == "0.0":
        if precision == 32: return '0' * 31
        elif precision == 64: return '0' * 63
    else:
        # Tworzymy listę ponieważ stringi w pythonie są immutable
        nums = [*number]
        nums.remove(".")
        # Jeżeli 1 jest naszym pierwszym znakiem to wyliczamy ilość przesunięć kropki
        if nums[0] == "1":
            dot = number.find(".")
            nums.insert(1, ".")
            exponent = dot - 1
        # Jeżeli 0 jest pierwszym znakiem to musimy przenieść kropkę przed pierwszą napotkaną 1 i pozbyć się zer z przodu
        else:
            firstOneFound = number.find("1")
            nums.insert(firstOneFound, ".")
            exponent = -(firstOneFound - 1)
            nums[0:firstOneFound - 1] = ""

        # Wyliczamy binarną reprezentację eksponentu w zależności od wybranej precyzji
        if precision == 32: exponent += 127
        elif precision == 64: exponent += 1023
        exponent = wholeToBin(exponent)

        # Wyrzucamy wszystko na lewo od kropki włącdznie z nią aby uzyskać czystą mantysę
        if nums[0] == "1": nums = nums[2:]

        # Nie będziemy już wykonywac operacji na elementach mantysy więc możemy wrzucić ją do stringa
        mantissa = "".join(nums)
        
        # Uzupełniamy eksponent w zależności od wybranej precyzji
        if precision == 32: exponent = "0" * (8 - len(exponent)) + exponent
        elif precision == 64: exponent = "0" * (11 - len(exponent)) + exponent 

        # Uzupełniamy mantysę w zależności od wybranej precyzji
        if precision == 32:
            while len(mantissa) < 23:
                mantissa += "0"
            mantissa = mantissa[0:23]
        elif precision == 64:
            while len(mantissa) < 52:
                mantissa += "0"
            mantissa = mantissa[0:52]
        
        return f"{exponent} {mantissa}"

def begin():
    precision = int(input("Tutaj wpisz tryb precyzji do wyboru są 32 lub 64 czyli single lub double precision: "))
    whole = int(input("Tutaj wpisz część całkowitą liczby dodatnią lub ujemną: "))
    dec = float(input("Tutaj wpisz część ułamkową liczby w postaci 0.** np 0.125: "))
    answer = f"{firstBit(whole)} {(convert(wholeToBin(abs(whole)) + '.' + decToBin(dec), precision))}"
    print(f"1: format(znak; eksponent; mantysa): {answer}\n2: format(cała liczba zapisana ciągiem): {answer.replace(' ', '')}")

if __name__ == "__main__":
    begin()
