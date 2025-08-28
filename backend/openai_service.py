import openai
import os
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
            self.client = openai
        else:
            self.client = None
            logger.warning("OpenAI API key not found")
    
    def is_available(self) -> bool:
        """Check if OpenAI service is available"""
        return self.client is not None
    
    def get_character_info(self, character: str) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive character information using OpenAI
        
        Args:
            character: Chinese character
            
        Returns:
            Dictionary with character info or None if failed
        """
        if not self.is_available():
            return None
        
        try:
            prompt = f"""Analyze the Chinese character "{character}" and provide the following information in JSON format:

{{
    "pinyin": "the pinyin pronunciation",
    "meaning": "the English meaning/definition",
    "radical": "the main radical component",
    "radical_meaning": "what the radical means",
    "stroke_count": "number of strokes",
    "difficulty": "beginner/intermediate/advanced"
}}

Be accurate and concise. Only return valid JSON."""

            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Chinese language expert. Provide accurate information about Chinese characters in JSON format only."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            # Parse the response
            content = response.choices[0].message.content.strip()
            
            # Try to extract JSON from the response
            import json
            try:
                # Remove any markdown formatting
                if content.startswith("```json"):
                    content = content[7:]
                if content.endswith("```"):
                    content = content[:-3]
                
                char_info = json.loads(content.strip())
                
                return {
                    "character": character,
                    "pinyin": char_info.get("pinyin", ""),
                    "meaning": char_info.get("meaning", ""),
                    "radical": char_info.get("radical", ""),
                    "radical_meaning": char_info.get("radical_meaning", ""),
                    "stroke_count": char_info.get("stroke_count", ""),
                    "difficulty": char_info.get("difficulty", "beginner"),
                    "source": "openai"
                }
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse OpenAI response as JSON: {e}")
                logger.error(f"Response content: {content}")
                return None
                
        except Exception as e:
            logger.error(f"OpenAI character info request failed: {e}")
            return None
    
    def generate_mnemonic(self, character: str, pinyin: str, meaning: str) -> Optional[str]:
        """
        Generate a mnemonic connection for a Chinese character
        
        Args:
            character: The Chinese character
            pinyin: The pinyin pronunciation
            meaning: The English meaning
            
        Returns:
            Generated mnemonic text or None if failed
        """
        if not self.is_available():
            return None
        
        try:
            prompt = f"""Create a memorable visual connection for the Chinese character {character} (pronounced "{pinyin}" meaning "{meaning}"). 

Focus on:
1. Visual similarity between the character's strokes and familiar objects
2. Sound associations with the pinyin pronunciation
3. Meaning connections that create vivid mental images

Keep it to 2-3 sentences maximum. Make it creative and memorable for language learning."""

            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative language learning assistant specializing in creating memorable mnemonics for Chinese characters."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI mnemonic generation failed: {e}")
            return None
    
    def get_character_analysis(self, character: str) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive character analysis including breakdown and learning tips
        
        Args:
            character: Chinese character
            
        Returns:
            Dictionary with analysis or None if failed
        """
        if not self.is_available():
            return None
        
        try:
            prompt = f"""Provide a comprehensive analysis of the Chinese character "{character}" in JSON format:

{{
    "character": "{character}",
    "pinyin": "pronunciation",
    "meaning": "English meaning",
    "components": ["list of character components"],
    "radical": "main radical",
    "radical_meaning": "what the radical means",
    "stroke_order": "basic stroke order description",
    "common_words": ["common words using this character"],
    "learning_tips": ["2-3 specific tips for remembering this character"],
    "difficulty_level": "beginner/intermediate/advanced"
}}

Be accurate and helpful for language learners."""

            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Chinese language teacher. Provide detailed character analysis in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.4
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse JSON response
            import json
            try:
                if content.startswith("```json"):
                    content = content[7:]
                if content.endswith("```"):
                    content = content[:-3]
                
                analysis = json.loads(content.strip())
                analysis["source"] = "openai"
                return analysis
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse analysis response: {e}")
                return None
                
        except Exception as e:
            logger.error(f"OpenAI character analysis failed: {e}")
            return None
