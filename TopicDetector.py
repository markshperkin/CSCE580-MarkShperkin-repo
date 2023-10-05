#written by Mark Shperkin
def CheckTopic(user_input):
    greatings_keywords = {"hello","hi","hey"}
    quit_keywords = {"quit","exit","stop","kill","die","q"}
    generalQuestions_keywords = {"how are you","how you doing","whats up","how do you do","whats up with it"}
    user_input = user_input.lower()
    for keywords in greatings_keywords:
            if keywords in user_input:
                    return "hello"
    for keywords in quit_keywords:
        if keywords in user_input:
                return "quit"
    for keywords in generalQuestions_keywords:
        if keywords in user_input:
            return "feel"
    if "backgammon" in user_input:
            return "backgammon"
    if "you" in user_input:
        return "you"
    
    return "general"
        