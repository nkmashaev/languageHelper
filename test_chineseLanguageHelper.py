import pytest
from chineseLanguageHelper import get_pinyin_list
from chineseLanguageHelper import get_tokenized_pinyin_str
from chineseLanguageHelper import get_tokenized_pinyin
from chineseLanguageHelper import clean_text
from chineseLanguageHelper import convert_to_marks
from chineseLanguageHelper import convert_to_plain

@pytest.mark.parametrize("input,expected", [
    # Test with latin and numbers
    ("我的T恤衫100元。", 
    ["wo", "de", "T", "xu", "shan", "100", "yuan", "."]),

    # Test simple sentence
    ("可以刷卡吗？",
    ["ke", "yi", "shua", "ka", "ma", "?"]),

    # Test sentence with two parts
    ("小明买完东西，回家了。",
    ["xiao", "ming", "mai", "wan", "dong", "xi", ",", "hui", "jia", "le", "."]),

    # Test 还 as huan
    ("跟​我​讨​价​还​价​，你​还​不​够​格​呢​。",
    ["gen", "wo", "tao", "jia", "huan", "jia", ",", "ni", "hai", "bu", "gou", "ge", "ne", "."]),

    # Test 还 as hai
    ("我们家还有一只这样的狗。",
    ["wo", "men", "jia", "hai", "you", "yi", "zhi", "zhe", "yang", "de", "gou", "."])
])
def test_get_pinyin_list(input, expected):
    cleaned_input = clean_text(input)
    actual = [convert_to_plain(pinyin_with_numbers) for pinyin_with_numbers in get_pinyin_list(cleaned_input)]
    assert actual == expected

@pytest.mark.parametrize("input,expected", [
    # Empty context
    ("", []),

    # Test with latin and numbers
    ("我的T恤衫100元。", 
    ["wo", "de", "Txushan", "100", "yuan", "."]),

    # Test simple sentence
    ("可以刷卡吗？",
    ["keyi", "shuaka", "ma", "?"]),

    # Test sentence with two parts
    ("小明买完东西，回家了。",
    ["xiaoming", "mai", "wan", "dongxi", ",", "huijia", "le", "."]),

    # Test 还 as huan
    ("跟​我​讨​价​还​价​，你​还​不​够​格​呢​。",
    ["gen", "wo", "taojiahuanjia", ",", "ni", "hai", "bu", "gouge", "ne", "."]),

    # Test 还 as hai
    ("我们家还有一只这样的狗。",
    ["women", "jia", "haiyou", "yi", "zhi", "zheyang", "de", "gou", "."])
])
def test_get_tokenized_pinyin(input, expected):
    actual = get_tokenized_pinyin(input, style="plain")
    assert actual == expected

@pytest.mark.parametrize("input,expected", [
    # Empty list
    ([], ""),

    # Test with latin and numbers
    ("我的T恤衫100元。", 
    "wo de Txushan 100 yuan."),

    # Test simple sentence
    ("可以刷卡吗？",
    "keyi shuaka ma?"),

    # Test sentence with two parts
    ("小明买完东西，回家了。",
    "xiaoming mai wan dongxi, huijia le."),

    # Test 还 as huan
    ("跟​我​讨​价​还​价​，你​还​不​够​格​呢​。",
    "gen wo taojiahuanjia, ni hai bu gouge ne."),

    # Test 还 as hai
    ("我们家还有一只这样的狗。",
    "women jia haiyou yi zhi zheyang de gou.")
])
def test_get_tokenized_pinyin_str(input, expected):
    tokenized_input = get_tokenized_pinyin(input, style="plain")
    print(tokenized_input)
    actual = get_tokenized_pinyin_str(tokenized_input)
    assert actual == expected