import config 
def mort():
  if config.eau==0 :
    config.tuer("mort de soif")
  if  config.faim==0:
    config.tuer("mort de faim")
  if  config.etat_de_sante==0:
    config.tuer("mort de mal traitance")
  if config.etat_de_sante>150:
    config.tuer("mort d'overdose")