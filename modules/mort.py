import config 
def mort():
  if config.eau==0 :
    config.tuer("soif")
  if  config.faim==0:
    config.tuer("faim")
  if  config.etat_de_sante==0:
    config.tuer("mal traitance")
  if config.etat_de_sante>150:
    config.tuer("overdose")