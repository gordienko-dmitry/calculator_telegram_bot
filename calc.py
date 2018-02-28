def calculate(text):
    text = text.replace(' ', '').replace('-','+-').replace('/','*1/')

    try: 
        count_bracket_open = text.count('(')
        count_bracket_close = text.count(')')
        if count_bracket_open != count_bracket_close:
            raise Exception('Проверьте количество открывающий и закрывающих скобок')
        if count_bracket_open == 0:
            return precalc(text, '+'), True
        return brackets(text), True
    
    except Exception as e:
        return e.args[0], False
    except ValueError:
        return 'Ошибка в выражении', False
    except ZeroDivisionError:
        return 'Насколько я помню - на ноль делить до сих пор нельзя', False

    
def brackets(text, level=0, brackets_dict={}):
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
    operands = text.split(oper)
    if oper in '+*':
        next_oper = '*' if oper == '+' else '/'
        result = 0 if oper == '+' else 1.0
        for num_operand in range(len(operands)):
            operand = precalc(operands[num_operand], next_oper, brackets_dict)
            if oper == '*':
                result *= operand
            else:
                result += operand
    else:
        result = float_bracket(operands[0], brackets_dict)
        for num_operand in range(1,len(operands)):
            result /= float_bracket(operands[num_operand], brackets_dict)
    return result


def float_bracket(operand, brackets_dict):
    if operand[:2] == 'br':
        result = brackets_dict.get(operand, None)
        if result is None:
            raise Exception('Не получилось вычислить значение в скобках')
        return brackets_dict.get(operand, 0)
    if operand[:3] == '-br':
        return -brackets_dict.get(operand[1:], 0)
    else:
        return float(operand)



