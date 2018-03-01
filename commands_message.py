from enum import Enum
import ephem
import datetime

from telegram import ReplyKeyboardMarkup
import texts
from calc import calculate
from word_to_calc import to_text_calc

class mode_of_bot(Enum):
    EMPTY = 0
    CALC = 1
    CALC_text = 2
    CALC_buttons = 3
    CALC_words = 4
    GORODA = 5
    PLANETS = 6
    WORDCOUNT = 7
    FULL_MOON = 8


menu_button = 'Меню'
cancel_button = ['Отмена']
empty_keyboard = ReplyKeyboardMarkup([[]], resize_keyboard=True, one_time_keyboard=True)
base_keyboard = ReplyKeyboardMarkup([['Счетчик слов'], ['Калькулятор'], ['Города'], 
                                    ['Планеты и созвездия'], ['Полнолуние'], ['Информация о боте']],
                                    resize_keyboard=True, one_time_keyboard=True)


def get_answer_message(bot, text):
    text_functrion = {'счетчик слов': wordcount, 'калькулятор': calculate_mode,
            'города': goroda, 'информация о боте': about, 'отмена': cancel, 'планеты и созвездия': planets, 
            'полнолуние': full_moon}

    if bot.mode != mode_of_bot.EMPTY and text.lower() != 'отмена':
        return special_mode(bot, text)
    #print(text)
    return text_functrion.get(text.lower(), default)(bot)


def get_answer_command(bot, user, text):

    # menu
    commands = {'/start': start, '/wordcount': wordcount, '/help': help_command,
        '/calc': calculate, '/goroda': goroda, '/about': about}

    bot.mode = mode_of_bot.EMPTY
    if text == '/start':
        name_to_call = get_name(user)
        return commands.get(text, default)().format(name_to_call), base_keyboard
    else:
        return commands.get(text, default)(bot)


def start():
    return texts.START_TEXT


def full_moon(bot, text=''):
    if bot.mode == mode_of_bot.FULL_MOON:
        try:
            date_moon = ephem.next_full_moon(text)
            answer_text = texts.FULL_MOON_2.format(date_moon)
            bot.mode = mode_of_bot.EMPTY 
            return answer_text, base_keyboard
        except ValueError:
            return texts.ERROR_DATE, None

    else:
        bot.mode = mode_of_bot.FULL_MOON
        answer_text = texts.FULL_MOON
        reply_keyboard = ReplyKeyboardMarkup([cancel_button], resize_keyboard=True, one_time_keyboard=True)
        return answer_text, reply_keyboard



def wordcount(bot,count=False,text=''):
    if count:
        text = text.replace('.',' ').replace(',',' ').replace('!',' ').replace('?', ' ').replace('   ',' ').replace('  ',' ').strip()
        
        if text == '':
            answer_text = texts.EMPTY_STRING
        else:
            count_text = text.split(' ')
            answer_text = texts.WORD_1.format(len(count_text))
        bot.mode = mode_of_bot.EMPTY
        return answer_text, base_keyboard
    else:
        bot.mode = mode_of_bot.WORDCOUNT
        answer_text = texts.WORD_0
        reply_keyboard = ReplyKeyboardMarkup([cancel_button], resize_keyboard=True, one_time_keyboard=True)
        return answer_text, reply_keyboard


def calculate_mode(bot,text=''):
    what_next = {mode_of_bot.EMPTY: first_calculate, mode_of_bot.CALC: type_calculate, 
                mode_of_bot.CALC_text: text_calculate, mode_of_bot.CALC_buttons: buttons_calculate, 
                mode_of_bot.CALC_words: words_calculate}

    return what_next.get(bot.mode, default_stop)(bot, text)


def buttons_calculate(bot, text):
    return 'Функция в разработке', None


