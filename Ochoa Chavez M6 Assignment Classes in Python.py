import random
from typing import List, Optional, Callable, Union

"""
Attempt to make an emulation of the card game YuGiOh.
Not as the same complexity, but use elements from the game while
trying to replicate it in a simple form. 
*using an element from Magic the Gathering with its Mana system, 
"""

# The following sets up the card portion, just using monster cards.
# Exluding Spell and Trap, to keep it easier to showcase and explain. 

class Card:
    def __init__(self, name: str, owner: "Duelist" = None):
        self.name = name
        self.owner = owner

    def play(self, duel: "Duel"):
        raise NotImplementedError("Subclasses must implement play().")

    def __str__(self) -> str:
        return self.name
    

# Keeps it to a simplified game mechanic, where you can only normal summon.
class MonsterCard(Card):
    def __init__(self, name: str, atk: int, hp: int, owner: "Duelist" = None):
        super().__init__(name, owner)
        self._atk = atk
        self._hp = hp

    @property
    def atk(self) -> int:
        return self._atk

    @property
    def hp(self) -> int:
        return self._hp

    def is_defeated(self) -> bool:
        return self._hp <= 0

    def take_damage(self, amount: int):
        self._hp -= amount

    def play(self, duel: "Duel"):
        self.owner.field.append(self)
        duel.log(f"{self.owner.name} Normal Summons {self.name} ({self.atk}/{self.hp}).")

    def attack_directly(self, duel: "Duel", target: "Duelist"):
        duel.log(f"{self.name} attacks {target.name} directly for {self.atk} damage!")
        target.take_damage(self.atk)

    def __str__(self) -> str:
        return f"{self.name} {self.atk}/{self.hp}"


# The deck for the game
class Deck:
    def __init__(self, cards: List[Card]):
        self._cards = cards[:]
        for c in self._cards:
            c.owner = None

    def shuffle(self):
        random.shuffle(self._cards)

    def draw(self) -> Optional[Card]:
        return self._cards.pop() if self._cards else None

    def attach_owner(self, owner: "Duelist"):
        for c in self._cards:
            c.owner = owner


# player and its attributes
class Duelist:
    def __init__(self, name: str, deck: Deck):
        self.name = name
        self._lp = 25
        self._hand: List[Card] = []
        self.field: List[MonsterCard] = []
        self.deck = deck
        self.deck.attach_owner(self)
        #below encforces the normal summon
        self._has_normal_summoned_this_turn = False

    @property
    def lp(self) -> int:
        return self._lp

    def take_damage(self, amount: int):
        self._lp = max(0, self._lp - amount)

    def draw(self):
        card = self.deck.draw()
        if card:
            card.owner = self
            self._hand.append(card)
    
    def draw_phase(self, duel: "Duel"):
        self.draw()
        duel.log(f"{self.name} draws a card.")

    def start_turn(self):
        # below resets normal summon availability each turn
        self._has_normal_summoned_this_turn = False

    def main_phase(self, duel: "Duel"):
        pass

    # makes all monsters attack directly
    def battle_phase(self, duel: "Duel", opponent: "Duelist"):
        if self.field:
            duel.log(f"{self.name} enters the Battle Phase and declares attacks with all monsters!")
        for monster in self.field:
            monster.attack_directly(duel, opponent)

    def end_phase(self, duel: "Duel"):
        duel.log(f"{self.name} proceeds to the End Phase.")

    
    # Actions for the game. 
    def normal_summon_from_hand(self, duel: "Duel", hand_position_1_based: int) -> bool:
        if self._has_normal_summoned_this_turn:
            duel.log(f"{self.name} has already Normal Summoned this turn.")
            return False

        idx = hand_position_1_based - 1
        if idx < 0 or idx >= len(self._hand):
            duel.log("Invalid hand position.")
            return False

        card = self._hand[idx]
        if not isinstance(card, MonsterCard):
            duel.log("Only Monster Cards can be Normal Summoned in this simplified duel.")
            return False

        card.play(duel)
        self._hand.pop(idx)
        self._has_normal_summoned_this_turn = True
        return True

    def __str__(self) -> str:
        field_txt = ", ".join(str(c) for c in self.field) if self.field else "—"
        hand_txt = ", ".join(str(c) for c in self._hand) if self._hand else "—"
        return (f"{self.name} | LP: {self.lp}\n"
                f"Field: {field_txt}\n"
                f"Hand: {hand_txt}\n")


