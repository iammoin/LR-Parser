from tkinter import *
import re
from back import *
gr={}
term =[]
nterm =[]
flag1 = True

def read():
        global g
        gr={}
    

        term=[]
        nterm=[]
        G=g.get(1.0,END).strip().split("\n")
        for i in range(len(G)):
            t1=re.search("\s*(\w)\s*-->\s*([e]|[^|e\s]+)\s*",G[i]) # anycharacter --> e | other than (|,e,\s) one more times
            l=[]
            
            l.append(t1.group(2)) # RHS is appended into the list
            gr[t1.group(1)]=l # gr[LHS]=RHS
            m=re.findall("\|\s*([e]|[^|e\s]+)\s*",G[i]) # if | exists
            for i in m:
                term2=re.findall("[a-z()+\-*/=]",i)
                term.extend(list(set(term2)))
            term1=re.findall("[a-z()+\-*/=]",t1.group(2))
            

            term.extend(list(set(term1)))
            
            nterm.extend(list(t1.group(1)))


            
            
            gr[t1.group(1)].extend(m)
        print(gr)
        return gr,term,nterm


def read1(event):
    #try:
        rd=read()
        f=first(rd[0],rd[1],rd[2])
        fst=Tk()
        fst.title("FIRST SET")
        sz=str((len(rd[1])+2)*70)+"x"+str((len(rd[2])+1)*70)
        fst.geometry(sz)
        ys=Scrollbar(fst)
        opt=Text(fst, wrap=NONE, fg="blue")
        ys.pack(side=RIGHT, fill=Y)
        opt.config(yscrollcommand=ys.set)
        opt.pack(side=LEFT, fill=Y)
        ys.config(command=opt.yview)
        opt.config(state=NORMAL, font='Arial -24')
        opt.delete(0.0,END)
        opt.insert(END,"\n\n")
        for i in rd[2]:
            opt.insert(END,"      FIRST("+i+")   =   ")
            f1=" , ".join(f[i])
            opt.insert(END,"{  "+f1+"  }")
            opt.insert(END,"\n\n")
        opt.config(state=DISABLED)
    

def read2(event):
    #try:
        rd=read()
        f=follow(rd[0],rd[1],rd[2])
        flw=Tk()
        flw.title("FOLLOW SET")
        sz=str((len(rd[1])+2)*70)+"x"+str((len(rd[2])+1)*70)
        flw.geometry(sz)
        ys=Scrollbar(flw)
        opt=Text(flw, wrap=NONE, fg="blue")
        ys.pack(side=RIGHT, fill=Y)
        opt.config(yscrollcommand=ys.set)
        opt.pack(side=LEFT, fill=Y)
        ys.config(command=opt.yview)
        opt.config(state=NORMAL, font='Arial -24')
        opt.delete(0.0,END)
        opt.insert(END,"\n\n")
        for i in rd[2]:
            opt.insert(END,"      FOLLOW("+i+")   =   ")
            f1=" , ".join(f[i])
            opt.insert(END,"{  "+f1+"  }")
            opt.insert(END,"\n\n")
        opt.config(state=DISABLED)

