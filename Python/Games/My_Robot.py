""" 
Prove 3 
Vivian Ashton 
Make a robot that have the following attributes 
    -x-coordinate
    -y-coordinate
    -fuel amount
and can do the following things
    -move left right up and down
    -display it's current status
    -fire it's laser


other things I want to add or fix:
    -randomize the location of the iteams 
    -add an inspect action
    -jumpin over fuel

"""

class Robot:

    def __init__(self):
        self.x_coordinate = 10
        self.y_coordinate = 10
        self.fuel_amount = 100
        self.command = ""
    
    def move_left(self):
        if (self.x_coordinate - 1) <= 0 or (self.x_coordinate - 1) > 10:
            print("Can't go that way. You'll fall off a cliff.") 
        elif (self.fuel_amount - 5) >= 0:
            self.x_coordinate -= 1
            self.fuel_amount -=5
        else:
            print("Insufficient fuel to perform action.")

    def move_right(self):
        if (self.x_coordinate + 1) <= 0 or (self.x_coordinate + 1) > 10:
            print("Can't go that way. You'll fall off a cliff.")
        elif (self.fuel_amount - 5) >= 0:
            self.x_coordinate += 1
            self.fuel_amount -= 5
        else:
            print("Insufficient fuel to perform action.")

    def move_up(self):
        if (self.y_coordinate - 1) <= 0 or (self.y_coordinate - 1) > 10:
            print("Can't go that way. You'll fall off a cliff.")
        elif (self.fuel_amount - 5) >= 0:
            self.y_coordinate -= 1
            self.fuel_amount -= 5
        else:
            print("Insufficient fuel to perform action.")

    def move_down(self):
        if (self.y_coordinate + 1) <= 0 or (self.y_coordinate + 1) > 10:
            print("Can't go that way. You'll fall off a cliff.")
        elif (self.fuel_amount - 5) >= 0:
            self.y_coordinate += 1
            self.fuel_amount -= 5
        else:
            print("Insufficient fuel to perform action.")

    def display_status(self):
        print(f"({self.x_coordinate}, {self.y_coordinate}) - Fuel: {self.fuel_amount}")
        
    def fire_laser(self):
        if (self.fuel_amount - 5) >= 10:
            print("PEW! PEW!")
            self.fuel_amount -= 15
        else:
            print("Insufficient fuel to perform action.") 

    def refuel(self):
        self.fuel_amount = 100

    def inspect(self):
        self.fuel_amount -= 5

    def left_jump(self):
        if (self.x_coordinate - 2) <= 0 or (self.x_coordinate - 2) > 10:
            print("Can't go that way. You'll fall off a cliff.")
        elif (self.fuel_amount - 10) >= 0: 
            self.x_coordinate -= 2
            self.fuel_amount -= 10
        else:
            print("Insufficient fuel to perform action")

    def right_jump(self):
        if (self.x_coordinate + 2) <= 0 or (self.x_coordinate + 2) > 10:
            print("Can't go that way. You'll fall off a cliff.")
            
        elif (self.fuel_amount - 10) >= 0:
            self.x_coordinate += 2
            self.fuel_amount -= 10
        else:
            print("Insufficient fuel to perform action")
    
    def up_jump(self):
        if (self.y_coordinate - 2) <= 0 or (self.y_coordinate - 2) > 10:
            print("Can't go that way. You'll fall off a cliff.")

        elif (self.fuel_amount - 10) >= 0:
            self.y_coordinate -= 2
            self.fuel_amount -= 10
        else:
            print("Insufficient fuel to perform action")

    def down_jump(self):
        if (self.y_coordinate - 2) <= 0 or (self.y_coordinate - 2) > 10:
            print("Can't go that way. You'll fall off a cliff.")

        elif (self.fuel_amount - 10) >= 0:
            self.y_coordinate += 2
            self.fuel_amount -= 10
        else:
            print("Insufficient fuel to perform action.")
   
class Iteams:
    
    def __init__(self):
        self.bomb_x = 8
        self.bomb_y = 9
        self.fuel_1x = 10
        self.fuel_1y = 5
        self.camera_x = 3
        self.camera_y = 4 
        self.rock_1x = 6
        self.rock_1y = 6
        #self.player_name = given_name

    # def detonate():
    #     print("BOOM!")
    #     print("You ecountered a bomb and it blew you up!")
    #     print("Game Over.")
    #     return "quit" # may or may not want this here

    def finish(self):
        print("Good Job! You found the camera and finsihed the game!")
        return "quit"

    def remove_rock(self):
        print("The rock has been destroyed")
        self.rock_1x = 0
        self.rock_1y = 0

    def refueled(self):
        #print("You found fuel!")
        print("Your tank is full again!")
        self.fuel_1x = 0
        self.fuel_1y = 0
    
    def blow_up_fuel(self):
        print("You blew up some fuel")
        self.fuel_1x = 0
        self.fuel_1y = 0
        


