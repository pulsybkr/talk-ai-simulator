from openai import OpenAI
from app.config import OPENAI_API_KEY
import tempfile

client = OpenAI(
    api_key=OPENAI_API_KEY
)

def create_initial_context(context):
    prompt = f"""Analysez les informations suivantes pour un entretien d'embauche :

    Fiche de poste : {context["job_description"]}

    CV du candidat : {context["cv"]}

    Lettre de motivation : {context.get("cover_letter", "")}

    Fournissez un résumé des points clés de la fiche de poste, du profil du candidat, et une liste de questions potentielles pour l'entretien basées sur ces informations."""

    return [{"role": "system", "content": prompt}]

def create_initial_prompt(context, general_info):
    prompt = f"""Vous êtes un recruteur conduisant un entretien d'embauche. Voici le contexte de l'entretien :

    {general_info}

    Commencez l'entretien avec une brève introduction voir salutation et presentation, demander son nom et se presenter. Ensuite posez les questions au candidat au fur et à mesure, n'hesitez pas de vous adapter pour que ça soit naturel. Vos réponses doivent être courtes, efficaces et naturelles. N'hésitez pas à ajouter des effets sonores ou des onomatopées pour rendre la conversation plus vivante, car vos réponses seront converties en audio. 
    Très important, il faut que ça soit naturel et pas scripté. Et si le candidat pause une question, ne la répète pas, mais répondez de manière naturelle. Si le candidat pause une question ou change de sujet, faite le lieu savoir et remettez le sur la bonne voie, c'est important de garder le sujet de l'entretien. votre nom c'est hiria  Dans tes reponses, ça ne sert pas d'ecrire ton nom ou ton prenom, mais de parler naturellement. Et aussi, tu n'es pas obligé de rebondire a chaque fois sur les reponses du candidat, mais de parler naturellement. Et n'hesite pas a changer de ton ou d'ajouter des petits commentaires pour que ça soit plus naturel. Et par changement de ton, je veux dire le fais de ne pas forcement etre trop gentil ou trop formel, mais de parler naturellement. A la fin de l'entretien, quant le candidat n'a plus de question, fait une courte conclusion ensuite parle lui de tout les points qu'il pourrai ameliorer pour ces futurs entretiens, donne lui des conseils pour ses futurs entretiens.
    """

    return [{"role": "system", "content": prompt}]

def get_chat_response(messages):
    # Transformer le tableau de messages en une seule chaîne de caractères
    message_string = ""
    for message in messages:
        if isinstance(message, dict) and "role" in message and "content" in message:
            message_string += f"{message['role']}: {message['content']}\n"
        else:
            print(f"Message ignoré car mal formaté : {message}")

    # Vérifier si la chaîne de messages n'est pas vide
    if not message_string:
        raise ValueError("Aucun message valide n'a été fourni")

    formatted_messages = [
        {"role": "user", "content": message_string.strip()}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=formatted_messages
    )
    return response.choices[0].message.content
