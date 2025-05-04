import tkinter as tk #for visuals
import random #going to be used for generating the target number

#CONSTANTS
KEY = 4 #encrytion aspect
MAX_ATTEMPTS = 3 #user gets three attempts to guess the code of the safe
TARGET_RANGE = (1,50) #range that the target could be
TIMER_MODE_RANGE = (1,100) #larger target range for the timer mode
TIME = 60

class SafeCracker:
    
    #initialization function
    def __init__(self, window):
        self.window = window
        self.window.title("Crack that Safe") #title of the window/game
        self.tries = 0 #starts the game where the user has not used up any tries yet

        self.timer_count = None #initializes the timer count
        self.remaining_timer = TIME #sets the timer mode's time
        self.game_on = False #makes sure that the game will stop when the timer ends

        self.make_visuals() #gonna create the buttons & labels (visuals)

    # function to create the titles and buttons for the game
    def make_visuals(self):
        #sets up the game title
        self.game_title = tk.Label(self.window, text="Crack That Safe!", font=("Roboto", 20, "bold"))
        self.game_title.pack(pady=15)

        #text showing how much of the timer is left
        self.timer = tk.Label(self.window, text="", font=("Roboto", 15, "bold"))
        self.timer.pack(pady=15)

        #text having the user choose what type of game mode they'll play
        self.subtitle = tk.Label(self.window, text="To play, choose a mode", font=("Roboto", 15))
        self.subtitle.pack(pady=5)

        #makes the button to make the game go into timed mode
        self.timer_button = tk.Button(self.window, text="Timer Mode (1m)", command=lambda: self.start_game("timer"))
        self.timer_button.pack(pady=10)
        
        #makes the button to make the game go into normal mode (three guesses)
        self.normal_button = tk.Button(self.window, text="Normal Mode (3 guesses)", command=lambda: self.start_game("normal"))
        self.normal_button.pack(pady=10)

        #sets up the user input
        self.user_input = tk.Entry(self.window)
        self.user_input.pack()

        #makes the button for user to submit a guess
        #when button's pressed, the check() function will run
        self.submit_button = tk.Button(self.window, text="Submit", command=self.check)
        self.submit_button.pack(pady=15)

        #will show the user whether their guess was correct, or if not, whether it was too low or too high
        self.result = tk.Label(self.window, text="")
        self.result.pack(pady=10)

        #makes the button for the user to reset the game
        self.play_again_button = tk.Button(self.window, text="Play again!", command=self.reset, state=tk.DISABLED)
        self.play_again_button.pack(pady=20)

    # function to switch between the two modes
    def start_game(self, game_type):
        #initializing everything
        self.game_type = game_type
        self.tries = 0
        self.result.config(text="")
        self.user_input.delete(0, tk.END)
        self.submit_button.config(state=tk.NORMAL) #enables the submit button for the game starting
        self.play_again_button.config(state=tk.DISABLED) #disables the play again button until the game ends
        self.game_on = True 

        if game_type == "normal":
            self.target = random.randint(*TARGET_RANGE) #sets up the target number for normal mode
        else:
            self.target = random.randint(*TIMER_MODE_RANGE) #sets up the target number for timer mode
            self.remaining_timer = TIME #sets up the timer's time
            self.update_timer() #calls the update timer function to run the active timer 
        
        self.encrypted_target = self.target + KEY

        #changes the subtitle depending on the game mode
        if game_type == "normal":
            #sets up the subtitle that has a quick instructional sentence for the user
            self.subtitle.config(text=f"Guess a number between {TARGET_RANGE[0]} and {TARGET_RANGE[1]} to try to crack the safe")
        else:
            self.subtitle.config(text=f"Guess a number between {TIMER_MODE_RANGE[0]} and {TIMER_MODE_RANGE[1]} to try to crack the safe")

    # function that updates the timer
    def update_timer(self):
        if self.remaining_timer > 0 and self.game_on:
            self.timer.config(text=f"Time remaining: {self.remaining_timer}s")
            self.remaining_timer -= 1
            self.timer_count = self.window.after(1000, self.update_timer)
        elif self.game_type == "timer" and self.game_on:
            self.timer.config(text="Time is up!")
            self.result.config(text=f"You didn't crack the safe :( . The safe's code was {self.target}. Play again!")
            self.end()

    # function to check the user's guess against the encryted target
    def check(self):
        #doesn't check if the timer isn't running
        if not self.game_on:
            return

        try: 
            user_guess = int(self.user_input.get()) #converts the user's guess to an integer
            encrypted_guess = user_guess + KEY #adds the encryption key to the guess to compare it with the encrypted target
            
            #user guesses correctly
            if encrypted_guess == self.encrypted_target:
                self.result.config(text="You cracked the safe!! Congratulations on this amazing achievement!")
                self.end() #calls end() function to terminate the game
                return
            #user guesses too high
            elif encrypted_guess > self.encrypted_target:
                self.result.config(text="Your guess is too high! Try again.")
            #user guesses too low
            else:
                self.result.config(text="Your guess is to low! Try again.")
                
            #user reaches max attempts (3 guesses) and their last guess isn't the target
            if self.game_type == "normal":
                self.tries += 1 #updates the tries count 
                if self.tries == MAX_ATTEMPTS and encrypted_guess != self.encrypted_target:
                    self.result.config(text=f"You didn't crack the safe :( . The safe's code was {self.target}. Play again!")
                    self.end()
        except ValueError:
            self.result.config(text="Enter a number within the range.")

    # function to end the game
    def end(self):
        self.submit_button.config(state=tk.DISABLED) #disables the submit button until the play again button is pressed
        self.play_again_button.config(state=tk.NORMAL) #enables the play again button
        self.game_on = False #turns off the game
        if self.timer_count:
            self.window.after_cancel(self.timer_count)


    # function to reset the game so the user can play again
    def reset(self):
        self.user_input.delete(0, tk.END) #deletes the user input stored
        self.result.config(text="") #resets the result string so it's empty for the new game to start
        self.timer.config(text="") #resets the timer string
        self.subtitle.config(text="Choose a game mode to play")

        self.submit_button.config(state=tk.NORMAL) #reactivates the submit button so it can be pressed now
        self.play_again_button.config(state=tk.DISABLED) #disbales the reset button so it cannot be pressed again until the game is over again
        self.game_on = False

        if self.timer_count:
            self.window.after_cancel(self.timer_count)
            self.timer_count = None


# runs the program
if __name__ == "__main__":
    window = tk.Tk()
    safe_game = SafeCracker(window)
    window.mainloop()