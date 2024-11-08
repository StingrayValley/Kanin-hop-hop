import random
import time

def roll_die():
    """Simulerer et terningkast som et tilfældigt tal mellem 0 og 5."""
    return random.randint(0, 5)

def play_game(num_players, ruleset):
    """Simulerer et spil Kanin Hop Hop med udgangshuller.
    
    Argumenter:
        num_players: Antal spillere i spillet.
        ruleset: Det regelsæt der er valgt ("normal", "hurtig", "langsom").
        
    Returnerer:
        list: Liste af vindende spilleres indekser hvis der er uafgjort.
    """
    num_rabbits = 20  # Start med 20 kaniner i hulen
    players_rabbits = [0] * num_players  # Start med 0 kaniner for alle spillere
    rabbits = [False] * 5  # 5 udgangshuller
    
    while num_rabbits > 0:
        for i in range(num_players):
            roll = roll_die()

            # Spilleregler
            if ruleset == 'normal':
                if roll < 5 and not rabbits[roll]:
                    rabbits[roll] = True
                    players_rabbits[i] += 1
                    num_rabbits -= 1
            elif ruleset == "hurtig":
                if roll < 5 and not rabbits[roll]:
                    rabbits[roll] = True
                    players_rabbits[i] += 1
                    num_rabbits -= 1
                if roll < 4:  # hurtig variant tillader at tage en kanin fra midten
                    players_rabbits[i] += 1
                    num_rabbits -= 1
            elif ruleset == "langsom":
                rabbits[roll] = True
                players_rabbits[i] += 1
                num_rabbits -= 1
                if roll == 0:  # langsom variant tillader langsommere handling
                    num_rabbits -= 1

    # Find spiller(e) med flest kaniner
    max_rabbits = max(players_rabbits)
    winners = [i + 1 for i, rabbits in enumerate(players_rabbits) if rabbits == max_rabbits]
    return winners

def monte_carlo_simulation(num_players, num_simulations, ruleset):
    """Kører Monte Carlo simulationer for at estimere vinder sandsynligheder for hver spiller.
    
    Argumenter:
        num_players: Antallet af spillere.
        num_simulations: Antallet af simuleringer.
        ruleset: Regelsættet - "normal", "hurtig", eller "langsom".
        
    Returnerer:
        list: Sandsynlighederne for hver spiller at vinde.
    """
    wins = [0] * num_players

    for sim in range(num_simulations):
        start_time = time.time()
        
        # Kør en spil simulation
        winners = play_game(num_players, ruleset)
        
        for winner in winners:
            wins[winner - 1] += 1
        
        # Print simulationstid for hver 100. simulation
        if (sim + 1) % 100 == 0:
            print(f"Simulation {sim + 1}/{num_simulations} tog {time.time() - start_time:.4f} sekunder")

    # Beregn sandsynligheder for hver spiller
    probabilities = [win / num_simulations for win in wins]
    return probabilities
