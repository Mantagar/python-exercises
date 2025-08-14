import pytest
from roman import Roman

valid_cases = [
	# all numerals
	("MDCLXVI", 1666),
	# repeated numerals
	("MMM", 3000),
	("MM", 2000),
	("CCC", 300),
	("CC", 200),
	("XXX", 30),
	("XX", 20),
	("III", 3),
	("II", 2),
	# one less
	("CM", 900),
	("CD", 400),
	("XC", 90),
	("XL", 40),
	("IX", 9),
	("IV", 4),
]

invalid_roman = [
	# invalid repetition
	"IIII",
	"VV",
	"XXXX",
	"LL",
	"CCCC",
	"DD",
	"MMMM",
	# wrong order
	"IIX",
	"IIV",
	"VX",
	"XXC",
	"XXL",
	"LC",
	"CCM",
	"CCD",
	"DM"
	"VL"
	"VD"
	"LD"
]

invalid_arabic = [
	0,
	-1,
	4000
]

@pytest.mark.parametrize("roman_str, expected", valid_cases)
def test_roman_to_arabic_valid(roman_str, expected):
	arabic = Roman.roman_to_arabic(roman_str)
	assert arabic == expected 

@pytest.mark.parametrize("roman_str", invalid_roman)
def test_roman_to_arabic_invalid(roman_str):
	with pytest.raises(ValueError):
		Roman.roman_to_arabic(roman_str)

@pytest.mark.parametrize("expected, arabic", valid_cases)
def test_arabic_to_roman_valid(expected, arabic):
	roman_str = Roman.arabic_to_roman(arabic)
	assert roman_str == expected 

@pytest.mark.parametrize("arabic", invalid_arabic)
def test_roman_to_arabic_invalid(arabic):
	with pytest.raises(ValueError):
		Roman.arabic_to_roman(arabic)

