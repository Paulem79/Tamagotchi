import modules.nourriture as nourriture
import modules.eau as eau
import modules.sante as sante
import aioconsole
import modules.sport as sport
import modules.DAE as DAE

async def action():
    a = await aioconsole.ainput('')

    if a == "dae":
        print("dae")
        DAE.actionner()
    elif a == "nourrir":
        nourriture.nourrir()
    elif a == "boire":
        eau.boire()
    elif a == "soins":
        sante.guerir()
    elif a == "sport":
        sport.sport()
    
    await action() # se rappelle soi meme 