def detonate():
    print("BOOM!")
    print("You ecountered a bomb and it blew you up!")
    print("Game Over.")
    return "quit" # may or may not want this here

def request_name():
    return input("Please name your robot: ")

def encounter():
    print("")
    print("You have encountered and object.")
    print("What action do you want to take?: ")
    print("")
    print("Jump over the object - jump")
    print("Fire lazer at the object - fire")
    #print("Inspect the object - inspect")
    print("Collect the object - collect")
    print("Go around the object - around")
    print("")
    return input("Enter command: ")

# the reactions of the encounter for each direction

def left_reaction(command, iteams, robot, command2):
    robot.command = command

    if command2 == "jump" and (robot.x_coordinate - 1)!= iteams.rock_1x and robot.y_coordinate != iteams.rock_1y:
        robot.left_jump()
    elif command2 == "fire" and (robot.x_coordinate - 1) == iteams.rock_1x and robot.y_coordinate == iteams.rock_1y:
        robot.fire_laser()
        iteams.remove_rock()
    elif command2 == "fire" and (robot.x_coordinate - 1) == iteams.bomb_x and robot.y_coordinate == iteams.bomb_y:
        robot.fire_laser()
        command = detonate()
        return command 
    elif command2 == "fire" and (robot.x_coordinate - 1) == iteams.fuel_1x and robot.y_coordinate == iteams.fuel_1y:
        robot.fire_laser()
        iteams.blow_up_fuel()
    elif command2 == "fire" and (robot.x_coordinate - 1) == iteams.camera_x and robot.y_coordinate == iteams.camera_y:
        robot.fire_laser()
        print("You blew up the camera!")
        print("Game Over")
        print("")
        return "quit"
    elif command2 == "collect" and (robot.x_coordinate - 1) == iteams.rock_1x and robot.y_coordinate == iteams.rock_1y:
        print("Unable to collect")
        print("what direction do you want to go?")
    elif command2 == "collect" and (robot.x_coordinate - 1) == iteams.fuel_1x and robot.y_coordinate == iteams.fuel_1y:
        iteams.refueled()
        robot.refuel()
    elif command2 == "collect" and (robot.x_coordinate  - 1) == iteams.bomb_x and robot.y_coordinate == iteams.bomb_y:
        command = detonate()
        return command 
    elif command2 == "collect" and (robot.x_coordinate - 1)== iteams.camera_x and robot.y_coordinate == iteams.camera_y:
        command = iteams.finish()
        return command
    elif command2 == "around":
        print("What direction do you want to go?")
    else:
        print("Invalid command")
        print("What direction do you want to go?")
        return command

def right_reaction(command, iteams, robot, command2):
    robot.command = command

    if command2 == "jump" and (robot.x_coordinate + 1)!= iteams.rock_1x and robot.y_coordinate != iteams.rock_1y:
        robot.right_jump()
    elif command2 == "fire" and (robot.x_coordinate + 1)== iteams.rock_1x and robot.y_coordinate == iteams.rock_1y:
        robot.fire_laser()
        iteams.remove_rock()
    elif command2 == "fire" and (robot.x_coordinate + 1)== iteams.bomb_x and robot.y_coordinate == iteams.bomb_y:
        robot.fire_laser()
        command = detonate()
        return command
    elif command2 == "fire" and (robot.x_coordinate + 1)== iteams.fuel_1x and robot.y_coordinate == iteams.fuel_1y:
        robot.fire_laser()
        iteams.blow_up_fuel()
    elif command2 == "fire" and (robot.x_coordinate + 1) == iteams.camera_x and robot.y_coordinate == iteams.camera_y:
        robot.fire_laser()
        print("You blew up the camera!")
        print("Game Over")
        print("")
        return "quit"
    elif command2 == "collect" and (robot.x_coordinate + 1)== iteams.rock_1x and robot.y_coordinate == iteams.rock_1y:
        print("Unable to collect")
        print("what direction do you want to go?")
    elif command2 == "collect" and (robot.x_coordinate + 1)== iteams.fuel_1x and robot.y_coordinate == iteams.fuel_1y:
        iteams.refueled()
        robot.refuel()
    elif command2 == "collect" and (robot.x_coordinate + 1) == iteams.bomb_x and robot.y_coordinate == iteams.bomb_y:
        command = detonate()
        return command
    elif command2 == "collect" and (robot.x_coordinate + 1) == iteams.camera_x and robot.y_coordinate == iteams.camera_y:
        command = iteams.finish()
        return command
    elif command2 == "around":
        print("What direction do you want to go?")
    else:
        print("Invalid command")
        print("What direction do you want to go?")
        return command

