# Define a function to handle user input and generate bot responses
def Chat_bot(user_input):
    from Responces import Responses
    R = Responses()
    if "hello" in user_input.lower():
        return "Hi there! How can I help you today?"
    elif "backgammon" in user_input.lower():
        return '''Backgammon is a classic board game that involves strategy, skill, and a bit of luck. Here's a step-by-step guide on how to play Backgammon:
                please tell me what do you want to know
                type: 
                Objective, Setup, Basic Rules, Hitting and Entering, Bearing Off, Winning, Doubling Cube.
                or just type: give me all the rules'''
    elif "give me all the rules" in user_input.lower():
            return R.objective+R.setup+R.basicRules+R.hittingAndEntering+R.bearingOff+R.winning+R.doublingCube
    elif "objective" in user_input.lower():
            return R.objective
    elif "setup" in user_input.lower():
            return R.setup
    elif "basic rules" in user_input.lower():
            return R.basicRules
    elif "hitting and entering" in user_input.lower():
            return R.hittingAndEntering
    elif "bearing off" in user_input.lower():
            return R.bearingOff
    elif "winning" in user_input.lower():
            return R.winning
    elif "doubling cube" in user_input.lower():
            return R.doublingCube
    elif "quit" in user_input.lower():
            return "see you late"
    else:
        return "I'm not sure how to respond to that."

# Main loop for the chat bot
while True:
    user_input = input("You: ")
    bot_response = Chat_bot(user_input)
    print("Bot:", bot_response)
    if user_input.lower() == "quit":
        break
    

