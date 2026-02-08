
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import InputRequired, ValidationError, Length


class BubbleSortForm(FlaskForm):
    items = StringField(validators=[InputRequired(), Length(min=1, max=80)], render_kw={"placeholder": "e.g cats,dog,bik or -58,6,-8,3,2,5"})
    is_ascending = BooleanField("Ascending", default = True)

    submit = SubmitField("Sort")

    def validate_items(self, items):
        values = items.data.split(',')

        for i in range(len(values)):
            values[i] = values[i].strip()

        if "" in values:
            raise ValidationError("Please enter comma separated values with no blanks.")
        
        all_numbers = True

        for i in values:
            try:
                float(i)
            except ValueError:
                all_numbers = False
                break
        
        all_words = all(v.isalpha() for v in values)

        if not (all_numbers or all_words):
            raise ValidationError("Please enter either only valid numbers or only valid letters")