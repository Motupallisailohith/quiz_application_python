# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 23:06:39 2018
@author: Abhik Banerjee
This .py code gives out the GUI for Stegnography.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import IntVar ,DISABLED
import datetime
"""
The Main Controller.
"""
class sai(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self)
        container=tk.Frame(self)
        self.title("Steg101 v1.10")
        
        container.grid()
        self.frames={}
        for x in (IntroPage,ExamPage):
            frame=x(container,self)
            self.frames[x]=frame
            frame.grid(row=0,column=0,sticky="nsew")
            
        self.showFrame(IntroPage)
        
    def showFrame(self,cont):
        frame=self.frames[cont]
        frame.tkraise() 
        
"""
This is the Start Page.
""" 
        
class IntroPage(tk.Frame):
    def __init__(self,parent,controller):
        ttk.Frame.__init__(self,parent)
        message1="""This is a test Application. Please Read the Introduction if
                        you are a first-timer. 
        """
        message2="""
        This application is a Mini  Quiz. You will be given 10 Question and 40 minutes to solve them.
        """
        message3="""
        """
        message4="""Warning: The Makers would not be held responsible for the actions of the User."""
        ttk.Label(self,text=message1,font=("Comic Sans MS",12,'bold')).grid(row=0)
        ttk.Label(self,text=message2,font=("Helvetica",12)).grid(row=1)
        ttk.Label(self,text=message3,font=("Verdana",10,"bold")).grid(row=2)
        ttk.Label(self,text=message4,font=("Times",12,"bold italic underline")).grid(row=3)
        ttk.Button(self,text="Start",command=lambda:controller.showFrame(ExamPage)).grid(row=4,pady=5)
"""
This page shows the questions and is the main page for the quiz
"""    
      
class ExamPage(tk.Frame):
    def __init__(self,parent,controller):
        ttk.Frame.__init__(self,parent)
        self.label=tk.Label(self,text="Welcome to the Quiz",font=("Times",14))
        self.label.grid(row=0, column=10, columnspan=10)
        self.timerLabel = tk.Label()
        self.timerLabel.grid(row=6,column=5,columnspan=2,sticky="nsew")
        self.started=False
        self.mark=0
        self.finished=False
        
                
        self.controller=controller
        
        #set the questions inside self.questions
        self.questions=["Question 1","Question 2","Question 3","Question 4","Question 5","Question 6","Question 7","Question 8","Question 9","Question 10"]
        
        self.choice=tk.IntVar()
        
        # manually set the choices in the self.choices dictionary
        self.choices={}
        for x in self.questions:
            self.choices[x]=[]
        for x in self.questions:
            for y in range(4):
                t="Option "+str(y+1)+" for "+x
                self.choices[x].append(t)  
        
        #mapping of question to correct answers
        self.correct={1:1,2:3,3:4,4:2,5:3,6:4,7:2,8:3,9:4,10:1}    
        
        self.chosen={}
        
        self.button2=ttk.Button(self,text="Start Exam",command=lambda:self.startExam())
        self.button2.grid(row=3,column=2,columnspan=2,padx=5,pady=10)
        
        self.button3=ttk.Button(self,text="Quit",command=lambda:self.endExam())
        self.button3.grid(row=5,column=2,columnspan=2)
        
    def startExam(self):
        
        if self.started==False:
            self.clock_start()
            
            self.button2.configure(text="Next Question")
            self.button2.grid(row=3,column=2,sticky="nsew",padx=5,pady=(10,5))
            
            self.button4=ttk.Button(self,text="Previous Question",command=lambda:self.previousQ())
            self.button4.grid(row=4,column=2,sticky="nsew",padx=5,pady=(5,10))
            
            self.started=True
            question=self.questions[self.mark]       
            self.label.configure(text=question)
            self.choice1=ttk.Radiobutton(self,text=self.choices[question][0],variable=self.choice,value=0)
            self.choice2=ttk.Radiobutton(self,text=self.choices[question][1],variable=self.choice,value=1)
            self.choice3=ttk.Radiobutton(self,text=self.choices[question][2],variable=self.choice,value=2)
            self.choice4=ttk.Radiobutton(self,text=self.choices[question][3],variable=self.choice,value=3)
            
            self.choice1.grid(row=2,column=5)
            self.choice2.grid(row=3,column=5)
            self.choice3.grid(row=4,column=5)
            self.choice4.grid(row=5,column=5)
                
            
        else:
            self.chosen[self.mark+1]=self.choice.get()+1
            print(self.chosen)
            self.mark+=1
            question=self.questions[self.mark]
            self.label.configure(text=question)
            self.choice1.configure(text=self.choices[question][0])
            self.choice2.configure(text=self.choices[question][1])
            self.choice3.configure(text=self.choices[question][2])
            self.choice4.configure(text=self.choices[question][3])
            
            
            
    def previousQ(self):
        if self.mark>0:
            self.mark-=1
            question=self.questions[self.mark]
            self.questionSpace.configure(text=self.questions[self.mark])
            self.choice1.configure(text=self.choices[question][0])
            self.choice2.configure(text=self.choices[question][1])
            self.choice3.configure(text=self.choices[question][2])
            self.choice4.configure(text=self.choices[question][3])
                    
    def clock_start(self):
        self.controller.after(datetime.timedelta(seconds=40*60).seconds*1000,lambda: self.root.destroy())
        self.done_time=datetime.datetime.now() + datetime.timedelta(seconds=40*60) # half hour
        self.update_clock()
        
    def update_clock(self):
        if self.finished==False:
            elapsed = self.done_time - datetime.datetime.now()
            h,m=0,0
            e=elapsed.seconds
            while(e>3600):
                h+=1
                e-=3600
            while(e>60):
                m+=1
                e-=60
            self.timerLabel.configure(text="Time Left:%02d:%02d:%02d"%(h,m,e))
            
            self.controller.after(1000, self.update_clock)
        
    def endExam(self):
        if self.started==False:
            self.controller.destroy()
        score=0
        for x in self.chosen:
            if self.correct[x]==self.chosen[x]:
                score+=1
        self.timerLabel.destroy()
        self.choice1.destroy() 
        self.choice2.destroy() 
        self.choice3.destroy() 
        self.choice4.destroy() 
        self.finished=True
        self.button2.configure(state=DISABLED)
        self.button4.configure(state=DISABLED)
        self.label.configure(text="Your Score is %d"%(score))
        self.button3.configure(command=self.controller.destroy)
        

inst=sai()
inst.mainloop()
