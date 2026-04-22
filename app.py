def genera_intelligente():
    while True:
        numeri = sorted(random.sample(range(1, 91), 6))

        # evita sequenze consecutive lunghe
        consecutivi = sum(1 for i in range(5) if numeri[i]+1 == numeri[i+1])

        # bilanciamento pari/dispari
        pari = len([n for n in numeri if n % 2 == 0])

        # distribuzione (evita tutti numeri bassi o alti)
        bassi = len([n for n in numeri if n <= 45])

        if (2 <= pari <= 4) and (2 <= bassi <= 4) and consecutivi <= 2:
            return numeri
