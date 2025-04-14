import requests
from typing import Optional
from app.config import config

class JobMarketTools:
    @staticmethod
    def get_job_trends(field: str, location: Optional[str] = None) -> dict:
        """Get current job market trends using Serper API"""
        params = {
            "q": f"latest trends in {field} jobs {location if location else ''}",
            "gl": "us"
        }
        
        headers = {
            "X-API-KEY": config.SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            "https://google.serper.dev/search",
            headers=headers,
            json=params
        )
        
        return {
            "trends": response.json().get("organic", []),
            "source": "Serper API"
        }

    @staticmethod
    def get_skill_demand(skill: str, location: Optional[str] = None) -> dict:
        """Get demand for specific skill using Adzuna API"""
        params = {
            "what": skill,
            "country": "us",
            "app_id": config.ADZUNA_APP_ID,
            "app_key": config.ADZUNA_APP_KEY
        }
        if location:
            params["where"] = location
            
        response = requests.get(
            "https://api.adzuna.com/v1/api/jobs/us/search/1",
            params=params
        )
        
        return {
            "count": response.json().get("count", 0),
            "results": response.json().get("results", []),
            "source": "Adzuna API"
        }

    @staticmethod
    def get_salary_estimates(job_title: str, location: Optional[str] = None) -> dict:
        """Get salary estimates using government labor statistics"""
        base_url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
        
        # This is a simplified example - you'd need to map job titles to BLS codes
        params = {
            "seriesid": ["OEUN0000000000000000000000000000"],
            "startyear": "2023",
            "endyear": "2023",
            "registrationkey": config.BLS_API_KEY
        }
        
        response = requests.post(
            base_url,
            json=params,
            headers={"Content-Type": "application/json"}
        )
        
        return {
            "data": response.json().get("Results", {}).get("series", []),
            "source": "BLS API"
        }

    @staticmethod
    def get_remote_jobs(limit: int = 5) -> dict:
        """Get remote job listings using Adzuna"""
        params = {
            "location0": "us__remote",
            "app_id": config.ADZUNA_APP_ID,
            "app_key": config.ADZUNA_APP_KEY,
            "results_per_page": limit
        }
        
        response = requests.get(
            "https://api.adzuna.com/v1/api/jobs/us/search/1",
            params=params
        )
        
        return {
            "jobs": response.json().get("results", []),
            "source": "Adzuna API"
        }