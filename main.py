from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import random
import asyncio
import subprocess
import dotenv
import os

dotenv.load_dotenv()
api_key = os.getenv("TELEGRAM_API_KEY")
print(api_key)

# Función para manejar el comando /hola
async def hola(update: Update, context: CallbackContext):
    await update.message.reply_text('¡Hola Mundo!')

# Función para manejar el comando /numero
async def numero(update: Update, context: CallbackContext):
    random_number = random.randint(1, 100)  # Número aleatorio entre 1 y 100
    await update.message.reply_text(f'El número aleatorio es: {random_number}')

# Función para manejar el comando /saludo
async def saludo(update: Update, context: CallbackContext):
    user_name = update.message.from_user.first_name  # Obtener el nombre del usuario
    await update.message.reply_text(f'Hello {user_name}!')  # Responder con el saludo personalizado

# Función para manejar el comando /ping
async def ping(update: Update, context: CallbackContext):
    if context.args:  # Verifica si hay argumentos (el URL)
        url = context.args[0]  # Obtiene la URL del comando
        try:
            # Ejecuta el comando ping y captura la salida
            result = subprocess.run(
                ["ping", "-c", "4", url],  # En sistemas basados en Unix (Linux/Mac), -c indica la cantidad de paquetes
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Verifica si hubo error
            if result.returncode != 0:
                await update.message.reply_text(f"Error al hacer ping a {url}: {result.stderr}")
            else:
                # Procesa la salida del comando ping
                output = result.stdout
                # Extrae las estadísticas relevantes (solo en sistemas Unix/Linux, en Windows sería diferente)
                lines = output.splitlines()
                stats = lines[-1]  # La última línea contiene la información sobre los paquetes
                await update.message.reply_text(f"Paquete enviado! {stats}")  # Responde con las estadísticas del ping

        except Exception as e:
            await update.message.reply_text(f"Hubo un error al intentar hacer ping: {e}")
    else:
        await update.message.reply_text("Por favor, proporciona una URL después de /ping.")

# Función para manejar cualquier mensaje de texto que no sea un comando
async def handle_text(update: Update, context: CallbackContext):
    user_text = update.message.text  # Obtener el texto que el usuario envió
    # Responder con el mismo texto (eco), o hacer algo con el texto recibido
    await update.message.reply_text(f'Recibí tu mensaje: {user_text}')

# Función principal que arranca el bot
def main():
    # Crear la instancia de Application (más reciente y asíncrona)
    application = Application.builder().token(api_key).build()
    
    # Agregar manejadores para los comandos /hola, /numero, /saludo, y /ping
    application.add_handler(CommandHandler("hola", hola))
    application.add_handler(CommandHandler("numero", numero))
    application.add_handler(CommandHandler("saludo", saludo))  # Comando /saludo
    application.add_handler(CommandHandler("ping", ping))  # Comando /ping
    
    # Agregar manejador para todos los mensajes de texto
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Iniciar el bot (asíncrono)
    application.run_polling()

# Ejecutar el bot sin asyncio.run en entornos donde el loop ya está corriendo
if __name__ == '__main__':
    # Verificar si asyncio está en ejecución
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError as e:
        if 'This event loop is already running' in str(e):
            asyncio.get_event_loop().create_task(main())  # Si ya está corriendo, lo ejecutamos como tarea