def down_reaction(command, iteams, robot, command2):
    robot.command = command

    if command2 == "jump" and robot.x_coordinate != iteams.rock_1x and (robot.y_coordinate + 1) != iteams.rock_1y:
        robot.down_jump()
    elif command2 == "fire" and robot.x_coordinate == iteams.rock_1x and (robot.y_coordinate + 1) == iteams.rock_1y:
        robot.fire_laser()
        iteams.remove_rock()
    elif command2 == "fire" and robot.x_coordinate == iteams.bomb_x and (robot.y_coordinate + 1)== iteams.bomb_y:
        robot.fire_laser()
        command = detonate()
        return command
    elif command2 == "fire" and robot.x_coordinate == iteams.fuel_1x and (robot.y_coordinate + 1) == iteams.fuel_1y:
        robot.fire_laser()
        iteams.blow_up_fuel()
    elif command2 == "fire" and robot.x_coordinate == iteams.camera_x and (robot.y_coordinate + 1) == iteams.camera_y:
        robot.fire_laser()
        print("You blew up the camera!")
        print("Game Over")
        print("")
        return "quit"
    elif command2 == "collect" and robot.x_coordinate == iteams.rock_1x and (robot.y_coordinate + 1)== iteams.rock_1y:
        print("Unable to collect")
        print("what direction do you want to go?")
    elif command2 == "collect" and robot.x_coordinate == iteams.fuel_1x and (robot.y_coordinate + 1)== iteams.fuel_1y:
        iteams.refueled()
        robot.refuel()
    elif command2 == "collect" and robot.x_coordinate == iteams.bomb_x and (robot.y_coordinate + 1)== iteams.bomb_y:
        return detonate()
    elif command2 == "collect" and robot.x_coordinate == iteams.camera_x and (robot.y_coordinate + 1)== iteams.camera_y:
        command = iteams.finish()
        return command
    elif command2 == "around":
        print("What direction do you want to go?")
    else:
        print("Invalid command")
        print("What direction do you want to go?")
        return command

def up_reaction(command, iteams, robot, command2):
    robot.command = command
    #while command2 == "around" or "jump" or "fire" or "collect":
        #print("What dicrection?")

    if command2 == "jump" and robot.x_coordinate != iteams.rock_1x and (robot.y_coordinate - 1) != iteams.rock_1y:
        robot.up_jump()
    elif command2 == "fire" and robot.x_coordinate == iteams.rock_1x and (robot.y_coordinate - 1) == iteams.rock_1y:
        robot.fire_laser()
        iteams.remove_rock()
    elif command2 == "fire" and robot.x_coordinate == iteams.bomb_x and (robot.y_coordinate - 1) == iteams.bomb_y:
        robot.fire_laser()
        command = detonate()
        return command
    elif command2 == "fire" and robot.x_coordinate == iteams.fuel_1x and (robot.y_coordinate - 1) == iteams.fuel_1y:
        robot.fire_laser()
        iteams.blow_up_fuel()
    elif command2 == "fire" and robot.x_coordinate == iteams.camera_x and (robot.y_coordinate - 1) == iteams.camera_y:
        robot.fire_laser()
        print("You blew up the camera!")
        print("Game Over")
        print("")
        return "quit"
    elif command2 == "collect" and robot.x_coordinate == iteams.rock_1x and (robot.y_coordinate - 1) == iteams.rock_1y:
        print("Unable to collect")
        print("what direction do you want to go?")
    elif command2 == "collect" and robot.x_coordinate == iteams.fuel_1x and (robot.y_coordinate - 1) == iteams.fuel_1y:
        iteams.refueled()
        robot.refuel()
    elif command2 == "collect" and robot.x_coordinate == iteams.bomb_x and (robot.y_coordinate - 1) == iteams.bomb_y:
        command = detonate()
        return command
    elif command2 == "collect" and robot.x_coordinate == iteams.camera_x and (robot.y_coordinate - 1) == iteams.camera_y:
        command = iteams.finish()
        return command
    elif command2 == "around":
        print("What direction do you want to go?")
    else:
        print("Invalid command")
        print("What direction do you want to go?")
        return command

# the welcome display
def display_welcome():
    print("Help your robot find his missing camera before his fuel runs out. You can't see without it.")

# menu of actions
def display_menu(given_name):
    print(f"Give {given_name} a command: ")
    print("To move to the left type: left")
    print("To move to the right type: right")
    print("To move to the up type: up")
    print("To move to the down type: down")
    print("To check location and fuel status type: status")
    print("To fire lazer type: fire")
    print("To quit game type: quit")

