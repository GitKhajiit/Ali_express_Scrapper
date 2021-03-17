from bot_requests import send_file
from scan_machine import aliexpress
from config import chat_id, tokens

aliexpress.find_title()
aliexpress.find_old_price()
aliexpress.find_new_price()
aliexpress.find_discount()
aliexpress.find_rating()
aliexpress.find_image_link()
aliexpress.write_to_txt()

# with open('page.html', 'w') as file:
#     file.write(aliexpress.page_content)

send_file(chat_id['post_lab_channel'], tokens['best_sales_bot'], 'post.txt')
