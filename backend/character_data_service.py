import requests
import json
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class CharacterDataService:
    def __init__(self):
        self.local_data = self._load_local_data()
    
    def _load_local_data(self) -> Dict[str, Any]:
        """Load local character data from JSON files"""
        try:
            with open("radicals.json", "r", encoding="utf-8") as f:
                return {"radicals": json.load(f)}
        except Exception as e:
            logger.error(f"Failed to load local data: {e}")
            return {"radicals": []}
    
    def get_character_info(self, character: str) -> Optional[Dict[str, Any]]:
        """
        Get character information from multiple sources with fallbacks
        
        Args:
            character: Chinese character
            
        Returns:
            Dictionary with character info or None if all sources fail
        """
        # Try OpenAI first (most reliable)
        try:
            from openai_service import OpenAIService
            openai_service = OpenAIService()
            if openai_service.is_available():
                result = openai_service.get_character_info(character)
                if result:
                    logger.info(f"OpenAI provided character info for {character}")
                    return result
        except Exception as e:
            logger.warning(f"OpenAI failed for {character}: {e}")
        
        # Fallback to CCDB
        try:
            return self._get_from_ccdb(character)
        except Exception as e:
            logger.warning(f"CCDB failed for {character}: {e}")
        
        # Fallback to local data
        try:
            return self._get_from_local_data(character)
        except Exception as e:
            logger.error(f"Local data failed for {character}: {e}")
        
        # Final fallback - basic info
        return self._get_basic_info(character)
    
    def _get_from_ccdb(self, character: str) -> Dict[str, Any]:
        """Get character info from CCDB API"""
        url = f"http://ccdb.hemiola.com/characters/string/{character}?fields=kDefinition,kMandarin,kRSKangXi"
        response = requests.get(url, headers={"User-Agent": "PinyImage/1.0"}, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            raise ValueError("No character data found")
        
        char_data = data[0]
        definition = char_data.get('kDefinition', '')
        rad_num = char_data.get('kRSKangXi', '').split('.')[0]
        
        # Get radical info
        radical_info = self._get_radical_info(rad_num)
        
        return {
            "character": character,
            "definition": definition,
            "radical_number": rad_num,
            "radical_character": radical_info.get('radical', ''),
            "radical_meaning": radical_info.get('english', ''),
            "source": "ccdb"
        }
    
    def _get_from_local_data(self, character: str) -> Dict[str, Any]:
        """Get character info from local database"""
        # This would be expanded with a local character database
        # For now, return basic info
        return self._get_basic_info(character)
    
    def _get_basic_info(self, character: str) -> Dict[str, Any]:
        """Get basic character info when all else fails"""
        return {
            "character": character,
            "definition": "character",
            "radical_number": "1",
            "radical_character": character,
            "radical_meaning": "basic character",
            "source": "fallback"
        }
    
    def _get_radical_info(self, rad_num: str) -> Dict[str, str]:
        """Get radical information from local data"""
        try:
            rad_num_int = int(rad_num)
            for radical in self.local_data.get("radicals", []):
                if radical.get("id") == rad_num_int:
                    return {
                        "radical": radical.get("radical", ""),
                        "english": radical.get("english", "")
                    }
        except (ValueError, KeyError):
            pass
        
        return {"radical": "", "english": ""}
    
    def is_available(self) -> bool:
        """Check if the service is available"""
        return len(self.local_data.get("radicals", [])) > 0
