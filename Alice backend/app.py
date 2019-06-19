
from flask import Flask, render_template, request
from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer
import testsentinet as s

app = Flask(__name__)

english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")

#english_bot.set_trainer(ChatterBotCorpusTrainer)
#english_bot.train("chatterbot.corpus.english")

b= '<span style="color: #024a02;">💻︎Alice: </span> '
flag=0
flag2=0
#question counter
i=-1
#total sentiment
total=0
#conituous adding usertext sentiment result
sentiment=0
#user input counter
uc=0
ucrs=0
#re start flag
rflag=0
pos=0
neg=0
j=0

@app.route("/")
def home():
    global total
    global flag
    global flag2
    global i
    global sentiment
    global uc
    global pos
    global neg
    global j
    pos=0
    neg=0
    flag=0
    flag2=0
    #question counter
    i=-1
    #total sentiment
    total=0
    #conituous adding usertext sentiment result
    sentiment=0
    #user input counter
    uc=0
    j=0
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    
    global total
    global flag
    global flag2
    global i
    global sentiment
    global uc
    global pos
    global neg
    global j
    question1 = "Upcoming questions are simple 'YES' or 'NO' questions.Please give you answer in 'YES' or 'NO'<br>Do you want to continue?(yes/no)"
    question2 = "Do you have little pleasure or interest in doing things?"
    question = ["Do you feel hopeless or down?","Do you have trouble sleeping, either sleeping too much or not at all?","Do you feel tired or have little energy?","Do you overeat or have a poor appetite?","Do you feel like a failure or you've let people down?","Do you have trouble concentrating?","Do you have any harmful thoughts towards yourself?"]
    userText = request.args.get('msg')
    
    
    
    if userText != 'Bye' and flag == 0 and userText != 'bye':
        uc = uc + 1
        response= str(english_bot.get_response(userText)) + "<br>sentiment:" + str(s.sentiment(userText)) + " UICtest:" +str(uc)
        sentiment = sentiment + float(s.sentiment(userText))
        return str(b + response)
    

    if userText == 'Bye' or userText == 'bye':
        if uc != 0:
            sentiment = sentiment/uc
            # return str(b +'You look depressed. Do you want to continue with Check Depression? (Y/N)' + str(sentiment))
            if sentiment<0:
            #return str(b +"negative:"+ str(neg)+"Positive:" + str(pos))
                temp=sentiment
                sentiment = 0
                flag = 1
                uc=0
                return str(b +'You look depressed. Do you want to continue with Check Depression? (Y/N)' + str(temp))
            elif sentiment>=0:
                #sentiment = 0
                uc=0
            #return str(b +"negative:"+ str(neg)+"Positive:" + str(pos))
                return str(b +"You're all good.. \nHave a good day" + str(sentiment))
            else:
                return str('Internal error')
        else:
            return str(b +"You're all good.. \nHave a good day")


    if userText == 'y' and flag == 1:
        if j==1:
            flag2=flag2+1
            flag=flag+1
            return str(b +question2)
        else:
            j=1
            #uc = uc + 1
            return str(b +question1)
    if userText == 'n' and flag == 1:
        flag=0
        return str(b +'Have a goodday...')


    if userText != 'Bye' and flag2 == 1 and flag == 2 and userText != 'bye':
        if len(question)>i+1:
            i=i+1
            # sentiment = sentiment + float(s.sentiment(userText))
            if userText == 'yes' or userText == 'Yes' or userText == 'y' or userText == 'Y':
                pos=pos+1
                return(b +question[i] +'<br>'+ "pos:" + str(pos) + " neg:" + str(neg))
            elif userText == 'no' or userText == 'No' or userText == 'n' or userText == 'N':
                neg=neg+1
                return(b +question[i] +'<br>'+ "pos:" + str(pos) + " neg:" + str(neg))
            else:
                i=i-1
                return(b +"Sorry i didn't get that.<br> <small>please give you answer in 'yes' or 'no'.</small>" ) 
        else:
            flag=0
            flag2=0
            i=-1
            if pos<=2:
                pos=0
                neg=0
                return str(b +'It is HIGHLY UNLIKELY you are suffering from depression.')
            elif pos>2 and pos<=4:
                pos=0
                neg=0
                return str(b +"it is LIKELY you have MILD depression. You have nothing to worry about if you have mild depression and it is something you can easily snap out of with the right help and support.")
            elif pos>4:
                pos=0
                neg=0
                return str( b +"It is HIGHLY LIKELY you are extremely depressed. Make an appointment with your local GP to discuss with them how you are feeling, they will be able to prescribe you medication (IN MOST CASES, NOT ALL) which can help with your depressed mood. They will also more than likely offer you talking therapy to help you alongside the medication.")
            else:
                pos=0
                neg=0
                return str('INTERNAL ERROR...')
    # if userText == 'rs' and rflag == 0 and flag == 0:
    #     flag=0
    #     flag2=0
    #     #question counter
    #     i=-1
    #     #total sentiment
    #     total=0
    #     #conituous adding usertext sentiment result
    #     sentiment=0
    #     #user input counter
    #     uc=0
    #     return str('re-started')
    # if userText == 'rs' and rflag == 0:
    #     flag=0
    #     flag2=0
    #     #question counter
    #     i=-1
    #     #total sentiment
    #     total=0
    #     #conituous adding usertext sentiment result
    #     sentiment=0
    #     #user input counter
    #     uc=0
    #     return str('re-started')
    
    
       
    

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)