def display_table(PPT,con,inpt,non_ter,ter):
        lltab=Tk()
        lltab.title("LL(1)-TABLE")
        sz=str((len(inpt)+1)*230)+"x"+str((len(non_ter)+1)*88)
        lltab.geometry(sz)
        ys=Scrollbar(lltab)
        xs=Scrollbar(lltab, orient=HORIZONTAL)
        opt=Text(lltab, wrap=NONE, width=str((len(inpt)+1)*20), height=str((len(non_ter)+1)*2+2), fg="blue")
        ys.pack(side=RIGHT, fill=Y)
        xs.pack(side=BOTTOM, fill=X)
        opt.config(yscrollcommand=ys.set, xscrollcommand=xs.set)
        opt.pack(side=LEFT, fill=Y)
        ys.config(command=opt.yview)
        xs.config(command=opt.xview)
        opt.config(state=NORMAL, font='Arial -24')
        opt.delete(0.0,END)
        opt.insert(END,"="*16*(len(inpt)+1)+"\n")
        opt.insert(END,"   NON_TERMINAL\t\t\t"+inpt[0])
        for i in inpt[1:]:
            opt.insert(END,"\t\t"+i)
        opt.insert(END,"\n")
        opt.insert(END,"="*16*(len(inpt)+1)+"\n")
        k=0
        for i in non_ter:
            opt.insert(END,"\t"+i+"\t\t")
            k=non_ter.index(i)
            for j in PPT[k]:
                if j=="error" or j=="conflict":
                    opt.insert(END,j+"    \t\t")
                else:
                    #if j[1]=="^":
                    #    opt.insert(END,j[0]+"-->lambda"+"    \t\t")
                    #else:
                    #   opt.insert(END,j[0]+"-->"+j[1]+"    \t\t")
                        for i in range(len(j)):
                                if i%2==0:
                                        opt.insert(END,j[i]+"-->")
                                else:
                                        opt.insert(END,j[i]+"   ")
                        opt.insert(END,"\t")
                            
                            
            opt.insert(END,"\n")
            k+=1
            if k<len(non_ter):
                opt.insert(END,"-"*28*(len(inpt)+1)+"\n")
        opt.insert(END,"="*16*(len(inpt)+1)+"\n")
        if con:
            opt.config(fg="red")
            opt.insert(END,"\n     "+"="*7*(len(ter)+1)+"<:: TABLE HAS CONFLICT ::>"+"="*7*(len(ter)+1)+"\n")
        opt.config(state=DISABLED)


def read3(event):
    #try:
        rd=read()
        PPT,con,inpt=table(rd[0],rd[1],rd[2])
        display_table(PPT,con,inpt,rd[2],rd[1])



def parse(PPT,G,ter,non_ter,Input,start=0):
    First=first(G,ter,non_ter)
    Follow=follow(G,ter,non_ter,start)
    inpt=ter[:]
    inpt.append('$')
    if start==0:
        start=non_ter[0]
    stack=start+"$"
    Input=Input+"$"
    matched=""
    action=""
    ip=0
    error=False
    x=stack[0]
    prse=Tk()
    prse.geometry("1050x850")
    prse.title("STRING PARSING")
    ys=Scrollbar(prse)
    xs=Scrollbar(prse, orient=HORIZONTAL)
    opt=Text(prse, wrap=NONE,fg="blue")
    ys.pack(side=RIGHT, fill=Y)
    xs.pack(side=BOTTOM, fill=X)
    opt.config(yscrollcommand=ys.set, xscrollcommand=xs.set)
    opt.pack(side=LEFT, fill=Y)
    ys.config(command=opt.yview)
    xs.config(command=opt.xview)
    opt.config(state=NORMAL, font='Arial -24')
    opt.delete(0.0,END)
    opt.insert(END,"\n    ","="*70+"\n")
    opt.insert(END,"\tMATCHED\t\tSTACK\t\tINPUT\t\tACTION\n")
    opt.insert(END,"    "+"="*70+"\n")
    opt.insert(END,"\t\t\t"+stack+"\t\t"+Input+"\n")
    while x!='$':
        opt.insert(END,"    "+"-"*122+"\n")
        a=Input[ip]
        if a not in inpt:
            action="Error: Input symbol doesn't belongs to Grammar symbol"
            error=True
            break
        if x==Input[ip]:
            stack=stack[1:]
            matched=matched+Input[ip]
            ip=ip+1
            action="match "+x
        elif x in ter:
            error=True
            action="Error"
        elif PPT[non_ter.index(x)][inpt.index(a)]=="error" or PPT[non_ter.index(x)][inpt.index(a)]=="conflict":
            error=True
            action="Error"
        else:
            prod=PPT[non_ter.index(x)][inpt.index(a)]
            l,r=prod
            stack=stack[1:]
            if r!="^":
                stack=r+stack
            if r=="^":
                action="output "+l+"-->"+"lambda"
            else:
                action="output "+l+"-->"+r
        x=stack[0]
        opt.insert(END,"\t"+matched+"\t\t"+stack+"\t\t"+Input[ip:]+"\t\t"+action+"\n")
        if error:
            break
    opt.insert(END,"    "+"="*70+"\n")
    if error:
        opt.config(fg="red")
        opt.insert(END,"\n\t         \"THE  GIVEN  STRING  DOES  NOT  BELONGS  TO  LANGUAGE\"\n")
    else:
        opt.insert(END,"\n\t\t\t\"STRING  PARSED  SUCCESSFULLY\"\n")
    opt.config(state=DISABLED)
    return (not error)

