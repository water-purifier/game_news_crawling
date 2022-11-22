import re,_init

comm = _init.CommonFucntion()
str = 'Pokemon Scarlet/Violet Glitch Lets You Run Twice As Fast With Two Controllers'
newStr = comm.remove_spe_char(str)
print(newStr)