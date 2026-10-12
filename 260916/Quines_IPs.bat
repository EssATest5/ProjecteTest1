@echo off
@echo _________________
@echo Fent ping al rang ...	
for /L %%i in (150,1,175) do @ping -n 1 -w 1 10.199.160.%%i >nul

arp -a > %1
@echo Llestos, ja pots mirar l'arxiu %1
@echo Recorda que la teva no surt al llistat pero si al la capselera
@echo _________________