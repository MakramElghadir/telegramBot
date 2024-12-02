# Importar las clases necesarias para interactuar con la API de Telegram y manejar actualizaciones
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random  # Importar la librería random para generar números aleatorios
import os  # Para manejar variables de entorno
from dotenv import load_dotenv  # Para cargar el archivo .env
import asyncio  # Para manejar corrutinas

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la API Key desde las variables de entorno
api_key = os.getenv("TELEGRAM_API_KEY")

# Validar que la API Key está configurada
if not api_key:
    raise ValueError("No se encontró la API Key. Por favor, configúrala en el archivo .env.")

# Define el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("¡Hola! Soy tu bot. Usa /hola para saludarme o /aleatorio para un número aleatorio.")

# Define el comando /hola
async def hola(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bomboclat!!")

# Define el comando /aleatorio
async def aleatorio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    numero = random.randint(1, 100)
    await update.message.reply_text(f"Numeroclat bombo es: {numero}")

# Configuración principal del bot
async def main():
    # Crear la aplicación del bot
    app = ApplicationBuilder().token(api_key).build()

    # Agregar manejadores para los comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hola", hola))
    app.add_handler(CommandHandler("aleatorio", aleatorio))

    # Iniciar el bot
    print("El bot está corriendo...")
    await app.run_polling()

# Punto de entrada del script
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()  # Permite reutilizar el bucle de eventos en entornos interactivos
    asyncio.run(main())  # Ejecuta la corrutina principal