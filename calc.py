from decimal import Decimal

def calculate(text):
    """Функция запуска расчета из вне
    Входной параметр: text - строка с числами и мат. знаками
    Возвращаем кортеж: текст ответа (или текст ошибки) и признак удачности операции
    p.s. замена - на +- и / на *1/ обусловлена разделением на одноранговые операции 
    по + в одном случае и по * в другом"""

    text = text.replace(' ', '').replace('-','+-').replace('/','*1/')

    try: 
        return prebrackets(text)
    except ValueError:
        return 'Ошибка в выражении', False
    except ZeroDivisionError:
        return 'Насколько я помню - на ноль делить до сих пор нельзя', False
    except Exception as e:
        return e.args[0], False


def prebrackets(text):
    """Функция определяет есть ли скобки и либо запускает привычный механизм без скобок, 
    либо отправляет на расчет выражения с учетом скобок"""

    count_bracket_open = text.count('(')
    count_bracket_close = text.count(')')
    if count_bracket_open != count_bracket_close:
        raise Exception('Проверьте количество открывающий и закрывающих скобок')
    if count_bracket_open == 0:
        return float(precalc(text, '+')), True
    return float(brackets(text)), True

    
def brackets(text, level=0, brackets_dict={}):
    """Обработка выражения в скобках
    Основная идея: если после первой открывающей скобки идет следующая открывающая, 
    то у нас вложенное выражение и надо его вычислять рекурсией
    если идет закрывающая скобка, то выражение в скобках можно вычислить, сохранить в словарь, 
    а в текст выражения подставить условное обозначение результата вычисления"""

    if level == 0:
        ind_open = text.find('(')
        while ind_open != -1:
            text = text[:ind_open] + brackets(text[ind_open:], level+1, brackets_dict)
            ind_open = text.find('(')
        return precalc(text, '+', brackets_dict)
    
    substring = ''
    ind_open = text[1:].find('(')
    ind_close = text[1:].find(')')
    if ind_close < ind_open or ind_open == -1:
        substring = text[1:ind_close+1]
        result_in_brackets = precalc(substring, '+', brackets_dict)
        brackets_dict['br_{}'.format(len(brackets_dict))] = result_in_brackets
        return text.replace("(" + substring + ")",'br_{}'.format(len(brackets_dict) - 1))
    else:
        return text[:ind_open+1] + brackets(text[ind_open+1:], level+1, brackets_dict)


def precalc(text, oper='+',brackets_dict={}):
    """Вычисление выражения
    Вычисление выражения происходит в три обхода данной функции:
    1. по знаку + (переменна oper)
    2. по знаку * (переменная oper)
    3. по знаку / - т.к. в начале мы преобразовали / на *1/  мы можем деление вынести в отдельный обход"""

    operands = text.split(oper)
    if oper in '+*':
        next_oper = '*' if oper == '+' else '/'
        result = Decimal('0' if oper == '+' else '1.0')
        for one_operand in operands:
            operand = precalc(one_operand, next_oper, brackets_dict)
            if oper == '*':
                result *= operand
            else:
                result += operand
    else:
        result = str2decimal(operands[0], brackets_dict)
        for num_operand in range(1,len(operands)):
            result /= str2decimal(operands[num_operand], brackets_dict)
    return result


def str2decimal(operand, brackets_dict):
    """Преобразование операнда к числовому виду,
    Это может быть просто число, а может быть значение скобки"""

    if operand[:2] == 'br':
        result = brackets_dict.get(operand, None)
        if result is None:
            raise Exception('Не получилось вычислить значение в скобках')
        return brackets_dict.get(operand, 0)
    if operand[:3] == '-br':
        return -brackets_dict.get(operand[1:], 0)
    else:
        return Decimal(operand)
        #return float(operand)



