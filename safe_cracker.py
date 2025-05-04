import tkinter as tk #for visuals
import random #going to be used for generating the target number

#CONSTANTS
KEY = 4 #encrytion aspect
MAX_ATTEMPTS = 3 #user gets three attempts to guess the code of the safe
TARGET_RANGE = (1,50) #range that the target could be

class SafeCracker:
    
    #initialization function
    def __init__(self, window):
        self.window = window
        self.window.title("Crack that Safe") #title of the window/game
        self.tries = 0 #starts the game where the user has not used up any tries yete
        self.target = random.randint(*TARGET_RANGE) #sets up the target number
        self.encrypted_target = self.target + KEY

        self.make_visuals() #gonna create the buttons & labels (visuals)

    # function to create the titles and buttons for the game
    def make_visuals(self):
        #sets up the game title
        self.game_title = tk.Label(self.window, text="Crack That Safe!", font=("Roboto", 20, "bold"))
        self.game_title.pack(pady=15)

        #sets up the subtitle that has a quick instructional sentence for the user
        self.subtitle = tk.Label(self.window, text=f"Guess a number between {TARGET_RANGE[0]} and {TARGET_RANGE[1]} to try to crack the safe")
        self.subtitle.pack(pady=5, padx=10)

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

    # function to check the user's guess against the encryted target
    def check(self):
        try: 
            user_guess = int(self.user_input.get()) #converts the user's guess to an integer
            self.tries += 1 #updates the tries count 

            if self.tries > MAX_ATTEMPTS: 
                self.result.config(text=f"You didn't crack the safe :( . The safe's code was {self.target}. Play again!")
                self.end() #calls the end() function to terminate the game
                return
            
            encrypted_guess = user_guess + KEY #adds the encryption key to the guess to compare it with the encrypted target

            #user guesses correctly
            if encrypted_guess == self.encrypted_target:
                self.result.config(text="You cracked the safe!! Congratulations on this amazing achievement!")
                self.end() #calls end() function to terminate the game
            #user guesses too high
            elif encrypted_guess > self.encrypted_target:
                self.result.config(text="Your guess is too high! Try again.")
            #user guesses too low
            else:
                self.result.config(text="Your guess is to low! Try again.")
            
            #user reaches max attempts (3 guesses) and their last guess isn't the target
            if self.tries == MAX_ATTEMPTS and encrypted_guess != self.encrypted_target:
                self.result.config(text=f"You didn't crack the safe :( . The safe's code was {self.target}. Play again!)")
                self.end()

        except ValueError:
            self.result.config(text="Enter a number within the range.")

    # function to end the game
    def end(self):
        self.submit_button.config(state=tk.DISABLED) #disables the submit button until the play again button is pressed
        self.play_again_button.config(state=tk.NORMAL)

    # function to reset the game so the user can play again
    def reset(self):
        self.tries = 0 #resets the guess count
        self.target = random.randint(*TARGET_RANGE) #resets the target to a new randomly generated number
        self.encrypted_target = self.target + KEY #readds the encryption to get a newly encrypted target number
        self.user_input.delete(0, tk.END) #deletes the user input stored
        self.result.config(text="") #resets the result string so it's empty for the new game to start
        self.submit_button.config(state=tk.NORMAL) #reactivates the submit button so it can be pressed now
        self.play_again_button.config(state=tk.DISABLED) #disbales the reset button so it cannot be pressed again until the game is over again

# runs the program
if __name__ == "__main__":
    window = tk.Tk()
    safe_game = SafeCracker(window)
    window.mainloop()