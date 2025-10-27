import requests
import json
from django.conf import settings
from django.utils.translation import gettext as _


def verify_recaptcha_enterprise(token, action='submit'):
    if not all([settings.RECAPTCHA_PROJECT_ID, settings.RECAPTCHA_API_KEY, settings.RECAPTCHA_SITE_KEY]):
        return {
            'success': False,
            'error': 'reCAPTCHA configuration incomplete'
        }
    
    url = settings.RECAPTCHA_VERIFY_URL.format(project_id=settings.RECAPTCHA_PROJECT_ID, api_key=settings.RECAPTCHA_API_KEY)
    
    assessment_data = {
        "event": {
            "token": token,
            "siteKey": settings.RECAPTCHA_SITE_KEY,
            "expectedAction": action
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    try:
        response = requests.post(url, json=assessment_data, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        
        if 'tokenProperties' in result and 'valid' in result['tokenProperties']:
            is_valid = result['tokenProperties']['valid']
            score = result.get('riskAnalysis', {}).get('score', 0.0)
            action_matched = result.get('tokenProperties', {}).get('action') == action
            
            return {
                'success': is_valid and action_matched,
                'score': score,
                'action_matched': action_matched,
                'raw_response': result
            }
        else:
            return {
                'success': False,
                'error': 'Invalid response format from reCAPTCHA Enterprise'
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'Request failed: {str(e)}'
        }
    except json.JSONDecodeError as e:
        return {
            'success': False,
            'error': f'Invalid JSON response: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }


def is_recaptcha_score_valid(score, threshold=None):
    if threshold is None:
        threshold = getattr(settings, 'RECAPTCHA_SCORE_THRESHOLD', 0.5)
    
    return score >= threshold
