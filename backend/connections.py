from openai_service import OpenAIService
import logging

logger = logging.getLogger(__name__)

def getConnections(character, pinyin, meaning=""):
    """
    Generate mnemonic connections for a Chinese character using OpenAI.
    
    Args:
        character: The Chinese character
        pinyin: The pinyin pronunciation
        meaning: The English meaning (optional)
        
    Returns:
        Generated mnemonic text or error message
    """
    try:
        logger.info(f"Generating connections for character: {character}, pinyin: {pinyin}")
        
        # Use OpenAI service
        openai_service = OpenAIService()
        
        if not openai_service.is_available():
            return "OpenAI service is currently unavailable. Please try again later."
        
        result = openai_service.generate_mnemonic(character, pinyin, meaning)
        
        if result:
            return result
        else:
            return "Unable to generate mnemonic at this time. Please try again."
            
    except Exception as e:
        logger.error(f"Error generating connections: {e}")
        return "An error occurred while generating the mnemonic. Please try again."

