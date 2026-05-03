import modules.nourriture as nourriture

def action():
    print(nourriture.faim) #test pour voir si faim descend
    a = input("action?")
    if a == "nourrir":
        nourriture.nourrir()
    action() #se rapelle elle meme 
