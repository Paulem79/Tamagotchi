import modules.nourriture as nourriture
import modules.eau as eau
import modules.sante as sante
import aioconsole
import modules.sport as sport
import modules.DAE as DAE
import config

async def action():
    # Input asynchrone pour pas bloquer le jeu
    a = await aioconsole.ainput('')

    if a == "dae":
        DAE.actionner()
    elif a == "nourrir":
        nourriture.nourrir()
    elif a == "boire":
        eau.boire()
    elif a == "soins":
        sante.guerir()
    elif a == "sport":
        sport.sport()

    if config.jeu_en_cours:
        await action()
    else:
        return
