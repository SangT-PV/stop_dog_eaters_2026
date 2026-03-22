import os
from pathlib import Path
from dotenv import load_dotenv

_here = Path(__file__).parent
load_dotenv(_here / '.env')

# AWS Bedrock — used for Claude content synthesis
AWS_PROFILE = os.getenv('AWS_PROFILE', 'default')
AWS_REGION = os.getenv('AWS_DEFAULT_REGION') or os.getenv('AWS_REGION', 'us-east-1')
BEDROCK_MODEL_ID = os.getenv('BEDROCK_MODEL_ID', 'us.anthropic.claude-haiku-4-5-20251001-v1:0')

# Research APIs — used for automated daily news research
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY', '')
PERPLEXITY_ENABLED = bool(PERPLEXITY_API_KEY)

MANUS_API_KEY = os.getenv('MANUS_API_KEY', '')
MANUS_ENABLED = bool(MANUS_API_KEY)

# Telegram — optional; publishing is skipped when these are not set
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID', '')
TELEGRAM_ENABLED = bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID)

CHANGE_ORG_URL = os.getenv('CHANGE_ORG_URL', 'https://www.change.org/p/end-dog-meat-trade-vietnam')
WEBSITE_URL = os.getenv('WEBSITE_URL', 'https://stopdogeaters.info')

# Facebook — optional; publishing is skipped when these are not set
FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID', '')
FACEBOOK_PAGE_TOKEN = os.getenv('FACEBOOK_PAGE_TOKEN', '')
FACEBOOK_ENABLED = bool(FACEBOOK_PAGE_ID and FACEBOOK_PAGE_TOKEN)

WEBSITE_DATA_DIR = (_here.parent / 'website' / 'data').resolve()
WEBSITE_ASSETS_DIR = (_here.parent / 'website' / 'assets').resolve()
INPUTS_DIR = (_here / 'inputs').resolve()
LOGS_DIR = (_here / 'logs').resolve()
