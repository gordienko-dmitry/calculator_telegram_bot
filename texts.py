from version import version

START_TEXT ="Приветствую тебя, {}! \n"\
            "Меня зовут Николастас, и я могу кое-что, ща покажу"

HELP_TEXT = 'Вот, что я умею:\n\n'\
            '/help - показать весь список доступных команд\n'\
            '/wordcount - расписание\n'\
            '/curs - о курсе\n'\
            '/test - запустить проверку знаний\n'\
            '/about - обо мне'


ABOUT_TEXT = 'exercise learn python bot v{}\nby Gordienko Dmitry'.format(version)

ERROR_COMMAND = 'Такой команды не предусмотрено'

TEXT_CANCEL = 'Добро пожаловать в главное меню'

ERROR_PLANET = 'Такой планеты не найдено'

PLANETS_INFO = 'Выберите планету'

planets = {'Меркурий': 'Mercury', 'венера': 'Venus', 'земля': 'Earth', 'марс': 'Mars',
            'юпитер': 'Jupiter', 'сатурн': 'Saturn', 'уран': 'Uranus', 'нептун': 'Neptune' }

constellation = {'Aries': 'Овен', 'Taurus': 'Телец', 'Gemini': 'Близнецы', 'Cancer': 'Рак', 'Leo': 'Лев', 'Virgo': 'Дева',
            'Libra': 'Весы', 'Scorpius': 'Скорпион', 'Ophiuchus': 'Змееносец', 'Sagittarius': 'Стрелец', 'Capricornus': 'Козерог',
            'Aquarius': 'Водолей', 'Pisces':'Рыбы'}
