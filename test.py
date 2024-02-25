from mimesis import Person, Datetime, Text, Generic
from mimesis.locales import Locale


# person = Person(Locale.UK)
#
# print(person.full_name())
# print(person.email())
# print(person.phone_number())
#
# text = Text(Locale.UK)
#
# print(text.quote())
# print(text.title())
#
# date = Datetime(Locale.UK)
#
# print(date.datetime())
# print(date.formatted_date())
# print(date.date())

generic = Generic(Locale.UK)

print(generic.person.name())
print(generic.datetime.date())
