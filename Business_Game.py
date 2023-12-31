from random import randint
import math
def PositiveDenomination(player,amount):
  notes = [5000, 1000, 500, 100]
  for i in range(3):
    if amount >= notes[i]:
      player.denominations[i] += amount//notes[i]
      amount = amount % notes[i]

def ShowDenomination(player):
  notes = [5000, 1000, 500, 100]
  for i in range(3):
    while player.denominations[3-i]<0:
      player.denominations[3-i] += notes[2-i]/notes[3-i]
      player.denominations[2-i] -= 1
      
class Player:
    def __init__(self, player_name):
        """Create a player from input"""
        self.name = player_name
        self.money = 15000
        self.properties = []
        self.house=[]
        self.die1 = 0
        self.die2 = 0
        self.last_roll = 0
        self.in_jail = False
        self.is_turn = False
        self.jail_time = 0
        self.miss_next_chance = False
        self.rent_collected = 0
        self.denominations = [1,4,10,10]

    def __repr__(self):
        """Return description of player"""
        return f'''\
            This player, {self.name}, is playing.
            {self.name} has Rs{self.money}, is currently on {business_board.player_positions[business_board.player_list.index(self)]}, and owns these properties:
            {self.properties}
            '''
    def roll_dice(self):
        """Roll two dice and return the results"""
        self.die1 = randint(1,6)
        self.die2 = randint(1,6)
        self.last_roll = self.die1 + self.die2

        print(f"{self.name} rolled a {self.last_roll}! ({self.die1} + {self.die2})")

        return (self.die1, self.die2, self.last_roll)

    def take_turn(self):
        self.is_turn = True
        turn_count = 0
        while self.is_turn < 2:
            turn_count += 1
            self.update_position()
            if self.is_turn and self.miss_next_chance:
                print(f"{self.name} rolled")


class Board():
    def __init__(self, layout):
        """Create Board object from list"""
        self.layout = layout
        self.length = len(layout)
        self.player_list = []
        self.player_positions = []
        self.player_turn = 0

    def update_position(self, player, die1 = 0, die2 = 0, spaces_to_move = 0):
        """Move players around board"""
        player_index = self.player_list.index(player)
        while spaces_to_move > 0:
            self.player_positions[player_index] += 1
            spaces_to_move -= 1
            # Wrap around board
            if self.player_positions[player_index] >= self.length:
                self.player_positions[player_index] = 0
                player.money += 1500
                player.denominations[3] += 10
                player.denominations[2] += 1
                print(f"{player.name} passed start and collects Rs1500.")
        return

    def go_to_jail(self, player):
        self.player_positions[self.player_list.index(player)] = self.layout.index(jail)
        print(f"{player.name} is on space {self.player_positions[self.player_list.index(player)]} and is in Jail.")
        player.in_jail = True
        player.jail_time = 0
        player.die1 = 0

class Sites:
    def __init__(self,name,cost,max_houses):
        self.name = name
        self.cost = cost
        self.house_cost = 500
        self.houses = 0
        self.rent = [math.floor(cost/1000)*100,math.floor(cost/500)*100]
        self.is_owned = False
        self.max_houses=max_houses
    def buy_property(self, player, board):
        if player.money < self.cost:
            print(f"You don't have enough money to afford this property.")
            self.fine(player, board)
            return
        else:
            print(f"{player.name} purchases {self.name} for Rs{self.cost}.")
            player.money -= self.cost
            player.denominations[3] -= self.cost/100
            player.properties.append(self)
            self.is_owned = True
            self.owner = player

    def fine(self, player, board):
      player.money -= 1000
      player.denominations[3] -= 10

    def buy_house(self, player):
        if player.money < self.house_cost:
            print(f"You don't have enough money to afford a house here.")
            return
        else:
            if self.houses <= self.max_houses:
                self.houses += 1
                player.house.append(self)
                player.money-=self.house_cost
                player.denomination[3]-= self.house_cost/100
            else:
                print(f"This property already has a house.")

    def charge_rent(self, renter):
        self.owner.money += self.rent[self.houses]
        self.owner.denominations[3] += self.rent[self.houses]/100
        self.owner.rent_collected += self.rent[self.houses]
        renter.money -= self.rent[self.houses]
        renter.denominations[3] -= self.rent[self.houses]/100
        print(f"{renter.name} landed on {self.name}. Rent with {self.houses} houses costs Rs{self.rent[self.houses]}.")
        print(f"{renter.name} paid {self.owner.name} Rs{self.rent[self.houses]}.")

    def interact(self, player, board):
        if self.is_owned == False:
            print("Would you like to buy",self.name," for ",self.cost,"?")
            response = str(input()).title()
            while response != "Yes" and response != "No":
                print("Please enter Yes or No.")
                response = str(input()).title()
            if response == "No":
                self.fine(player, board)
            else:
                self.buy_property(player, board)
        else:
            if self.owner == player:

                print("You own this property, would you like to build a house?")
                if self.houses<self.max_houses:
                    response = str(input()).title()
                    while response != "Yes" and response != "No":
                        print("Please enter Yes or No.")
                    response = str(input()).title()
                    if response == "Yes":
                        self.buy_house(player)
                    return
                else:
                    print('You own this property')
                    return
            self.charge_rent(player)

