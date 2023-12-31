#written by Mark Shperkin
def Chat_bot(user_input):
    import subprocess
    from Responces import Responses
    from TopicDetector import CheckTopic
    R = Responses()
    topic = CheckTopic(user_input)
    if topic == "hello":
        return "Hi there! How can I help you today?"
    elif topic == "backgammon":
        return R.intro
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
    elif "play" in user_input.lower():
            
            print(" please type 'computer' for playing agaist the computer\nor type 'friend' to play against a friend")
            user_input = input("You: ")

            if "computer" in user_input.lower():
                try:
                    subprocess.run(['python', 'backgammon/single_player.py'], check=True)
                    return "Game started successfully."
                except subprocess.CalledProcessError as e:
                    return f"Error starting the game: {e}"  
            elif "friend" in user_input.lower():
                try:
                    subprocess.run(['python', 'backgammon/two_player.py'], check=True)
                    return "Game started successfully."
                except subprocess.CalledProcessError as e: 
                    return f"Error starting the game: {e}"
            else:
                return "please try again"
    elif topic == "you":
            return "I am a non AI chat-bot.\nMy only goal is to teach anyone how to play backgammon."
    elif topic == "feel":
            return '''my creator designed me to be as human as posible but I cannotyou feel anything.
        I am an early production, and maybe in the future I will have feelings and emotions.
        Thank you for asking :)'''
    elif topic == "quit":
            return "see you later"
    else:
        return "I'm not sure how to respond to that.\nplease try again"

# Main loop for the chat bot
while True:
        
    user_input = input("You: ")
    bot_response = Chat_bot(user_input)
    print("Bot:", bot_response)
    from TopicDetector import CheckTopic
    topic = CheckTopic(user_input)
    if topic == "quit":
        break