# the actions taken after getting a command for a direction
def action_left(robot, iteams, command):
    if (robot.x_coordinate - 1) == iteams.bomb_x and robot.y_coordinate == iteams.bomb_y:
        command2 = encounter()
        command = left_reaction(command, iteams, robot, command2)
        return command
    elif (robot.x_coordinate - 1) == iteams.rock_1x and robot.y_coordinate == iteams.rock_1y:
        command2 = encounter()
        command = left_reaction(command, iteams, robot, command2)
        return command
    elif (robot.x_coordinate - 1) == iteams.fuel_1x and robot.y_coordinate == iteams.fuel_1y:
        command2 = encounter()
        command = left_reaction(command, iteams, robot, command2)
        return command
    elif (robot.x_coordinate - 1) == iteams.camera_x and robot.y_coordinate == iteams.camera_y:
        command2 = encounter()
        command = left_reaction(command, iteams, robot, command2)
        return command
    else:
        robot.move_left()
    return command

def action_right(robot, iteams, command):
    if (robot.x_coordinate + 1) == iteams.bomb_x and robot.y_coordinate == iteams.bomb_y:
        command2 = encounter()
        command = right_reaction(command, iteams, robot, command2)
        return command
    elif (robot.x_coordinate + 1) == iteams.rock_1x and robot.y_coordinate == iteams.rock_1y:
        command2 = encounter()
        command = right_reaction(command, iteams, robot, command2)
        return command
    elif (robot.x_coordinate + 1) == iteams.fuel_1x and robot.y_coordinate == iteams.fuel_1y:
        command2 = encounter()
        command = right_reaction(command, iteams, robot, command2)
        return command
    elif (robot.x_coordinate + 1) == iteams.camera_x and robot.y_coordinate == iteams.camera_y:
        command2 = encounter()
        command = right_reaction(command, iteams, robot, command2)
        return command
    else:
        robot.move_right()
    return command

def action_down(robot, iteams, command):
    if (robot.y_coordinate + 1) == iteams.bomb_y and robot.x_coordinate == iteams.bomb_x:
        command2 = encounter()
        command = down_reaction(command, iteams, robot, command2)
        return command
    elif (robot.y_coordinate + 1) == iteams.rock_1y and robot.x_coordinate == iteams.rock_1x:
        command2 = encounter()
        command = down_reaction(command, iteams, robot, command2)
        return command
    elif (robot.y_coordinate + 1) == iteams.fuel_1y and robot.x_coordinate == iteams.fuel_1x:
        command2 = encounter()
        command = down_reaction(command, iteams, robot, command2)
        return command
    elif (robot.y_coordinate + 1) == iteams.camera_y and robot.x_coordinate == iteams.camera_x:
        command2 = encounter()
        command = down_reaction(command, iteams, robot, command2)
        return command
    else:
        robot.move_down()
    return command

def action_up(robot, iteams, command):
    if (robot.y_coordinate - 1) == iteams.bomb_y and robot.x_coordinate == iteams.bomb_x:
        command2 = encounter()
        command = up_reaction(command, iteams, robot, command2)
        return command
    elif (robot.y_coordinate - 1) == iteams.rock_1y and robot.x_coordinate == iteams.rock_1x:
        command2 = encounter()
        command = up_reaction(command, iteams, robot, command2)
        return command
    elif (robot.y_coordinate - 1) == iteams.fuel_1y and robot.x_coordinate == iteams.fuel_1x:
        command2 = encounter()
        command = up_reaction(command, iteams, robot, command2)
        return command
    elif (robot.y_coordinate - 1) == iteams.camera_y and robot.x_coordinate == iteams.camera_x:
        command2 = encounter()
        command = up_reaction(command, iteams, robot, command2)
        return command
    else:
        robot.move_up()
    return command

## All actions taken
def action(robot, iteams, given_name):
    command = input("Enter command: ")
    if command == "left":
        return action_left(robot, iteams, command)
    elif command == "right":
        return action_right(robot, iteams, command)
    elif command == "up":
        return action_up(robot, iteams, command)
    elif command == "down":
        return action_down(robot, iteams, command)
    elif command == "fire": #change to fire
        robot.fire_laser()
    elif command == "status":
        robot.display_status()
    elif command == "quit":
        print("Goodbye")
    else:
        print("")
        print("Invaild command.")
        display_menu(given_name)
        print("")
    return command

# running the thing 
def main():
    print("")
    display_welcome()
    robot_name = request_name()
    print("")

    display_menu(robot_name)
    print("")

    robot = Robot()
    iteams = Iteams()
    command = "start"
    
    while command != "quit":
        command = action(robot, iteams, robot_name)
        if robot.fuel_amount == 0:
            print("Your out of fuel! ")
            print("")
            print("Game Over")
            command = "quit"
        #print(command)
        #robot.display_status()



if __name__ == "__main__":
    main()