def readstr(event):
    #try:
        rd=read()
        PPT,con,inpt=table(rd[0],rd[1],rd[2])
        strng=s.get(1.0,END).strip()
        parse(PPT,rd[0],rd[1],rd[2],strng)


            
def create_new():
    global g
    top1.destroy()
    top = Tk()
    top.title("LL-1 Table")
    top.geometry('750x550')
    labelframe = LabelFrame(top, text="CD PROJECT", font="Algerian -20 italic bold",fg="purple",bg="azure2")
    labelframe.pack(padx='2',pady='2',fill="both", expand="yes")
    label = Label(labelframe, text='LL-1 Parsing Table',font= "Algerian -40 italic bold", fg="purple",bg="azure2")
    label.pack(side=TOP)

    label1 = Label(top, text='GRAMMAR:',font='Arial -15 bold', fg="purple",bg='azure2')
    label1.place(relx = 0.08, rely = 0.18)

    g = Text(labelframe,width="40", height="08",font='Arial -24')
    g.place(relx = 0.25, rely = 0.15)

    b2=Button(labelframe,justify = LEFT)        #first button
    photo2=PhotoImage(file="button2.png")
    b2.config(image=photo2,width="156",height="32",bg="azure2")
    b2.place(relx = 0.1, rely = 0.7)
    b2.bind('<Button-1>',read1)


    b3=Button(labelframe,justify = LEFT)        #follow button
    photo3=PhotoImage(file="button3.png")
    b3.config(image=photo3,width="156",height="32",bg="azure2")
    b3.place(relx = 0.4, rely = 0.7)
    b3.bind('<Button-1>',read2)


    b4=Button(labelframe,justify = LEFT)        #Parsing table button
    photo4=PhotoImage(file="button4.png")
    b4.config(image=photo4,width="156",height="32",bg="azure2")
    b4.place(relx = 0.7, rely = 0.7)
    b4.bind('<Button-1>',read3)

    

    b6=Button(labelframe,justify = LEFT)        #quit button
    photo6=PhotoImage(file="quit.png")
    b6.config(image=photo6,width="156",height="32",bg="azure2",command=quit)
    b6.place(relx = 0.4, rely = 0.9)
    
    g.insert(END,"S--> CC\n")
    g.insert(END,"C--> cC | d\n")

    mainloop()


###################  start window starts

top1 = Tk()
top1.title("LL-1 Table")
top1.geometry('550x400')

labelframe = LabelFrame(top1, text="CD PROJECT", font="Algerian -20 italic bold",fg="purple",bg="azure2")
labelframe.pack(padx='2',pady='2',fill="both", expand="yes")

label = Label(labelframe, text='LL-1 Parsing Table',font= "Algerian -40 italic bold", fg="purple",bg="azure2")
label.pack(side=TOP)

b=Button(labelframe,justify = LEFT)
photo=PhotoImage(file="marco.jpg")
b.config(image=photo,width="451",height="100",bg="azure2",command=create_new)
b.place(relx = 0.08, rely = 0.3)

mainloop()

####################  start window closes