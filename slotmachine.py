from random import randint
import matplotlib.pyplot as plt

# READ ME

# How To Play
# Run the python file
# Enter user to play regularly
#   Enter space to play
#   Enter q to quit session
# Enter test to run simulation
#   Enter desired number of plays
#   Observe session statistics in console

# Paytable
#   Scatter                        -> 2
#   Standard + Standard            -> 3
#   Scatter + Scatter              -> 5
#   Standard + Standard + Scatter  -> 7
#   Standard + Standard + Standard -> 11
#   Scatter + Scatter + Scatter    -> 50
#   Bonus                          -> 1 Free Spin
#   Bonus + Bonus                  -> 3 Free Spins
#   Bonus + Bonus + Bonus          -> 5 Free Spins

# RTP/Expectation: ~89.85% or ~$0.90 per $1 entered
# Hit Frequency: ~35.83% Hit Rate

reel = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V']
payTable = {
    'onescatter': 2,
    'pair': 3,
    'twoscatter': 5,
    'pairandscatter': 7,
    'threeofakind': 11,
    'threescatter': 50
}
payTableBonus = {
    0: 0,
    1: 1,
    2: 3,
    3: 5,
}
paySymbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S']
bonus = 'T'
wild = 'U'
scatter = 'V'

def main():

    moneyBalance = 0
    playCount = 0
    winCount = 0
    sessionBonus = 0

    while True:
        print('Enter Mode (user, test)')
        mode = input()
        if mode == 'user' or mode == 'test':
            break

    if mode == 'user':
        while True:
            print('Enter Space To Play, Enter q To Quit')
            wager = input()
            if wager == ' ':
                if sessionBonus == 0:
                    moneyBalance -= 1
                else:
                    sessionBonus -= 1

                payLine = runSlot(mode)
                multiplier, addedBonus = winCheck(payLine)

                if multiplier != 0 or addedBonus != 0:
                    winCount += 1
                    moneyBalance += multiplier
                    sessionBonus += addedBonus

                playCount += 1

                print('Play Count:', playCount, 'Balance: ', moneyBalance, ' Multiplier: ', multiplier, ' PayLine: ', payLine, ' Bonus: ', addedBonus)

            elif wager == 'q':
                break

    if mode == 'test':
        while True:
            print('Number Of Iterations')
            iterationCount = input()
            if iterationCount.isdigit():
                iterationCount = int(iterationCount)
                break

        for x in range(iterationCount):
            if sessionBonus == 0:
                moneyBalance -= 1
            else:
                sessionBonus -= 1
            payLine = runSlot(mode)
            multiplier, addedBonus = winCheck(payLine)

            if multiplier != 0 or addedBonus != 0:
                winCount += 1
                moneyBalance += multiplier
                sessionBonus += addedBonus

            playCount += 1


        print('Plays: ', playCount, 'Wins: ', winCount, 'Balance: ', moneyBalance, 'Hit Rate: ', winCount/playCount, 'RTP: ', 1-abs(moneyBalance/playCount))

def winCheck(payLine):
    multiplier = 0
    addedBonus = 0
    bonusCount = 0
    scatterCount = 0
    wildCount = 0
    
    for symbol in payLine:
        if symbol == bonus:
            bonusCount += 1
        if symbol == wild:
            wildCount += 1
        if symbol == scatter:
            scatterCount += 1

    addedBonus = payTableBonus[bonusCount]

    if bonusCount == 3:
        return multiplier, addedBonus
    
    if scatterCount == 3:
        multiplier = payTable['threescatter']
        return multiplier, addedBonus
    
    if wildCount == 3:
        multiplier = payTable['threeofakind']
        return multiplier, addedBonus
    
    if wildCount == 2:
        for symbol in payLine:
            if symbol != wild and symbol != bonus and symbol != scatter:
                multiplier = payTable['threeofakind']
                return multiplier, addedBonus
    
    if scatterCount == 2:
        multiplier = payTable['twoscatter']
        return multiplier, addedBonus
    
    for paySymbol in paySymbols:
        symbolCount = 0
        for symbol in payLine:
            if symbol == paySymbol:
                symbolCount += 1

        if symbolCount == 3:
            multiplier = payTable['threeofakind']
            return multiplier, addedBonus
        
        if symbolCount == 2:
            multiplier = payTable['pair']

            for symbol in payLine:
                if symbol == wild:
                    multiplier = payTable['threeofakind']
                    return multiplier, addedBonus

            for symbol in payLine:
                if symbol == scatter:
                    multiplier = payTable['pairandscatter']
                    return multiplier, addedBonus
                
            return multiplier, addedBonus
        
    if scatterCount == 1:
        multiplier = payTable['onescatter']
        return multiplier, addedBonus
        
    return multiplier, addedBonus

def runSlot(mode):
    stripOnePosition = randint(0, len(reel)-1)
    stripTwoPosition = randint(0, len(reel)-1)
    stripThreePosition = randint(0, len(reel)-1)

    if mode == 'user':
        print('- - -')
        print(reel[stripOnePosition-1], reel[stripTwoPosition-1], reel[stripThreePosition-1])
        print(reel[stripOnePosition], reel[stripTwoPosition], reel[stripThreePosition])
        print(reel[(stripOnePosition+1)%len(reel)], reel[(stripTwoPosition+1)%len(reel)], reel[(stripThreePosition+1)%len(reel)])
        print('- - -')

    return reel[stripOnePosition] + reel[stripTwoPosition] + reel[stripThreePosition]

if __name__=="__main__":
    main()