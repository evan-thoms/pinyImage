import cohere
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

def getConnections(character, pinyin):
	print("conections", character, pinyin)
	formMessage = "Make a visual connection between the meaning Chinese character "+character + "(" +pinyin+"). and its sound or character appearance. Be creative, as this connection will help in remembering the character for language learning purposes. Respond in one to two quick sentences making two to three connections between the meaning and the charater appearance, and sound.int"
	co = cohere.Client(os.getenv("API_KEY"))
	print(os.getenv("API_KEY"))
	response = co.chat(
		message=formMessage
	)

	return response.text

