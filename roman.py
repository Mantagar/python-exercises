import re

class Roman():
  MAPPING = (
    ("MMM", 3000),
    ("MM", 2000),
    ("M", 1000),
    ("CM", 900),
    ("DCCC", 800),
    ("DCC", 700),
    ("DC", 600),
    ("D", 500),
    ("CD", 400),
    ("CCC", 300),
    ("CC", 200),
    ("C", 100),
    ("XC", 90),
    ("LXXX", 80),
    ("LXX", 70),
    ("LX", 60),
    ("L", 50),
    ("XL", 40),
    ("XXX", 30),
    ("XX", 20),
    ("X", 10),
    ("IX", 9),
    ("VIII", 8),
    ("VII", 7),
    ("VI", 6),
    ("V", 5),
    ("IV", 4),
    ("III", 3),
    ("II", 2),
    ("I", 1)
  )
  PATTERN = re.compile(
    "^{}{}{}{}$".format(
      "M{0,3}",
      "(CM|DC{0,3}|CD|C{1,3}|)",
      "(XC|LX{0,3}|XL|X{1,3}|)",
      "(IX|VI{0,3}|IV|I{1,3}|)"
    )
  )
  
  def roman_to_arabic(roman_str):
    if re.search(Roman.PATTERN, roman_str) == None:
      raise ValueError()

    total = 0
    for roman_numeral, roman_value in Roman.MAPPING:
      if roman_str.startswith(roman_numeral):
        roman_str = roman_str.split(roman_numeral, 1)[1]
        total += roman_value
    return total

  def arabic_to_roman(value):
    if value < 1 or value > 3999:
      raise ValueError()

    roman_repr = ""
    for roman_numeral, roman_value in Roman.MAPPING:
      if value >= roman_value:
        value -= roman_value
        roman_repr += roman_numeral
    return roman_repr