class Property(Sites):
    def __init__(self,name,cost,max_houses=1):
        super().__init__(name,cost,max_houses)
class Transportation(Sites):
    def __init__(self,name,cost,max_houses=0):
        super().__init__(name,cost,max_houses)
class Services(Sites):
    def __init__(self,name,cost,max_houses=0):
        super().__init__(name,cost,max_houses)

class Chance():
    def __init__(self,name):
      self.die_number = 0
      self.name=name
    def movement_card(self, player, board):
      current_space = board.player_positions[board.player_list.index(player)]
      target_space = board.layout.index(restHouse)
      spaces_to_move = 0
      if target_space > current_space:
        spaces_to_move = target_space - current_space
      else:
        spaces_to_move = board.length - (current_space - target_space)
      board.update_position(player = player, spaces_to_move = spaces_to_move)
      current_position = board.player_positions[board.player_list.index(player)]
      print(f"{player.name} landed on space {current_position}, {board.layout[current_position].name}.")
      board.layout[current_position].interact(player = player, board = board)

    def interact(self,player,board):
      self.die_number = player.last_roll
      if self.die_number==2:
        print('Loss of Rs2000 in share market')
        player.money -= 2000
        player.denominations[3] -= 20
      elif self.die_number==3:
        print('Congrats!,You have won lottery prize of Rs2500')
        player.money += 2500
        PositiveDenomination(player,2500)
      elif self.die_number==4:
        print('Drink and Drive, Fine of Rs1000')
        player.money -= 1000
        player.denominations[3] -= 10
      elif self.die_number==5:
        print('Congrats!,You have won crossword competition of Rs1000')
        player.money += 1000
        PositiveDenomination(player,1000)
      elif self.die_number==6:
        print('House Repairs Rs1500')
        player.money -= 1500
        player.denominations[3] -= 15
      elif self.die_number==7:
        print('Congrats!,You have won jackpot prize of Rs2000')
        player.money += 2000
        PositiveDenomination(player,2000)
      elif self.die_number==8:
        print('Loss due to fire in godown,Rs3000')
        player.money -= 3000
        player.denominations[3] -= 30
      elif self.die_number==9:
        pass
      elif self.die_number==10:
        print('Go To Jail.')
        board.player_positions[board.player_list.index(player)] = board.layout.index(jail)
      elif self.die_number==11:
        print('Congrats!,price of best performance in Exports,Rs3000')
        player.money += 3000
        PositiveDenomination(player,2000)
      else:
        print('Go to Rest House,you cannot play next turn')
        board.player_positions[board.player_list.index(player)] = board.layout.index(restHouse)
        player.miss_next_chance=True



