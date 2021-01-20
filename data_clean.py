import re

string = "https://resizing.flixster.com/f8hhEBZOgRZaY31Rx5P6P93WW24=/fit-in/200x296.2962962962963/v1.bTsxMjU0NjIzNDtqOzE4Njg1OzEyMDA7MTY4ODsyNTAw 1024w, https://resizing.flixster.com/mNWgYYGsgEzCEoubTXRhegK90n8=/fit-in/124x183.7037037037037/v1.bTsxMjU0NjIzNDtqOzE4Njg1OzEyMDA7MTY4ODsyNTAw 768w"

print(re.match('([^\s]+)', string))
