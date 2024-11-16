import os
from pathlib import Path
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from django.conf import settings
from django.core.cache import cache
import logging
from .configure import API_HOST,API_KEY

logger = logging.getLogger(__name__)

@dataclass
class CricketAPIConfig:
    API_KEY: str = API_KEY  # Replace with your actual API key
    API_HOST: str = API_HOST
    BASE_URL: str = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1"
    CACHE_TIMEOUT: int = 3600  # 1 hour cache

class PlayerImageHandler:
    def __init__(self):
        self.base_url = "https://cricbuzz-cricket.p.rapidapi.com/img/v1"
        self.headers = {
            "x-rapidapi-key": CricketAPIConfig.API_KEY,
            "x-rapidapi-host": CricketAPIConfig.API_HOST
        }
        # Create media directory if it doesn't exist
        self.image_dir = os.path.join(settings.MEDIA_ROOT, 'player_images')
        os.makedirs(self.image_dir, exist_ok=True)

    def get_player_image(self, face_id: str) -> str:
        if not face_id:
            return self.get_default_image_url()

        # Check if image already exists
        image_filename = f'{face_id}.jpg'
        image_path = os.path.join(self.image_dir, image_filename)
        
        if os.path.exists(image_path):
            return f'{settings.MEDIA_URL}player_images/{image_filename}'

        try:
            url = f"{self.base_url}/i1/c{face_id}/i.jpg"
            querystring={"d":"high"}
            response = requests.get(url, headers=self.headers,params=querystring)
            response.raise_for_status()

            # Verify it's an image response
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                logger.error(f"Invalid content type received: {content_type}")
                return self.get_default_image_url()

            # Save the image directly to file system
            with open(image_path, 'wb') as f:
                f.write(response.content)

            return f'{settings.MEDIA_URL}player_images/{image_filename}'

        except Exception as e:
            logger.error(f"Error processing player image: {str(e)}")
            return self.get_default_image_url()

    @staticmethod
    def get_default_image_url() -> str:
        """Return the URL for the default player image"""
        return f'{settings.STATIC_URL}images/default_player.jpg'

class CricketAPIService:
    def __init__(self):
        self.config = CricketAPIConfig()
        self.image_handler = PlayerImageHandler()
        self.headers = {
            "x-rapidapi-key": self.config.API_KEY,
            "x-rapidapi-host": self.config.API_HOST
        }

    def _make_request(self, url: str, params: Dict = None) -> Dict:
        """Make API request with error handling"""
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return None

    def search_player(self, player_name: str) -> Optional[Dict]:
        """Search for a player by name"""
        url = f"{self.config.BASE_URL}/player/search"
        data = self._make_request(url, {"plrN": player_name})
        if data and 'player' in data:
            return data['player'][0] if data['player'] else None
        return None

    def get_player_details(self, player_id: str) -> Optional[Dict]:
        """Get detailed information about a player"""
        url = f"{self.config.BASE_URL}/player/{player_id}"
        data = self._make_request(url)
        if data:
            face_img_id = data.get('faceImageId')
            data['image_url'] = self.image_handler.get_player_image(face_img_id)
        return data

    def get_player_career(self, player_id: str) -> Optional[Dict]:
        """Get player career statistics"""
        url = f"{self.config.BASE_URL}/player/{player_id}/career"
        data = self._make_request(url)
        if not data:
            return None
        
        return {
            'formats': data.get('values', []),
            'seoTitle': data.get('appIndex', {}).get('seoTitle', ''),
            'webURL': data.get('appIndex', {}).get('webURL', '')
        }

    def get_player_stats(self, player_id: str) -> Dict:
        """Get both batting and bowling statistics for a player"""
        return {
            'batting_stats': self._get_batting_stats(player_id),
            'bowling_stats': self._get_bowling_stats(player_id)
        }

    def _get_batting_stats(self, player_id: str) -> List[Dict]:
        """Get batting statistics for a player"""
        url = f"{self.config.BASE_URL}/player/{player_id}/batting"
        data = self._make_request(url)
        return self._process_stats(data) if data else []

    def _get_bowling_stats(self, player_id: str) -> List[Dict]:
        """Get bowling statistics for a player"""
        url = f"{self.config.BASE_URL}/player/{player_id}/bowling"
        data = self._make_request(url)
        return self._process_stats(data) if data else []

    @staticmethod
    def _process_stats(data: Dict) -> List[Dict]:
        """Process raw statistics data into a structured format"""
        headers = data.get('headers', [])
        stats_values = data.get('values', [])
        processed_stats = []

        for stat in stats_values:
            category_values = stat.get('values', [])
            if category_values:
                processed_stat = {'name': category_values[0]}
                for i in range(1, len(headers)):
                    processed_stat[headers[i]] = category_values[i]
                processed_stats.append(processed_stat)

        return processed_stats