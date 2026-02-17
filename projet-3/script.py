import random
import time

def ask_int(prompt: str, min_value: int | None = None, max_value: int | None = None) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw.isdigit():
            print("Entre un nombre entier.")
            continue
        val = int(raw)
        if min_value is not None and val < min_value:
            print(f"Choisis un nombre >= {min_value}.")
            continue
        if max_value is not None and val > max_value:
            print(f"Choisis un nombre <= {max_value}.")
            continue
        return val

def choose_difficulty():
    print("\nChoisis une difficulté :")
    print("1) Facile   (1 à 50)")
    print("2) Normal   (1 à 100)")
    print("3) Difficile(1 à 500)")
    print("4) Personnalisé")

    choice = ask_int("Ton choix: ", 1, 4)

    if choice == 1:
        return 1, 50, 12
    if choice == 2:
        return 1, 100, 10
    if choice == 3:
        return 1, 500, 12

    # Personnalisé
    low = ask_int("Borne min: ")
    high = ask_int("Borne max (doit être > min): ")
    while high <= low:
        print("La borne max doit être strictement supérieure à la borne min.")
        high = ask_int("Borne max (doit être > min): ")
    max_tries = ask_int("Nombre d'essais max: ", 1)
    return low, high, max_tries

def play_round(low: int, high: int, max_tries: int) -> dict:
    secret = random.randint(low, high)
    tries = 0
    guesses = []
    start = time.time()

    print(f"\n🎯 Le nombre est entre {low} et {high}. Tu as {max_tries} essais.\n")

    while tries < max_tries:
        remaining = max_tries - tries
        guess = ask_int(f"Essai {tries+1}/{max_tries} (reste {remaining}) : ", low, high)
        tries += 1
        guesses.append(guess)

        if guess < secret:
            print("C'est plus !\n")
        elif guess > secret:
            print("C'est moins !\n")
        else:
            duration = round(time.time() - start, 2)
            print(f"✅ Bravo ! Tu as trouvé {secret} en {tries} essais ({duration}s).")
            return {
                "win": True,
                "secret": secret,
                "tries": tries,
                "duration": duration,
                "guesses": guesses
            }

    duration = round(time.time() - start, 2)
    print(f"❌ Perdu. Le nombre était {secret}. ({duration}s)")
    return {
        "win": False,
        "secret": secret,
        "tries": tries,
        "duration": duration,
        "guesses": guesses
    }

def score_for_round(win: bool, tries: int, max_tries: int, duration: float) -> int:
    # Score simple: bonus si victoire + bonus vitesse + bonus essais restants
    if not win:
        return 0
    base = 100
    bonus_tries = (max_tries - tries) * 10
    bonus_speed = max(0, int(30 - duration))  # max 30 pts si < 0s, sinon décroît
    return base + bonus_tries + bonus_speed

def main():
    print("=== Jeu du Juste Prix (console) ===")
    total_score = 0
    rounds_played = 0
    wins = 0

    while True:
        low, high, max_tries = choose_difficulty()
        result = play_round(low, high, max_tries)
        round_score = score_for_round(result["win"], result["tries"], max_tries, result["duration"])

        rounds_played += 1
        if result["win"]:
            wins += 1
        total_score += round_score

        print("\n--- Résumé ---")
        print(f"Historique des essais: {result['guesses']}")
        print(f"Score de la manche: {round_score}")
        print(f"Score total: {total_score} | Manches: {rounds_played} | Victoires: {wins}\n")

        again = input("Rejouer ? (o/n): ").strip().lower()
        if again not in ("o", "oui", "y", "yes"):
            print("\nMerci ! À bientôt 👋")
            break

if __name__ == "__main__":
    main()
