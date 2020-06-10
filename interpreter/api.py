import sys
import string

import exception
import namespace


namespace = namespace.Namespace()
self = sys.modules[__name__]

bool_vars = {
    'true': True,
    'false': False,
    '1': True,
    '0': False,
}


def out(*text, line='null', **kwargs):
    print(*text, **kwargs)

    # return ' '.join(text)


def inp(to_var=None, text=None, line='null'):
    if to_var is None:
        text = ''
    elif text is None:
        text = to_var
    else:
        to_var = to_var[1:]

    text = input(text)

    if to_var is not None:
        namespace.put(to_var, text)

    return text.replace('"', '\\"')


def var(varname, *content, line='null'):
    namespace.put(varname[1:], ' '.join(content))


def call(func, args=(), kwargs=None, line='null'):
    if kwargs is None:
        kwargs = {}

    if callable(func):  # if we have a function object (not it's name)
        func = func.__name__

    function = getattr(self, func)

    return function(*args, line=line, **kwargs)


def add(*args, line='null'):
    result = sum(map(int, args[1:]))

    if args[0].isdigit():
        result += int(args[0])
    else:
        if args[0] != '&':
            _var = args[0][1:]
        else:
            _var = args[0]

        namespace.put(_var, result)

    return result


def minus(*args, line='null'):
    result = int(args[1])

    if args[0].isdigit():
        result = int(args[0]) - result
    else:
        namespace.put(args[0], result)

    try:
        for num in args[2:]:
            result -= num
    except IndexError:
        pass

    return result


def seq(*sequence, line='null'):
    sequence = ' '.join(sequence)

    if any([i in string.ascii_letters.replace('e', '') for i in sequence]):
        return 'error:bad sequence'

    try:
        return eval(sequence)
    except Exception as exc:
        exception.throw('bad_sequence', 'bad sequence:', exc, line=line)


def pass_line(*args, **kwargs):
    return


def delvar(*variables, line='null'):
    for variable in variables:
        namespace.rm(variable, line=line)


def exit_(code=None, reason=None, line='null'):
    print('\nAborted', '(' + str(reason) + ')' if reason is not None else '')

    try:
        sys.exit(int(code))
    except (ValueError, TypeError):
        sys.exit(1)


def set_immortality(value, line='null'):
    try:
        exception.EXIT_ON_EXCEPTION = not bool_vars[value]
    except KeyError:
        exception.throw('bad_state', 'unknown value for function "setimm": ' + str(value), line=line)


def get_functions():
    return {
        'out': out,
        'inp': inp,
        'in': inp,
        'var': var,
        'call': call,
        'add': add,
        'min': minus,
        'seq': seq,
        'del': delvar,
        'pass': pass_line,
        'exit': exit_,
        'setimm': set_immortality,
    }