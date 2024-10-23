from fastapi import APIRouter, WebSocket, Depends, HTTPException, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import interview_service, openai_service, audio_service
from app.models.interview import InterviewCreate, InterviewModel, InterviewWithMessages
from typing import List
import magic
import traceback

router = APIRouter()

@router.websocket("/ws/interview/{interview_id}")
async def websocket_endpoint(websocket: WebSocket, interview_id: int, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        interview = interview_service.get_interview(db, interview_id)
        if not interview:
            await websocket.close(code=4004)
            await websocket.send_text("Erreur : Entretien non trouvé. Veuillez vérifier l'ID de l'entretien.")
            return

        # Obtenir le contexte général de l'entretien
        interview_context = interview_service.get_interview_context(db, interview)

        # Initialiser le contexte général
        initial_context = openai_service.create_initial_context(interview_context)
        general_info = openai_service.get_chat_response(initial_context)

        # Envoyer les informations générales au client
        await websocket.send_json({
            "type": "general_info",
            "content": general_info
        })

        # Créer le prompt initial pour commencer l'entretien
        initial_prompt = openai_service.create_initial_prompt(interview_context, general_info)
        ai_response = openai_service.get_chat_response(initial_prompt)

        # Envoyer la première question de l'IA
        audio_data = audio_service.text_to_speech(ai_response)
        await websocket.send_bytes(audio_data)

        # Initialiser le contexte de la conversation
        context = initial_prompt + [{"role": "assistant", "content": ai_response}]

        while True:
            # Recevoir l'audio de l'utilisateur
            user_audio = await websocket.receive_bytes()
            
            user_text = audio_service.speech_to_text(user_audio)
            
            # Ajouter le message de l'utilisateur au contexte
            user_message = {"role": "user", "content": user_text}
            context.append(user_message)

            # Obtenir la réponse de ChatGPT
            ai_response = openai_service.get_chat_response(context)

            # Ajouter la réponse de l'IA au contexte
            ai_message = {"role": "assistant", "content": ai_response}
            context.append(ai_message)
            
            # Convertir la réponse en audio et l'envoyer
            audio_data = audio_service.text_to_speech(ai_response)
            await websocket.send_bytes(audio_data)
            
            # Sauvegarder les messages dans la base de données
            interview_service.save_messages(db, interview_id, [user_message, ai_message])

    except WebSocketDisconnect:
        print(f"WebSocket déconnecté pour l'entretien {interview_id}")
    except Exception as e:
        error_message = f"Une erreur inattendue s'est produite : {str(e)}"
        await websocket.send_text(error_message)
        print(error_message)
        traceback.print_exc()
    finally:
        await websocket.close()

@router.post("/interviews/", response_model=InterviewModel)
def create_interview(interview: InterviewCreate, db: Session = Depends(get_db)):
    try:
        return interview_service.create_interview(db, interview)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création de l'entretien : {str(e)}")

@router.get("/interviews/{interview_id}", response_model=InterviewWithMessages)
def get_interview(interview_id: int, db: Session = Depends(get_db)):
    interview = interview_service.get_interview(db, interview_id)
    if interview is None:
        raise HTTPException(status_code=404, detail=f"Entretien avec l'ID {interview_id} non trouvé")
    return interview
