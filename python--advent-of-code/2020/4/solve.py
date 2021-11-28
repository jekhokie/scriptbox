#!/usr/bin/env python3

import re

lines = []
with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

def get_passports(lines):
  passport = ''
  passports = []
  for line in lines:
    if line != '':
      passport += ' {}'.format(line)
    else:
      try:
        birth_year = re.findall(r'byr:([^\s]+)', passport)[0]
        issue_year = re.findall(r'iyr:([^\s]+)', passport)[0]
        exp_year = re.findall(r'eyr:([^\s]+)', passport)[0]
        height = re.findall(r'hgt:([^\s]+)', passport)[0]
        hair_color = re.findall(r'hcl:([^\s]+)', passport)[0]
        eye_color = re.findall(r'ecl:([^\s]+)', passport)[0]
        passport_id = re.findall(r'pid:([^\s]+)', passport)[0]

        passports.append({'birth_year': birth_year,
                          'issue_year': issue_year,
                          'exp_year': exp_year,
                          'height': height,
                          'hair_color': hair_color,
                          'eye_color': eye_color,
                          'passport_id': passport_id})
        passport = ''
      except:
        # do nothing - invalid passport
        passport = ''
        continue

  return passports

def year_check(check_val, digits, min, max):
  try:
    if len(check_val) == digits and int(check_val) >= min and int(check_val) <= max:
      return True
  except:
    return False

  return False

def height_check(check_val):
  try:
    (height, unit) = re.findall(r'([0-9]+)(in|cm)', check_val)[0]
    height = int(height)
    if unit == 'cm':
      return (height >= 150 and height <= 193)
    else:
      return (height >= 59 and height <= 76)
  except:
    # do nothing - didn't find expected values
    return False

  return False

passports = get_passports(lines)

#--- challenge 1

print("Solution to challenge 1: {}".format(len(passports)))

#--- challenge 2

valid_passports = 0
for passport in passports:
  if (year_check(passport['birth_year'], 4, 1920, 2002) and
      year_check(passport['issue_year'], 4, 2010, 2020) and
      year_check(passport['exp_year'], 4, 2020, 2030) and
      height_check(passport['height']) and
      re.match('^#[0-9a-f]{6}$', passport['hair_color']) and
      re.match('(amb|blu|brn|gry|grn|hzl|oth)', passport['eye_color']) and
      re.match('^[0-9]{9}$', passport['passport_id'])):
    valid_passports += 1

print("Solution to challenge 2: {}".format(valid_passports))
