import re, difflib
# Functions for populating the knowledge base
from Bot.Main.SentimentDict import pos_files, neg_files, read_det_file, read_negate_file
#from classify import classify
from Bot.Main.Topic import topic_match
from Bot.Main.Sentiment import sent_match
from Bot.Main.Template import template_gen
from Bot.models import Sessions, Statements

# Generates a list of known determiners
basal_determiner_bank = read_det_file()
# Generates a list of known negators
negators_bank = read_negate_file()
posWords = pos_files()
negWords = neg_files()
# # Text to be parsed
def InputRec(text, Session):
    Reply = "Sorry I don't understand, please try again. My responses are limited, so unfortunately I can only discuss the cost or location. If your response was about the cost or location I did not understand it."
    t = Sessions.objects.get(SessionKey=Session) 
    if t.TopicComplete == False:

        if t.TemplatesUsed == False:
            if t.ReasonGiven == False:
                sent = sent_match(text, posWords, negWords, negators_bank)
                topic = topic_match(text)
                #If the topic or sentiment 
                if topic == "Unclear" or sent == "Neutral":
                    Set = {}
                    for i in Statements.objects.filter():
                        trial = i.statement
                        Score = difflib.SequenceMatcher(None, trial, text).ratio()
                        Set[trial] = Score
                    print(Set)
                    Confidence = max(Set.values())
                    Match = max(Set, key=lambda i: Set[i])
                    if Confidence >= 0.6:
                        ReplySecondHalf = "Why do you think that?"
                        t.CurrentStatement = Match
                        S = Statements.objects.get(statement__icontains=t.CurrentStatement)
                        sentiment = str(S.sentiment)
                        topicset = str(S.topic)
                        if t.FirstStatement == "":
                            t.FirstStatement = Match
                            t.FirstTopic = topicset
                            t.FirstSentiment  = sentiment
                        elif t.SecondStatement == "":
                            t.SecondStatement = Match
                            t.SecondSentiment = sentiment
                            t.SecondTopic = topicset
                        else:
                            pass
                        Reply = ReplySecondHalf
                        t.TemplatesUsed = True
                        t.ReasonGiven = True
                        t.save()
                    elif Confidence < 0.6 and Confidence >= 0.3:
                        
                        Set2 = {}
                        for i in Statements.objects.filter(topic=t.CurrentTopic):
                            Statement2 = i.statement
                            totalmatches = 0
                            total = 0
                            statementlist = i.statement.split()
                            total = len(statementlist)
                            for j in statementlist:
                                if (" " + j + " ") in text:
                                    totalmatches += 1
                                else:
                                    pass
                            Matchpercent = totalmatches/total
                            Set2[Statement2] = Matchpercent
                            Confidence2 = max(Set2.values())
                            Match2 = max(Set2, key=lambda i: Set[i])
                            if Confidence2 >= 0.6:
                                ReplySecondHalf = "Why do you think that?"
                                t.CurrentStatement = Match2
                                S = Statements.objects.get(statement__icontains=t.CurrentStatement)
                                sentiment = str(S.sentiment)
                                topicset = str(S.topic)
                                if t.FirstStatement == "":
                                    t.FirstStatement = Match2
                                    t.FirstSentiment = sentiment
                                    t.FirstTopic = topicset
                                elif t.SecondStatement == "":
                                    t.SecondStatement = Match2
                                    t.SecondSentiment = sentiment
                                    t.SecondTopic = topicset
                                else:
                                    pass
                                Reply = ReplySecondHalf
                                t.TemplatesUsed = True
                                t.ReasonGiven = True
                                t.save()

                    else:
                        if sent == "Positive":
                            Reply = "Why do you think that?"
                            t.TemplatesUsed = True
                            t.ReasonGiven = True
                            t.TopicComplete = True
                            t.save()
                        elif sent == "Negative":
                            Reply = "What do you suggest?"
                            t.TemplatesUsed = True
                            t.ReasonGiven = True
                            t.TopicComplete = True
                            t.save()
                #If topic and sentiment can be assessed do this
                else:
                    TopicsInList = t.Topics
                    t.Topics = (TopicsInList + topic)
                    t.CurrentTopic = topic
                    if t.FirstTopic == "":
                        t.FirstTopic = topic
                        t.FirstSentiment = sent
                    elif t.SecondTopic == "":
                        t.SecondTopic = topic
                        t.SecondSentiment = sent
                    else:
                        pass
                    t.save()
                    ReplyFirstHalf = template_gen(sent, topic, Session)
                    if ReplyFirstHalf == "Sorry I don't understand, please try again. My responses are limited, so unfortunately I can only discuss the cost or location. If your response was about the cost or location I did not understand it.":
                        Reply = ReplyFirstHalf
                    elif ReplyFirstHalf == "What are your concerns about the cost or the location?":
                        Reply = ReplyFirstHalf
                    elif ReplyFirstHalf == "Do you not have any concerns about the cost or the location?":
                        Reply = ReplyFirstHalf  
                    else:
                        Set = {}
                        for i in Statements.objects.filter(sentiment=sent):
                            trial = i.statement
                            Score = difflib.SequenceMatcher(None, trial, text).ratio()
                            Set[trial] = Score
                        print(Set)
                        Confidence = max(Set.values())
                        Match = max(Set, key=lambda i: Set[i])
                        if Confidence >= 0.6:
                            ReplySecondHalf = ("Why do you think that " + str(Match) + "?")
                            t.CurrentStatement = Match
                            if t.FirstStatement == "":
                                t.FirstStatement = Match
                            elif t.SecondStatement == "":
                                t.SecondStatement = Match
                            else:
                                pass
                            Reply = ReplyFirstHalf + ReplySecondHalf
                            t.TemplatesUsed = True
                            t.ReasonGiven = True
                            t.save()
                        elif Confidence < 0.6 and Confidence >= 0.3:
                            
                            Set2 = {}
                            for i in Statements.objects.filter(topic=t.CurrentTopic):
                                Statement2 = i.statement
                                totalmatches = 0
                                total = 0
                                statementlist = i.statement.split()
                                total = len(statementlist)
                                for j in statementlist:
                                    if (" " + j + " ") in text:
                                        totalmatches += 1
                                    else:
                                        pass
                                Matchpercent = totalmatches/total
                                Set2[Statement2] = Matchpercent
                                Confidence2 = max(Set2.values())
                                Match2 = max(Set2, key=lambda i: Set[i])
                                if Confidence2 >= 0.6:
                                    ReplySecondHalf = ("Why do you think that " + str(Match2) + "?")
                                    t.CurrentStatement = Match2
                                    if t.FirstStatement == "":
                                        t.FirstStatement = Match2
                                    elif t.SecondStatement == "":
                                        t.SecondStatement = Match2
                                    else:
                                        pass
                                    Reply = ReplyFirstHalf + ReplySecondHalf
                                    t.TemplatesUsed = True
                                    t.ReasonGiven = True
                                    t.save()

                        else:
                            S = Statements.objects.get(statement__icontains=t.CurrentStatement)
                            sentiment = str(S.sentiment)
                            if sent == "Positive":
                                Reply = "Why do you think that?"
                                t.TemplatesUsed = True
                                t.ReasonGiven = True
                                t.TopicComplete = True
                                t.save()
                            else:
                                Reply = "What do you suggest?"
                                t.TemplatesUsed = True
                                t.ReasonGiven = True
                                t.TopicComplete = True
                                t.save()
                            
            

        elif t.TemplatesUsed == True: 

            if t.ReasonGiven == True:  
                    S = Statements.objects.get(statement__icontains=t.CurrentStatement)
                    link = S.counters
                    T = Statements.objects.get(id=link)
                    if T.response == "False":
                        Reply = ("Do you not think " + str(T.statement) + "?")
                        t.ReasonGiven = False
                       
                        t.save()
                    else:
                        Reply = str(T.response)
                        t.ReasonGiven = False
                        
                        
                        t.save()

            else:
                S = Statements.objects.get(statement__icontains=t.CurrentStatement)
                sentiment = str(S.sentiment)
                if sentiment == "Positive":
                    Reply = "Why do you think that?"
                    t.TemplatesUsed = True
                    t.ReasonGiven = True
                    t.TopicComplete = True
                    t.CurrentStatement = ""
                    t.save()
                else:
                    Reply = "What do you suggest?"
                    t.TemplatesUsed = True
                    t.ReasonGiven = True
                    t.TopicComplete = True
                    t.CurrentStatement = ""
                    t.save()
    elif t.TopicComplete == True:
        topicsused = t.Topics
        if topicsused == "Cost":
            NextTopic = "Location"
            Reply = ("Thank you for your response. What about the " + NextTopic + "?" + '\n' + " If you have no other concerns select End to stop.")
        elif topicsused == "Location":
            NextTopic = "Cost"
            Reply = ("Thank you for your response. What about the " + NextTopic + "?" + '\n' + "If you have no other concerns select End to stop.")
        else:
            Reply = "Thank you for taking part, please select End to be taken to the questionnaire"
        t.TemplatesUsed = False
        t.ReasonGiven = False
        t.TopicComplete = False
        t.CurrentTopic = ""
        t.save()
    else:
        Reply = "Sorry I don't understand, please try again. My responses are limited, so unfortunately I can only discuss the cost or location. If your response was about the cost or location I did not understand it."
    
    return Reply

			