class CommunityChest():
    def __init__(self,name):
      self.die_number = 0
      self.name=name


    def collection_card(self, active_player, board):
      for player in board.player_list:
        player.money -= 500
        player.denominations[3] -= 5
        active_player.money += 500
        active_player.denominations[3] += 5
    def interact(self,player,board):
      self.die_number = player.last_roll
      if self.die_number==2:
        print('Congrats! It is your birthday, take Rs500 from each player')
        self.collection_card(player, board)
      elif self.die_number==3:
        print('Congrats!, Go To Jail.')
        board.player_positions[board.player_list.index(player)] = board.layout.index(jail)
      elif self.die_number==4:
        print('Congrats!,First prize in Big Boss,Rs2500')
        player.money += 2500
        PositiveDenomination(player,2500)
      elif self.die_number==5:
        print('School and Medical Fees,Rs1000')
        player.money -= 1000
        player.denominations[3] -= 10
      elif self.die_number==6:
        print('Income Tax Refund!, Rs2000')
        player.money += 2000
        PositiveDenomination(player,2000)
      elif self.die_number==7:
        print('Marriage Celebration, Rs2000')
        player.money -= 2000
        player.denominations[3] -= 20
      elif self.die_number==8:
        print('Go to Rest House,you cannot play next turn')
        player.miss_next_turn = True
        board.player_positions[board.player_list.index(player)] = board.layout.index(restHouse)
      elif self.die_number==9:
        print('Houses Repair, Rs50 per each')
        n_houses = 0
        for i in player.properties:
          n_houses += i.houses
        player.money -= 50*n_houses
        player.denominations[3] -= 0.5*n_houses
      elif self.die_number==10:
        print('Congrats!, received interest of Rs1500 on shares.')
        player.money += 1500
        PositiveDenomination(player,1500)
      elif self.die_number==11:
        print('Pay insurance premium of Rs1500.')
        player.money -= 1500
        player.denominations[3] -= 15
      else:
        print('Sale of stocks,Rs3000 received.')
        player.money += 3000
        PositiveDenomination(player,3000)


class Miscellaneous:
    def __init__ (self, name):
        self.name = name

    def interact (self, player, board):
        if self.name == "Start":
            return
        elif self.name == "IncomeTax":
            print(f"{player.name} pays Income Tax of Rs{math.floor(player.rent_collected/1000)*100}")
            player.money -= math.floor(player.rent_collected/1000)*100
            player.denominations[3] -= math.floor(player.rent_collected/1000)
        elif self.name == "Jail":
            print('You have to pay Rs1500 to the bank and lose your next turn')
            player.money-=1500
            player.denominations[3] -= 15
            player.miss_next_chance=True

        elif self.name == "restHouse":
            print(f"Pay Rs100 and enjoy the facilities of Rest House.")
            player.money -= 100
            player.denominations[3] -= 1
        elif self.name == "WealthTax":
            print(f"{player.name} pays Wealth Tax of Rs200")
            player.money -= 200
            player.denominations[3] -= 2
        elif self.name == "Club":
            print(f"Pay Rs100 and enjoy the facilities of Club.")
            player.money -= 200
            player.denominations[3] -= 2


Mumbai = Property(name="Mumbai", cost=8500)
Ahmedabad = Property(name="Ahmedabad", cost=4000)
Indore = Property(name="Indore", cost=1500)
Goa = Property(name="Goa", cost=4000)
Cochin = Property(name="Cochin", cost=3000)
Mysore = Property(name="Mysore", cost=2500)
Bangalore = Property(name="Bangalore", cost=4000)
Chennai = Property(name="Chennai", cost=7000)
Hyderabad = Property(name="Hyderabad", cost=3500)
Kolkata = Property(name="Kolkata", cost=6500)
Darjeeling = Property(name="Darjeeling", cost=2500)
Patna = Property(name="Patna", cost=2000)
Kanpur = Property(name="Kanpur", cost=4000)
Agra = Property(name="Agra",cost=2500)
Jaipur = Property(name="Jaipur",cost=3000)
Srinagar = Property(name="Srinagar",cost=5000)
Amritsar = Property(name="Amritsar", cost=3300)
Shimla = Property(name="Shimla", cost=2200)
Chandigarh = Property(name="Chandigarh", cost=2500)
Delhi = Property(name="Delhi", cost=6000)

BEST = Transportation(name="BEST",cost=3500)
Railways = Transportation(name="Railways",cost=9500)
MotorBoat = Transportation(name="MotorBoat",cost=5500)
AirIndia = Transportation(name="AirIndia",cost=10500)

ElectricCompany = Services(name="ElectricCompany",cost=2500)
WaterWorks = Services(name="WaterWorks",cost=3200)

Start = Miscellaneous("Start")
IncomeTax = Miscellaneous("IncomeTax")
jail = Miscellaneous("Jail")
restHouse = Miscellaneous("restHouse")
WealthTax = Miscellaneous("WealthTax")
Club = Miscellaneous("Club")

Chance = Chance('Chance')
CommunityChest = CommunityChest('Community Chest')

