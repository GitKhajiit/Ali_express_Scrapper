import requests


def get_update(chat_id, token, update_id):
    '''
    This function return update(update, post, etc...) from chat in telegram
    Arguments:
        chat_id - chat where you find the update
        token - token for bot which will return update
        update_id - update with this id will be your response
    '''
    update_paramas = {
        'data': {
            'offset': update_id,
        },
    }
    response = requests.post(  # sends request and recive response
        f"https://api.telegram.org/bot{token}/getUpdates",
        data=update_paramas['data'],
    )
    if response.ok:
        print('get_update success')
        return response.json()
    else:
        print('get_update failed')


def get_update_text(chat_id, token, update_id):
    '''
    Get text content of the message in update
    Arguments:
        chat_id - chat where you find the update message text
        token - token for bot which will return update
        update_id - update with this id will be your response
    '''
    response = get_update(chat_id, token, update_id)
    message_text = response['result'][0]['message']['text']
    return message_text


def send_message(chat_id, token, message):
    '''
    This function sends text message to chat by bot
    Arguments:
        chat_id - bot will send update to chat or channel with this id
        token - bot`s token
        message - just message in string format
    '''
    message_paramas = {
        'data': {
            'chat_id': chat_id,
            'text': message,
        },
    }
    response = requests.post(  # sends request and recive response
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=message_paramas['data'],
    )
    if response.ok:
        print('send_message success')
        return response.ok
    else:
        print('send_message failed')
        return response.ok


def send_file(chat_id, token, file, parse_mode='HTML'):
    '''
    This function sends file as message to chat by bot
    Arguments:
        chat_id - bot will send file to chat or channel with this id
        token - bot`s token
        file - path to file
        parse_mode - in which format file will send to telegram
    '''
    with open(file, 'rb') as tel_post:
        opened_file = tel_post.read()
    message_paramas = {
        'data': {
            'chat_id': chat_id,
            'text': opened_file,
            'parse_mode': parse_mode,
        },
    }
    response = requests.post(  # sends request and recieve response
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=message_paramas['data'],
    )
    if response.ok:
        print('send_file success')
        return response.ok
    else:
        print('send_file failed')
        return response.ok
