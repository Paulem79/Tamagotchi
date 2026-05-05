import modules.nourriture as nourriture
import modules.eau as eau
import modules.sante as sante
import aioconsole

async def action():
    a = await aioconsole.ainput('')
    
    if a == "nourrir":
        nourriture.nourrir()
    elif a == "boire":
        eau.boire()
    elif a == "soins":
        sante.guerrir()
    
    await action() # se rappelle elle meme 
