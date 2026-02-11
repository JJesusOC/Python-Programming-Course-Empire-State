
# Sets the conditions for the scores and their grades

def grade_and_score(score):
    if score >= 97:
        return "A+"
    elif score >= 93:
        return "A"
    elif score >= 90:
        return "A-"
    elif score >= 87:
        return "B+"
    elif score >= 83:
        return "B"
    elif score >= 80:
        return "B-"
    elif score >= 77:
        return "C+"
    elif score >= 73:
        return "C"
    elif score >= 70:
        return "C-"
    elif score >= 67:
        return "D+"
    elif score >= 63:
        return "D"
    elif score >= 60:
        return "D-"
    else:
        return "F"


# Here we have a random set of scores and their will have a for loop for the squence


import random

possible_scores = range(0, 100)        
random_scores = random.sample(list(possible_scores), k=6)  

print("Grade Report:")
for s in random_scores:
    letter = grade_and_score(s)
    print(f" Score {s} → Grade {letter}")


# The while loop with a break and contnue feature will allow user
# to continue to add scores and will provide the approprate grade
# assosiaciated with that score. 

scores = []

print("Enter your scores between 0 and 100. Type 'Quit' to finish program.")

while True:
    entry = input("Score: ").strip()

    if entry.lower() == "quit":
        break

    if not entry.isdigit():
        print("Invalid! Numbers only!")
        continue

    score = int(entry)
    if not (0 <= score <= 100):
        print("Score out of range (0..100).")
        continue

    scores.append(score)
    print(f"Added {score} → Grade {grade_and_score(score)}")