business_board = Board([Start, Mumbai, WaterWorks, Railways, Ahmedabad, IncomeTax, Indore, Chance, Jaipur, jail, Delhi, Chandigarh, ElectricCompany,
                        BEST,Shimla,Amritsar,CommunityChest,Srinagar,Club,Agra,Chance,Kanpur,Darjeeling,AirIndia,Kolkata,Hyderabad,restHouse,Chennai,
                        CommunityChest,Bangalore,WealthTax,Mysore,Cochin,MotorBoat,Goa])



player_count = 0
while player_count < 2 or player_count > 4:
    print("How many players will be playing?")
    try:
        player_count = int(input())
    except:
        print("That wasn't a number!")
    if player_count < 2:
        print("Player count is too low, please select between 2 and 4 players.")
    if player_count > 4:
        print("Player count is too high, please select between 2 and 4 players.")

for i in range(player_count):
    player_choices = []
    print(f"What is Player {i+1}'s name?")
    player_choices.append(input().title())

    business_board.player_list.append(Player(player_choices[0]))
    business_board.player_positions.append(0)

print('Welcome',end=' ')
for u in business_board.player_list:
  print(u.name,end=', ')
print('')
print('All the players have been given Rs15000 and now are ready for the game')


print(f'{business_board.player_list[0].name} goes first.')
business_board.player_list[0].is_turn = True

game_active = True

while game_active:
    for player in business_board.player_list:
        turn_count = 0

        if player.miss_next_chance==True:
          print(player.name,'can not the play this turn')
          player.miss_next_chance=False
          turn_count=1
        else:
            print(f"{player.name}'s turn! Press enter to roll dice.")


        while turn_count<1:
            input()
            if player.last_roll!=0:
              roll1, roll2, movement = player.roll_dice()
              turn_count += 1
              business_board.update_position(player, roll1, roll2, movement)
              current_position = business_board.player_positions[business_board.player_list.index(player)]
              print(f"{player.name} landed on space {current_position}, {business_board.layout[current_position].name}.")
              print('Would you to like to sell any property?')
              response = str(input()).title()
              while response != 'Yes' and response != 'No':
                print("Please enter Yes or No.")
                response = str(input()).title()
              if response=='No' :
                business_board.layout[current_position].interact(player = player, board = business_board)
              else:
                if player.properties==[]:
                  print('You can not sell any property')
                  business_board.layout[current_position].interact(player = player, board = business_board)
                else:
                  print('Properties you own are:')
                  a=[]
                  for i in player.properties:
                    print(i.name, end=', ')
                    a.append(i.name)
                  print('')
                  print('Type the name of property you want to sell')
                  resp=str(input())
                  while resp not in a:
                    print('Please type a valid property name')
                    resp=str(input())
                  for i in player.properties:
                    if i.name==resp:
                      player.properties.pop(player.properties.index(i))
                      i.is_owned=False
                      print('You have successfully sold',i.name,'. You will get a refund of',math.floor(i.cost/200)*100)
                      player.money+=math.floor(i.cost/200)*100
                      player.denominations[3]+=math.floor(i.cost/200)
                      print('After selling',i.name,', you own the following properites')
                      for l in player.properties:
                        print(l.name, end=', ')
                      print('')
                      business_board.layout[current_position].interact(player = player, board = business_board)

            else:
              roll1, roll2, movement = player.roll_dice()
              if movement<=9:
                player.last_roll=0
                print('Sorry, to get started, you need atleast a 10 on your first roll')
                turn_count += 1
              else:
                turn_count += 1
                business_board.update_position(player, roll1, roll2, movement)
                current_position = business_board.player_positions[business_board.player_list.index(player)]
                print(f"{player.name} landed on space {current_position}, {business_board.layout[current_position].name}.")
                business_board.layout[current_position].interact(player = player, board = business_board)
        if player.money<=0:
          print(player.name,'has gone bankrupt')
          b=[]
          for o in business_board.player_list:
            b.append(o.money)
          print('Congrats',business_board.player_list[b.index(max(b))].name,'! You have won the game')
          game_active=False
          break


        else:
          print(f"{player.name} ends their turn with Rs{player.money}.")
    print('If you want to see the current status of the game, enter show, otherwise, enter continue')
    resp=str(input()).title()
    if resp=='Show':
      for i in business_board.player_list:
        print('Name :',i.name)
        print('Properties owned by',i.name,'are:')
        for j in i.properties:
          print(j.name,end=', ')
        print('')
        print(i.name,'has',i.money,'in cash')
        ShowDenomination(i)
        print('5000,1000,500,100 : ',i.denominations)
