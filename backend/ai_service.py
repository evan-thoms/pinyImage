import os
import cohere
import openai
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize clients if API keys are available
        self.cohere_client = None
        self.openai_client = None
        
        if self.cohere_api_key:
            try:
                self.cohere_client = cohere.Client(self.cohere_api_key)
                logger.info("Cohere client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Cohere client: {e}")
        
        if self.openai_api_key:
            try:
                openai.api_key = self.openai_api_key
                self.openai_client = openai
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                self.openai_client = None
    
    def generate_mnemonic(self, character: str, pinyin: str, meaning: str) -> Optional[str]:
        """
        Generate a mnemonic connection for a Chinese character using the best available AI service.
        
        Args:
            character: The Chinese character
            pinyin: The pinyin pronunciation
            meaning: The English meaning
            
        Returns:
            Generated mnemonic text or None if all services fail
        """
        # Try OpenAI first (generally better for creative tasks)
        if self.openai_client:
            try:
                return self._generate_with_openai(character, pinyin, meaning)
            except Exception as e:
                logger.error(f"OpenAI generation failed: {e}")
        
        # Fallback to Cohere
        if self.cohere_client:
            try:
                return self._generate_with_cohere(character, pinyin, meaning)
            except Exception as e:
                logger.error(f"Cohere generation failed: {e}")
        
        logger.error("No AI service available")
        return None
    
    def _generate_with_openai(self, character: str, pinyin: str, meaning: str) -> str:
        """Generate mnemonic using OpenAI API"""
        prompt = f"""Create a memorable visual connection for the Chinese character {character} (pronounced "{pinyin}" meaning "{meaning}"). 

Focus on:
1. Visual similarity between the character's strokes and familiar objects
2. Sound associations with the pinyin pronunciation
3. Meaning connections that create vivid mental images

Keep it to 2-3 sentences maximum. Make it creative and memorable for language learning."""

        response = self.openai_client.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative language learning assistant specializing in creating memorable mnemonics for Chinese characters."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_with_cohere(self, character: str, pinyin: str, meaning: str) -> str:
        """Generate mnemonic using Cohere API"""
        prompt = f"""Create a memorable visual connection for the Chinese character {character} (pronounced "{pinyin}" meaning "{meaning}"). 

Focus on:
1. Visual similarity between the character's strokes and familiar objects
2. Sound associations with the pinyin pronunciation  
3. Meaning connections that create vivid mental images

Keep it to 2-3 sentences maximum. Make it creative and memorable for language learning."""

        response = self.cohere_client.chat(
            message=prompt,
            model="command",
            temperature=0.8,
            max_tokens=150
        )
        
        return response.text.strip()
    
    def is_available(self) -> bool:
        """Check if any AI service is available"""
        return bool(self.cohere_client or self.openai_client)
    
    def get_available_services(self) -> list:
        """Get list of available AI services"""
        services = []
        if self.cohere_client:
            services.append("Cohere")
        if self.openai_client:
            services.append("OpenAI")
        return services