def first_calculate(bot, text):
    bot.mode = mode_of_bot.CALC
    answer_text = texts.CALC_1
    buttons = [['Текстовый'], ['Кнопочный'], ['Словесный']]
    buttons.append(cancel_button)
    reply_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    return answer_text, reply_keyboard


def type_calculate(bot, text):
    bot.mode = mode_of_bot(texts.CALC_TYPE.get(text.capitalize(), 1))
    if bot.mode == mode_of_bot.CALC:
        answer_text = 'Попробуйте еще раз'
        return answer_text, None
    else:
        answer_text = texts.CALC_TEXT_1
        buttons = [cancel_button]
        reply_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        return answer_text, reply_keyboard
    

def text_calculate(bot, text):
    result, without_error = calculate(text)
    if without_error:
        buttons = [cancel_button]
        reply_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

        return [texts.CALC_TEXT_RESULT.format(result), texts.CALC_TEXT_2], reply_keyboard
    else:
        buttons = [cancel_button]
        reply_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

        return [result, texts.CALC_TEXT_2], reply_keyboard


def CALC_buttons(bot, text):
    return 'Функция в разработке', None


def words_calculate(bot, text):
    text_calc = to_text_calc(text.lower())
    result, without_error = calculate(text_calc)
    if without_error:
        buttons = [cancel_button]
        reply_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        return [text_calc.replace('*', '\*') + '\n' + texts.CALC_TEXT_RESULT.format(result), texts.CALC_TEXT_2_word], reply_keyboard
    else:
        buttons = [cancel_button]
        reply_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

        return [text_calc + '\n' + result, texts.CALC_TEXT_2], reply_keyboard


def goroda():
    pass


def planets(bot):
    bot.mode = mode_of_bot.PLANETS
    answer_text = texts.PLANETS_INFO
    buttons = [['Меркурий', 'Венера', 'Земля'], ['Марс', 'Юпитер', 'Сатурн'], ['Уран', 'Нептун']]
    buttons.append(cancel_button)
    reply_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    return answer_text, reply_keyboard


def about(bot):
    return texts.ABOUT_TEXT, base_keyboard


def get_name(user):
    name_to_call = user.first_name
    if name_to_call == '':
        name_to_call = user.first_name
        if name_to_call == '':
            name_to_call = user.username
        else:
            name_to_call = 'товарищ ' + name_to_call
    return name_to_call


def special_mode(bot, text):
    if bot.mode == mode_of_bot.PLANETS:
        return constellation(bot, text)
    if bot.mode == mode_of_bot.WORDCOUNT:
        return wordcount(bot, count=True,text=text)
    if bot.mode in [mode_of_bot.CALC, mode_of_bot.CALC_text, mode_of_bot.CALC_buttons, mode_of_bot.CALC_words]:
        return calculate_mode(bot, text)
    if bot.mode == mode_of_bot.FULL_MOON:
        return full_moon(bot, text)


def constellation(bot, text):
    
    name_planet = texts.planets.get(text.lower(), None)
    if name_planet is None:
        answer_text = texts.ERROR_PLANET
        return answer_text, empty_keyboard

    ephem_planet = getattr(ephem, name_planet)
    ephem_planet_date = ephem_planet(datetime.datetime.now())
    _, constellation_planet = ephem.constellation(ephem_planet_date)
    constellation_planet_rus = texts.constellation.get(constellation_planet, name_planet)
    result = 'Планета {} находится в созвездии {} '.format(text, constellation_planet_rus)
    bot.mode = mode_of_bot.EMPTY
    return result, base_keyboard



def help_command(bot):
    return texts.HELP_TEXT, base_keyboard


def author(bot):
    return texts.AUTHOR, base_keyboard


def default(bot):
    return texts.ERROR_COMMAND, base_keyboard


def cancel(bot):
    bot.mode = mode_of_bot.EMPTY
    return texts.TEXT_CANCEL, base_keyboard


def default_stop(bot, text):
    return texts.ERROR_COMMAND, None

