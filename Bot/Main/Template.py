from Bot.models import Sessions

def template_gen(sent, topic, Session):
    template = ""
    temp_used = ""
    if sent == "Positive":
        if topic == "Unclear":
            temp_used = "Do you not have any concerns about the cost or the location?"
            template = False
        else:
            temp_used = "So are you not concerned about the " + topic + ". "
            template = True
    elif sent == "Negative":
        if topic == "Unclear":
            temp_used = "What are your concerns about the cost or the location?"
            template = False
        else:
            temp_used = "So you are concerned about the " + topic + ". "
            template = True
    else:
        temp_used = "Sorry I don't understand, please try again. My responses are limited, so unfortunately I can only discuss the cost or location. If your response was about the cost or location I did not understand it."
        template = False
    t = Sessions.objects.get(SessionKey=Session)
    topiccontent = t.Topics
    if topic == "Unclear":
        pass
    elif topic in topiccontent:
        pass
    else:
        t.Topics = (topiccontent + topic)
    
    
    return temp_used