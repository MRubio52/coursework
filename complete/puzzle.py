from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

KnowledgeBase = And(
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Or(CKnave, CKnight),
    Not(And(AKnave, AKnight)),
    Not(And(BKnave, BKnight)),
    Not(And(CKnave, CKnight)),

)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    KnowledgeBase,
    # He can't be both, so prove that he is not a Knight, keep that structure all the way down. 
    Implication(AKnight, And(AKnight, AKnave)),
    # Prove he is a Knave by showing that he can't be a Knight and a Knave.
    Implication(AKnave, Not(And(AKnave, AKnight)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    KnowledgeBase,
    # Basic one, they both can't be knaves. Prove that A is not a Knight.
    Implication(AKnight, And(AKnave, BKnave)),
    # Prove that A is a Knave.
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    KnowledgeBase,
    # A is lying since A and B cannot be the same. Therefore B is telling the truth.
    # Line 1 should prove why A cannot be a knight, so A Knight or A and B are a knight, and A and B are Knaves?
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))), 
    # Line 2 is a half truth and should imply that A is a knave, so A Knave, not A Knight so not B Knight, and A Knave B Knave (Which cannot be true).
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # Line 3 is the truth, so either B Knight or B is a Knight and A is a Knave or B is a Knave and A is a Knight (Flase).
    Implication(BKnight, Or(And(BKnight, AKnave), And(BKnave, AKnight))),
    # Line 4 should further disprove that B is a Knave, so B Knave and the following is not true: either B is a knight and A is a knave or B is a Knave and A is a Knight.
    Implication(BKnave, Not(Or(And(BKnight, AKnave), And(BKnave, AKnight))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    KnowledgeBase,
    # Easiest one to solve for, if A is a Knight then C must be a knight, but get to that later? For now A Knight or AKnave
    Implication(AKnight, Or(AKnight, AKnave)),
    # and then A Knave with the above code being a lie 
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    # This one is gonna be messy, have to untie the others first.
    Or(Implication(BKnight, Or(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))), Implication(BKnave, Not(Or(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))))),
    # B is absolutely the knave with this sentence so just prove it?
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    # A is indeed a knight off the above, so the puzzle solution should be A Knight, B Knave C Knight. 
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
