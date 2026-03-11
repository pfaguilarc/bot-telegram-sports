import requests
from app.config import settings

class FootballAPI:
    def __init__(self):
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            'x-rapidapi-key': settings.API_FOOTBALL_KEY,
            'x-rapidapi-host': settings.API_FOOTBALL_HOST
        }
    
    def get_live_matches(self):
        """Obtener partidos en vivo"""
        try:
            response = requests.get(
                f"{self.base_url}/fixtures?live=all",
                headers=self.headers,
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_leagues_by_country(self, country):
        """Obtener ligas por país"""
        try:
            response = requests.get(
                f"{self.base_url}/leagues?country={country}",
                headers=self.headers,
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_fixtures_by_league(self, league_id, season=2024):
        """Obtener partidos de una liga"""
        try:
            response = requests.get(
                f"{self.base_url}/fixtures?league={league_id}&season={season}",
                headers=self.headers,
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

football_api = FootballAPI()