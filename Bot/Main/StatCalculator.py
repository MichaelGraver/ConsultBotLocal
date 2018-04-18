from Bot.models import Sessions

def FirstTopicCalc():
    LocCount = 0
    CostCount = 0
    for i in Sessions.objects.filter(FirstTopic="Location"):
        LocCount +=1
    for i in Sessions.objects.filter(FirstTopic="Cost"):
        CostCount +=1
    if LocCount > CostCount:
        FirstTopic = "Location"
    elif CostCount > LocCount:
        FirstTopic = "Cost"
    else:
        FirstTopic = "Cost and Location are equal"

    return FirstTopic

def LocSentCalc():
    PosLoc = 0
    NegLoc = 0
    for i in Sessions.objects.filter(FirstTopic="Location", FirstSentiment="Positive"):
        PosLoc +=1
    for i in Sessions.objects.filter(SecondTopic="Location", SecondSentiment="Positive"):
        PosLoc +=1
    for i in Sessions.objects.filter(FirstTopic="Location", FirstSentiment="Negative"):
        NegLoc +=1
    for i in Sessions.objects.filter(FirstTopic="Location", FirstSentiment="Negative"):
        NegLoc +=1

    if PosLoc > NegLoc:
        LocSent = "Positive"
    elif NegLoc > PosLoc:
        LocSent = "Negative"
    else:
        LocSent = "The sentiment is equally split"

    return LocSent

def CostSentCalc():
    PosCost = 0
    NegCost = 0
    for i in Sessions.objects.filter(FirstTopic="Cost", FirstSentiment="Positive"):
        PosCost +=1
    for i in Sessions.objects.filter(SecondTopic="Cost", SecondSentiment="Positive"):
        PosCost +=1
    for i in Sessions.objects.filter(FirstTopic="Cost", FirstSentiment="Negative"):
        NegCost +=1
    for i in Sessions.objects.filter(SecondTopic="Cost", SecondSentiment="Negative"):
        NegCost +=1

    if PosCost > NegCost:
        CostSent = "Positive"
    elif NegCost > PosCost:
        CostSent = "Negative"
    else:
        CostSent = "The sentiment is equally split"

    return CostSent


def LocStateCalc():

    Set = {}

    for i in Sessions.objects.filter(FirstTopic="Location"):
        statement = i.FirstStatement
        if statement in Set:
            Set[statement] += 1
        else:
            Set[statement] = 1

    for i in Sessions.objects.filter(SecondTopic="Location"):
        statement = i.SecondStatement
        if statement in Set:
            Set[statement] += 1
        else:
            Set[statement] = 1
    try:
        LocState = max(Set, key=lambda i: Set[i])
    except:
        LocState == "No Statements"

    return LocState

def CostStateCalc():

    Set = {}

    for i in Sessions.objects.filter(FirstTopic="Cost"):
        statement = i.FirstStatement
        if statement in Set:
            Set[statement] += 1
        else:
            Set[statement] = 1

    for i in Sessions.objects.filter(SecondTopic="Cost"):
        statement = i.SecondStatement
        if statement in Set:
            Set[statement] += 1
        else:
            Set[statement] = 1
    try:
        CostState = max(Set, key=lambda i: Set[i])
    except:
        CostState == "No Statements"

    return CostState