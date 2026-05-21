import config 
def mort():
  if config.eau==0 :
    config.tuér("mort de soif")
  if  config.faim==0:
    config.tuér("mort de faim")
  if  config.etat_de_sante==0:
    config.tuér("mort de mal traitance")