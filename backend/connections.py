import cohere

def getConnections(character, pinyin):
	print("conections", character, pinyin)
	formMessage = "Make a visual connection between the meaning Chinese character "+character + "(" +pinyin+"). and its sound or character appearance. Be creative, as this connection will help in remembering the character for language learning purposes. Respond in one to two quick sentences making two to three connections between the meaning and the charater appearance, and sound."
	co = cohere.Client("PxEa5mkfwRevaEJFtzmJcO8De1vxN2yupKtuPbZt")
	response = co.chat(
		message=formMessage
	)

	return response.text

