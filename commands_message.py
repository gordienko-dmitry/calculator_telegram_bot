from enum import Enum
import ephem
import datetime

from telegram import ReplyKeyboardMarkup
import texts
from calc import calculate


class mode_of_bot(Enum):
    EMPTY = 0
    CALC = 1
    CALC_text = 2
    CALC_buttons = 3
    CALC_words = 4
    GORODA = 5
    PLANETS = 6
    WORDCOUNT = 7


menu_button = 'Меню'
cancel_button = ['Отмена']
empty_keyboard = ReplyKeyboardMarkup([[]], resize_keyboard=True, one_time_keyboard=True)
base_keyboard = ReplyKeyboardMarkup([['Счетчик слов'], ['Калькулятор'], ['Города'], 
                                    ['Планеты и созвездия'], ['Полнолуние'], ['Информация о боте']],
                                    resize_keyboard=True, one_time_keyboard=True)


def get_answer_message(bot, text):
    text_functrion = {'счетчик слов': wordcount, 'калькулятор': calculate_mode,
            'города': goroda, 'информация о боте': about, 'отмена': cancel, 'планеты и созвездия': planets}

    if bot.mode != mode_of_bot.EMPTY and text.lower() != 'отмена':
        return special_mode(bot, text)
    print(text)
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
    if bot.mode == mode_of_bot.EMPTY:
        bot.mode = mode_of_bot.CALC
        answer_text = texts.CALC_1

        buttons = [['Текстовый'], ['Кнопочный'], ['Словесный']]
        buttons.append(cancel_button)
        reply_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        return answer_text, reply_keyboard

    if bot.mode == mode_of_bot.CALC:
        bot.mode = mode_of_bot(texts.CALC_TYPE.get(text.capitalize(), 1))
        if bot.mode == mode_of_bot.CALC:
            answer_text = 'Попробуйте еще раз'
            answer_text, None
        else:
            answer_text = texts.CALC_TEXT_1
            buttons = [cancel_button]
            reply_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

            return answer_text, reply_keyboard
    
    if bot.mode == mode_of_bot.CALC_text:
        result, without_error = calculate(text)
        if without_error:
            buttons = [cancel_button]
            reply_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

            return [texts.CALC_TEXT_RESULT.format(result), texts.CALC_TEXT_2], reply_keyboard


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


def shedule_dates(bot, text):
    if texts.SHEDULE_DATES.count(text) > 0:
        ind = texts.SHEDULE_DATES.index(text)
        answer_text = texts.SHEDULE_TEXT_1.format(text, texts.SHEDULE_THEMES[ind]) + texts.SHEDULE[ind]
        bot.mode = mode_of_bot.EMPTY
        return answer_text, base_keyboard
    else:
        answer_text = texts.TEST_ERROR
        return answer_text, None





def test(bot):
    bot.mode = mode_of_bot.TEST
    bot.test = {'test_step': 0, 'test_variant': 0, 'test_answers': []}

    answer_text = texts.TEST_TEXT_0

    buttons = [[texts.TEST_THEMES[i] for i in range(3)]]
    buttons.append(cancel_button)
    reply_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    return answer_text, reply_keyboard


def get_test_step(variant, step):
    answer_text = texts.TEST_TEXT_1.format(step) + '\n\n' + texts.TEST_QUESTIONS[variant-1][step-1]
    buttons = [texts.TEST_VARIANT[variant-1][step-1]]
    buttons.append(cancel_button)
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    return answer_text, keyboard


def solve_test(bot, variant):
    count_right = 0
    for ind, answer in enumerate(TEST_ANSWERS[variant - 1]):
        count_right += 1 if answer == bot.test.get('test_answers', [])[ind] else 0

    bot.test = {'test_step': 0, 'test_variant': 0, 'test_answers': []}
    bot.mode = mode_of_bot.EMPTY

    answer_text = 'Результаты теста:\n\n Вы дали {} верных ответов, это {:2.2f} % \n\n Сами сделайте вывод'. \
        format(count_right, count_right / 3 * 100)
    return answer_text, base_keyboard


def test_steps(bot, text):
    test_step = bot.test.get('test_step', 0)
    test_variant = bot.test.get('test_variant', 0)

    if test_step == 0:
        if texts.TEST_THEMES.count(text) > 0:
            ind = texts.TEST_THEMES.index(text.capitalize())
            bot.test['test_variant'] = ind + 1
            bot.test['test_step'] = 1
            answer_text, keyboard = get_test_step(bot.test.get('test_variant', 0), 1)
            return answer_text, keyboard
        else:
            answer_text = 'Такого варианта нет'
            return answer_text, None

    else:
        if texts.TEST_VARIANT[test_variant - 1][test_step - 1].count(text) > 0:
            bot.test['test_answers'].append(texts.TEST_VARIANT[test_variant - 1][test_step - 1].index(text))

            if test_step == 3:
                return solve_test(bot, test_variant)

            bot.test['test_step'] += 1
            return get_test_step(test_variant, bot.test['test_step'])
        else:
            answer_text = texts.TEST_ERROR
            return answer_text, None


def shedule(bot):
    bot.mode = mode_of_bot.SHEDULE
    answer_text = texts.SHEDULE_TEXT_0

    buttons = [[texts.SHEDULE_DATES[i] for i in range(3)], [texts.SHEDULE_DATES[i] for i in range(3,6)],
               [texts.SHEDULE_DATES[i] for i in range(6,9)], [texts.SHEDULE_DATES[9]]]

    buttons.append(cancel_button)
    reply_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    return answer_text, reply_keyboard


def help_command(bot):
    return texts.HELP_TEXT, base_keyboard


def kurs(bot):
    return texts.KURS_TEXT, base_keyboard




def author(bot):
    return texts.AUTHOR, base_keyboard


def default(bot):
    print('def')
    return texts.ERROR_COMMAND, base_keyboard


def cancel(bot):
    return texts.TEXT_CANCEL, base_keyboard

