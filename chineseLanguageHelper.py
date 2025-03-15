import spacy
import pypinyin
import re
import functools
import string
from pinyin_tone_converter.pinyin_tone_converter import PinyinToneConverter

# Global variables
NLP = spacy.load("zh_core_web_lg")
TEXT_REGEX = re.compile(r'[^\u4e00-\u9fff0-9a-zA-Z，。？！：；（）【】、，]') 
DIGIT_REGEX = re.compile(r'\d') 
PUNCTUATION_MAP = {
    '，': ',',  # китайская запятая на европейскую
    '。': '.',  # китайская точка на европейскую
    '！': '!',  # китайский восклицательный знак на европейский
    '？': '?',   # китайский вопросительный знак на европейский
    '：': ':',   # китайский двоеточие на европейское
    '；': ';',   # китайская точка с запятой на европейскую
    '（': '(',   # китайская открывающая скобка на европейскую
    '）': ')',   # китайская закрывающая скобка на европейскую
    '【': '[',   # китайская квадратная скобка на европейскую
    '】': ']',   # китайская квадратная скобка на европейскую
    '、': ',',   # китайский знак перечисления на запятую
    '—': '-',    # китайский длинный тире на европейское
}

def convert_to_plain(pinyin_with_numbers):
    if is_number(pinyin_with_numbers):
        return pinyin_with_numbers
    return DIGIT_REGEX.sub('', pinyin_with_numbers)

def convert_to_marks(pinyin_with_numbers):
    if is_number(pinyin_with_numbers):
        return pinyin_with_numbers
    return PinyinToneConverter().convert_text(pinyin_with_numbers)

def is_number(s):
    try:
        float(s)  # пытаемся преобразовать строку в вещественное число
        return True
    except ValueError:
        return False

def clean_text(text):
    cleaned_text = TEXT_REGEX.sub('', text)
    return cleaned_text

def get_pinyin_list(context):
    pinyin_list = pypinyin.pinyin(context, style=pypinyin.STYLE_TONE3, heteronym=False)
    # TODO: add check whether all of the sublists of the pinyin_list are of the size 1

    pinyin_list_flattened = functools.reduce(lambda acc, new_pinyin: acc + [new_pinyin[0]], pinyin_list, [])
    for i, pinyin in enumerate(pinyin_list_flattened):
        if pinyin in PUNCTUATION_MAP:
            pinyin_list_flattened[i] = PUNCTUATION_MAP[pinyin]
    return pinyin_list_flattened

def get_tokenized_context(context):
    tokenized_context = NLP(context)
    return [token for token in tokenized_context]

def get_tokenized_pinyin(context, style=None):
    if not context:
        return []
    cleaned_context = clean_text(context)
    tokenized_context = get_tokenized_context(cleaned_context)
    pinyin_list = get_pinyin_list(cleaned_context)

    if style is None:
        format_pinyin = lambda x: x
    elif style.lower().strip() == "plain":
        format_pinyin = convert_to_plain
    elif style.lower().strip() == "marks":
        format_pinyin = convert_to_marks
        
    k = 0
    tokenized_pinyin = []
    for token in tokenized_context:
        token_str = str(token)
        token_size = 1 if is_number(token_str) else len(token_str)

        sub_list = [format_pinyin(pinyin_with_numbers) for pinyin_with_numbers in pinyin_list[k:k+token_size]]
        tokenized_pinyin.append(''.join(sub_list))
        k = k + token_size
    return tokenized_pinyin

def get_tokenized_pinyin_str(tokenized_pyinin):
    if not tokenized_pyinin:
        return ""
    
    str_list = [str(tokenized_pyinin[0])]
    for token in tokenized_pyinin[1:]:
        token_str = str(token)
        if token_str in string.punctuation:
            str_list.append(token_str)
        else:
            str_list.append(" " + token_str)
    return "".join(str_list)