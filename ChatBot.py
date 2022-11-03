import re
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
]

def get_response(user_input):
    split_message = re.split(r'\s|[,:;.?!-_]\s*', user_input.lower())
    print(split_message)
    response = check_all_messages(split_message)
    return response

def message_probability(user_message, recognized_words, single_response=False, required_word=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognized_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognized_words))

    for word in required_word:
        if word not in user_message:
            has_required_words = False
            break
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob
        highest_prob[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    response('Hola. ¿Hay algo con lo que te pueda ayudar?', ['hola', 'hi', 'saludos', 'buenas'], single_response=True)
    response('Hoy deberías cocinar '+ ['Pollo al Horno', 'Ceviche', 'Lentejitas'][
        random.randrange(3)], ['recomiendas', 'cocinar', 'debería', 'hacer','preparar'], single_response=True)
    response('¿Estoy bien y tú, te puedo ayudar en algo?', ['como', 'estas', 'va', 'vas', 'sientes'], required_words=['como'])

    best_match = max(highest_prob, key=highest_prob.get)

    return unknown() if highest_prob[best_match] < 1 else best_match


def unknown():
    response = ['¿Puedes decirlo de nuevo?', 'No estoy seguro de lo quieres', 'Por favor, reformula tu consulta'][
        random.randrange(3)]
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
def ask(request = None):
    if request is None:
        text = 'No ha recibido nada'
    else:
        text = get_response(request)
    return text