# User Duelist input
class HumanDuelist(Duelist):
    def main_phase(self, duel: "Duel"):
        if not self._hand:
            print("=== Main Phase ===\nYour hand is empty. You may proceed to the Battle Phase.")
            return

        print("=== Main Phase ===")
        print("Your Hand:")
        for i, c in enumerate(self._hand, start=1):  # 1-based display
            print(f"  ({i}) {c}")

        choice = input("Normal Summon 1 monster by entering its number, or press Enter to skip: ").strip()
        if choice == "":
            print("You skip your Normal Summon.")
            return
        if not choice.isdigit():
            print("Invalid input. Skipping.")
            return

        hand_pos = int(choice)
        ok = self.normal_summon_from_hand(duel, hand_pos)
        if not ok:
            print("Normal Summon failed.")


# Bot Duelist input
class BotDuelist(Duelist):
    def main_phase(self, duel: "Duel"):
        if not self._hand:
            duel.log(f"{self.name} has no cards to Normal Summon.")
            return

        # This finds all monsters positions (1-based), then picks the highest ATK
        monster_positions = [i for i, c in enumerate(self._hand, start=1) if isinstance(c, MonsterCard)]
        if not monster_positions:
            duel.log(f"{self.name} has no monsters to Normal Summon.")
            return

        best_pos = max(
            monster_positions,
            key=lambda pos: (self._hand[pos - 1].atk, self._hand[pos - 1].hp)
        )
        self.normal_summon_from_hand(duel, best_pos)


# This tells the sequence of chains (like in the actual TCG) of actions. 
class Duel:
    def __init__(self, d1: Duelist, d2: Duelist):
        self.duelists = [d1, d2]
        self.turn = 0
        self._log: List[str] = []

    def opponent_of(self, d: Duelist) -> Duelist:
        return self.duelists[1] if self.duelists[0] == d else self.duelists[0]

    def log(self, text: str):
        self._log.append(text)
        print(text)

    def is_over(self) -> bool:
        return any(d.lp <= 0 for d in self.duelists)

    def winner(self) -> Optional[Duelist]:
        a, b = self.duelists
        if a.lp <= 0 and b.lp <= 0:
            return None  # tie
        if a.lp <= 0:
            return b
        if b.lp <= 0:
            return a
        return None

    def show_state(self):
        print("\n== Current State ==")
        for d in self.duelists:
            print(d)
        print("===================\n")
    
    #Opening hand: Draw 5 cards (really old school compared to today)
    def run(self):
        for d in self.duelists:
            d.deck.shuffle()
            for _ in range(5):
                d.draw()
        
        #Progression of Phases: Draw, Main, Battle, and End Phase
        while not self.is_over():
            self.turn += 1
            current = self.duelists[(self.turn - 1) % 2]
            opponent = self.opponent_of(current)

            print(f"\n===== Turn {self.turn}: {current.name} =====")
            current.start_turn()

            print(">> Draw Phase")
            current.draw_phase(self)

            print(">> Main Phase")
            current.main_phase(self)

            print(">> Battle Phase")
            current.battle_phase(self, opponent)

            print(">> End Phase")
            current.end_phase(self)
            self.show_state()

            if self.is_over():
                break

        w = self.winner()
        if w is None:
            print("The duel ends in a tie!")
        else:
            print(f"{w.name} won the duel!")


# Deck Builder. Monster Cards only as mentioned with a max of 3 copies of each monster
def build_monster_deck() -> Deck:

    # The format of the monsters and their stats:
    #  Name: (ATK, HP, copies); Max of 3 copies
    pool = {
        "Lovely Labrynth of the Silver Castle": (6, 7, 1),
        "Tearlaments Kaleido-Heart":            (6, 6, 1),
        "Accesscode Talker":                    (7, 6, 1),
        "Five-Headed Dragon":                   (8, 8, 1),
        "Red Nova Dragon":                      (7, 7, 1),
        "Supreme King Z-ARC":                   (8, 8, 1),
        "Quintet Magician":                     (7, 6, 1),
        "Dark Paladin":                         (6, 5, 1),
        "Ultimate Conductor Tyranno":           (7, 6, 1),
        "Red-Eyes Darkness Metal Dragon":       (6, 6, 1),
        "Blue-Eyes Shining Dragon":             (7, 6, 1),
        "Number C107: Neo Galaxy-Eyes Tachyon Dragon": (8, 7, 1),
        "Armityle the Chaos Phantom":           (8, 8, 1),
        "Apoqliphort Towers":                   (7, 7, 1),
        "Raviel, Lord of Phantasms":            (7, 7, 1),
    }

    # This enforces the limit of 3 copies
    cards: List[Card] = []
    for name, (atk, hp, copies) in pool.items():
        copies = max(0, min(3, int(copies)))
        for _ in range(copies):
            cards.append(MonsterCard(name, atk, hp))

    return Deck(cards)


# Main
def main():
    random.seed()
    human_deck = build_monster_deck()
    bot_deck = build_monster_deck()

    human = HumanDuelist("You", human_deck)
    bot = BotDuelist("Bot", bot_deck)

    duel = Duel(human, bot)
    duel.run()

if __name__ == "__main__":
    main()