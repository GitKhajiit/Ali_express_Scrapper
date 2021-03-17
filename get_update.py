from bot_requests import get_update, get_update_text
from config import chat_id, tokens

response = get_update('193872955', tokens['best_sales_bot'], '-1')

response_text = get_update_text('193872955', tokens['best_sales_bot'], '-1')

print(response)
