import random
import discord


#DISCORD CONNECTIONS

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} to play type ".play" :) ')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.play'):
        await message.channel.send("Let's play blackjack! \nDo you want to start?[Y/N]")
    
        start = await client.wait_for('message')
        start = start.content
        if(start == "Y" or start == "y"):
            pass
        else:
            quit()
        
        
        
        #GAME STARTS HERE
         
        decks = [1,2,3,4,5,6,7,8,9,10,11,12,13]*4

        #draws a random card
        def card(deck):
            rand = random.choice(deck)

            if(rand > 10):
                rand = 10
            elif(rand == 1):
                rand = 11     
            return rand
        #------------------------------------------------------------------------------
        #Dealer and Player cards

        dealerhand = [card(decks),card(decks)]
        #playerhand = [card(decks),card(decks)]
        playerhand = [2,2]

        if(sum(playerhand) == 22):
            playerhand[0] = 1
        #-----------------------------------------------------------------------------

        #Asks the player what they want to do with their cards
        async def whatToDo(hand,split):
            
            if(split == True):
                await message.channel.send("[H]it, [S]tand:")
                ask = await client.wait_for('message')
                ask = ask.content
                
                if(ask != "H" and ask != "S" and ask != "s" and ask != "h"):
                    await whatToDo(hand,split)
            elif(hand[0] == hand[1] and len(hand) == 2):
                await message.channel.send("[H]it, [S]tand, [D]ouble Down or [SP]lit:")
                ask = await client.wait_for('message')
                ask = ask.content
                
                if(ask != "H" and ask != "S" and ask != "D" and ask != "SP"
                   and ask != "h" and ask != "s" and ask != "d" and ask != "sp" ):
                    await whatToDo(hand,split)
            else:
                await message.channel.send("[H]it, [S]tand, [D]ouble Down:")
                ask = await client.wait_for('message')
                ask = ask.content
                if(ask != "H" and  ask != "S" and ask != "D" and ask != "h"
                    and ask != "s" and ask != "d"):
                    await whatToDo(hand,split)
            
           
            
            return ask
        #------------------------------------------------------------------------------

        #asks player if they want to play again
        async def playAgain():
            
            await message.channel.send("Play Again? (Y/N): ")
            tryAgain = await client.wait_for('message')
            tryAgain = tryAgain.content        
            
            if(tryAgain == "Y" or tryAgain == "y"):
                #clears everthing and creates new cards for the player and dealer
                
                playerhand = [card(decks),card(decks)]
                dealerhand = [card(decks),card(decks)]
                if(sum(playerhand) == 22):
                    playerhand[0] = 1
                    
                await message.channel.send("\nDealer is showing a "+str(dealerhand[0]))
                if(playerhand[0] == 11 and playerhand[1] == 10
                    or playerhand[1] == 11 and playerhand[0] == 10):
                    
                    await message.channel.send("Your cards: "+ str(playerhand)+' "21 You win"')
                    await playAgain()
                    
                elif(dealerhand[0] == 11 and dealerhand[1] == 10
                    or dealerhand[1] == 11 and dealerhand[0] == 10):
                    
                    await message.channel.send("Dealer: "+ str(dealerhand) +' "21 Dealer wins"')
                    await playAgain()
                    
                await play(playerhand,dealerhand)
                await playAgain()
            elif(tryAgain == "N" or tryAgain == "n"):
                await message.channel.send("You have quit.")
            else:
                await playAgain()
        #------------------------------------------------------------------------------

        #splits the first two cards into new hands and plays a new game with them
        async def split(playercards,dealercards):
            
            sp = True
            hit = False
            
            await message.channel.send("\nYour cards: "+str(playercards)+" For a total of: "+str(sum(playercards))+"\n")
            
            ask = await whatToDo(playerhand,sp)
                
            if(ask ==  "H" or ask == "h"):
                playercards.append(card(decks))
                for x in range(len(playercards)):

                    if(playercards[x] == 11 and sum(playercards) > 21):
                        playercards[x] = 1
                        hit = True
                        
                if(hit == True):
                    await split(playercards,dealercards)
                    
                elif(sum(playercards) > 21):
                    await message.channel.send("Your cards: "+str(playercards)+" For a total of: "+str(sum(playercards))+"\n")
                    await message.channel.send("You busted.\n")
                else:
                    await split(playercards,dealercards)
                    
            elif(ask == "S" or ask == "s"):
                
                return
        #------------------------------------------------------------------------------  

        async def play(playercards,dealercards):
            sp = False
            hit = False
            
            await message.channel.send("\nYour cards: "+str(playercards)+" For a total of: "+str(sum(playercards))+"\n")
            ask = await whatToDo(playercards, sp)
                    
            if(ask ==  "H" or ask == "h"):
                #gives another card and checks if you bust while Ace = 11 then the Ace will be 1
                playercards.append(card(decks))
                for x in range(len(playercards)):
                    if(playercards[x] == 11 and sum(playercards) > 21):
                        playercards[x] = 1
                        hit = True
                            
                if(hit == True):
                    await play(playercards,dealercards)
                    
                elif(sum(playercards) > 21):
          
                    await message.channel.send("\nYou busted.\n")
                    await message.channel.send("Your cards: "+str(playercards)+" For a total of: "+str(sum(playercards))+"\n")
                    return 
                else:
                    await play(playercards,dealercards)
                
            elif(ask == "S" or ask == "D" or ask == "s" or ask == "d"):
                #Checks who won
                if(ask == "D" or ask == "d"):
                    playercards.append(card(decks))
                    
                for x in range(len(playercards)):
                        if(playercards[x] == 11 and sum(playercards) > 21):
                            playercards[x] = 1
                
                if(sum(playercards) > 21):           
                    await message.channel.send("\nYou busted.")
                    await message.channel.send("Your cards: "+str(playercards)+" For a total of: "+str(sum(playercards)))
                    return
                while(sum(dealercards) < 17):
                    dealercards.append(card(decks))
                    
                if(sum(dealercards) > 21):
                    await message.channel.send("You win. Dealer Busted")
                    await message.channel.send("Dealers Cards: "+str(dealercards)+ "For a total of: "+str(sum(dealercards)))
                    return
                        
                if(sum(playercards) <= 21 and sum(playercards) == sum(dealercards)):
                    await message.channel.send("Your cards: "+str(playercards)+" For a total of: "+str(sum(playercards)))
                    await message.channel.send("Yours and the dealers scores were the same! Tie!")
                    await message.channel.send("Dealers Cards: "+str(dealercards)+ "For a total of: "+str(sum(dealercards)))
                    return
                    
                if(sum(playercards) <= 21 and sum(playercards) > sum(dealercards)):
                    await message.channel.send("Your cards: "+str(playercards)," For a total of: "+str(sum(playercards)))
                    await message.channel.send("You had a bigger score than the dealer. You won")
                    await message.channel.send("Dealers Cards: "+str(dealercards)+ "For a total of: "+str(sum(dealercards)))
                    return
                    
                else:
                    await message.channel.send("Your cards: "+str(playercards)+" For a total of: "+str(sum(playercards)))
                    await message.channel.send("Dealers score was bigger. You lost")
                    await message.channel.send("Dealers Cards: "+str(dealercards)+ "For a total of: "+str(sum(dealercards)))
                    return
                
            elif(ask == "sp" or ask == "SP"):
                    
                #makes two hands from the original hand
                hand1 = [playercards[0],card(decks)]
                hand2 = [playercards[1],card(decks)]
                
                
                    
                #plays the players hand one after another
                await message.channel.send("Play the First hand")
                await split(hand1,dealercards)
                
                    
                await message.channel.send("Play the Second hand")
                await split(hand2,dealercards)
               
                    
                hands = [hand1,hand2]
                    
                await message.channel.send("The First hand: "+str(hands[0])+ " Totals to: "+ str(sum(hands[0]))+" The Second hand: "+str(hands[1])+ " Totals to: "+ str(sum(hands[1]))+"\n")
                    
                #after the player hands have been played the dealer reveals their cards
                while(sum(dealercards) < 17):
                    dealercards.append(card(decks))
                        
                await message.channel.send("Dealer has: "+ str(dealercards) + " For a sum of: " + str(sum(dealercards)) + "\n")
                    
                #Checks who won the game or if they tied
                for i in range(len(hands)):
                    if(sum(hands[i]) > 21):         
                        await message.channel.send("You busted. Dealer wins Hand"+str(i + 1)+".")
                    elif(sum(dealercards) > 21):
                        await message.channel.send("You win hand "+str(i + 1)+". Dealer Busted")
                                
                    elif(sum(hands[i]) <= 21 and sum(dealercards) == sum(hands[i])):
                        await message.channel.send("Yours and the dealers scores were the same! Hand "+str(i + 1)+" Ties!") 
                    elif(sum(hands[i]) <= 21 and sum(hands[i]) > sum(dealercards)):
                        await message.channel.send("You had a bigger score than the dealer. You won Hand "+str(i + 1)+".") 
                    elif(sum(hands[i]) < sum(dealercards) and sum(dealercards) <= 21):
                        await message.channel.send("Dealers score was bigger. You lost Hand " + str(i + 1) + ".") 
            else:
                await message.channel.send("Not a valid input")
                
        #------------------------------------------------------------------------------
           
        #Checks if anyone had a natural blackjack if player had it he/her gets 3 times his/her bet
        if(playerhand[0] == 11 and playerhand[1] == 10
            or playerhand[1] == 11 and playerhand[0] == 10):
            
            await message.channel.send("Your cards: "+ str(playerhand) +' "21 You win"')
            await playAgain()
            
        elif(dealerhand[0] == 11 and dealerhand[1] == 10
            or dealerhand[1] == 11 and dealerhand[0] == 10):
            
            await message.channel.send("Dealer: "+  str(dealerhand) + ' "21 Dealer wins"')
            await playAgain()
        else:
            await message.channel.send("Dealer is showing a "+ str(dealerhand[0]) +"\n")
            await play(playerhand,dealerhand)
            await playAgain()

    

client.run(TOKEN)
