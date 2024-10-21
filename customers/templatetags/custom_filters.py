from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    # Adding a class to the field's widget
    return field.as_widget(attrs={'class': css_class})



@register.filter
def sub(value, arg):
    return value - arg


# تابعی برای تبدیل اعداد به فارسی
def to_persian_number(number):
    persian_digits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
    # Remove any non-digit characters before conversion
    number_str = ''.join(c for c in str(number) if c.isdigit())
    return ''.join(persian_digits[int(digit)] for digit in number_str)

# تابعی برای جدا کردن اعداد
def separate_thousands(number):
    number_str = str(number)[::-1]  # معکوس کردن رشته
    grouped = [number_str[i:i + 3] for i in range(0, len(number_str), 3)]
    return ','.join(grouped)[::-1]  # مجدداً معکوس کردن رشته

@register.filter
def pnumber_style(value):
    
    persian_number = to_persian_number(value)
    separated_number = separate_thousands(persian_number)
    
    return separated_number


@register.filter
def format_date(value):
    return value.strftime("%Y-%m-%d %H:%M")  # فرمت: سال-ماه-روز ساعت:دقیقه
    