import requests
import re
from bs4 import BeautifulSoup
from currency_exchanger import get_currency_exchage
from bot_requests import get_update_text
from config import chat_id, tokens


last_message_data_str = get_update_text(chat_id['best_sales_bot'], tokens['best_sales_bot'], '-1')
last_message_data_list = last_message_data_str.split(' ')
post_dict = {
    'title': '',
    'discount': '',
    'old_price': '',
    'new_price': '',
    'rating': '',
}  # Dict with post elements for writing in txt file


class shopPage():
    link_to_page = last_message_data_list[0]
    try:
        words_count = last_message_data_list[1]
    except IndexError:
        words_count = 7
    page_content = requests.get(link_to_page).text
    currency = get_currency_exchage('RUB', 'UAH')

    def find_title(self):  # Extract the title from HTML
        soup = BeautifulSoup(self.page_content, 'lxml')
        title = soup.find('title').contents[0]  # find tag content with title
        all_title_list = title.split(' ')  # make list from title
        num_of_words = self.words_count  # witch count of words will add to post
        lim_title_list = [all_title_list[i] for i in range(int(num_of_words))]  # make list necessary words
        lim_title = ' '.join(lim_title_list)  # make correct title from list
        post_dict['title'] = lim_title

    def find_discount(self, post_write=True):
        try:
            raw_discount = re.findall('"discount":(\d\d|\d)', self.page_content)[0]
            discount_str = raw_discount.replace('"discount":', '')
            discount_num = int(discount_str)
        except IndexError:
            discount_num = 1
        detailed_discount = f'Скидка на товар по ссылке: - {discount_num}% !!'
        post_dict['discount'] = ''
        if post_write is True:
            if discount_num > 1:
                post_dict['discount'] = detailed_discount
            else:
                post_dict['discount'] = 'discount not found'
        else:
            return discount_num

    def find_old_price(self, post_write=True):  # Parse the price in html doc
        raw_price = re.findall('formatedPrice":".{,30}руб', self.page_content)[0]  # regex search of stirng with price
        list_for_del = ['formatedPrice":"', 'руб', ',', '\xa0', ' ']  # list of unnecessary text parts
        corr_price = raw_price  # copy of raw text for correction
        corr_price = corr_price.replace(',', '.')
        for for_del in list_for_del:  # delete unnecessary text
            corr_price = corr_price.replace(f'{for_del}', '')

        if '-' in corr_price:  # execute code if it price range
            old_str_prices_list = corr_price.split('-')  # make list with start and end price
            old_num_prices_list = [float(price) for price in old_str_prices_list]  # convert str to num
            min_price = old_num_prices_list[0]
            max_price = old_num_prices_list[1]
            if post_write is True:
                detailed_old_price = f'Старая цена: {min_price} - {max_price} руб / {round(min_price*self.currency, 2)} - {round(max_price*self.currency, 2)} грн'
                post_dict['old_price'] = detailed_old_price
            else:
                return old_num_prices_list
        else:  # execute code if it single price
            old_num_price = float(corr_price)
            if post_write is True:
                detailed_old_price = f'Старая цена: {old_num_price} руб / {round(old_num_price*self.currency, 2)} грн'
                post_dict['old_price'] = detailed_old_price
            else:
                return old_num_price

    def find_new_price(self, post_write=True):
        discount = self.find_discount(post_write=False)
        old_price = self.find_old_price(post_write=False)
        if type(old_price) == list:
            new_num_prices_list = [round(price-(discount*int(price)/100), 2) for price in old_price]
            min_price = new_num_prices_list[0]
            max_price = new_num_prices_list[1]
            if post_write is True:
                detailed_new_price = f'Новая цена: {min_price} - {max_price} руб / {round(min_price*self.currency, 2)} - {round(max_price*self.currency, 2)} грн'
                post_dict['new_price'] = detailed_new_price
            else:
                return new_num_prices_list
        elif type(old_price) == float:
            new_num_price = round(old_price-(discount*int(old_price)/100), 2)
            if post_write is True:
                detailed_new_price = f'Новая цена: {new_num_price} руб / {round(new_num_price*self.currency, 2)} грн'
                post_dict['new_price'] = detailed_new_price
            else:
                return new_num_price

    def find_rating(self):  # Find the rating
        raw_rating = re.findall('averageStar":"\d.\d', self.page_content)[0]
        rating_str = raw_rating.replace('averageStar":"', '')
        rating_num = int(round(float(rating_str), 0))
        detailed_rating = 'Средняя оценка: ' + '&#11088'*rating_num
        if rating_num > 0:
            post_dict['rating'] = detailed_rating
        else:
            post_dict['rating'] = 'rating not found'

    def find_image_link(self):  # Find the link of main image of the product
        raw_image_link = re.findall('https://.{,120}50x50.(?:jpg|png)', self.page_content)[0]
        print(raw_image_link)
        image_link_str = raw_image_link.replace('50x50', '')
        post_dict['image_link'] = image_link_str

    def write_to_txt(self):
        with open('post.txt', 'w') as post:
            post.write(post_dict['title'] + '\n'*2)
            post.write(post_dict['discount'] + '\n'*2)
            post.write(post_dict['old_price'] + '\n'*1)
            post.write(post_dict['new_price'] + '\n'*2)
            post.write(post_dict['rating'] + '\n')
            post.write(f'<a href=\'{post_dict["image_link"]}\'>&#8203</a> \n')
            post.write(f'<a href=\'{self.link_to_page}\'>Ссылка — bit.ly/2LJsno</a>')


aliexpress = shopPage()
