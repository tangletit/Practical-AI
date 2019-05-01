import random
secret=random.randint(1,10)
print("yuezhu xiaoxiannv")

temp = input("guess what I thinking now : ")
guess = int(temp)
while guess != secret:
	temp = input("you need to do it one more time")
	guess = int(temp)
	if guess == 8:
		print("you are so clever")
	else:
		if guess > 8:
			print("too big")
		else:
			print("too small")
print("game over")