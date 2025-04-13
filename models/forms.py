from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class MovieSetupForm(FlaskForm):
    movie_title = StringField('Movie Title', validators=[DataRequired()])
    
    genre = SelectField('Genre', choices=[
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('scifi', 'Science Fiction'),
        ('family', 'Family')
    ], validators=[DataRequired()])
    
    budget = IntegerField(
        'Production Budget (in Crores ₹)', 
        validators=[
            DataRequired(),
            NumberRange(min=1, max=500, message="Budget must be between 1 and 500 crores")
        ],
        default=50
    )
    
    marketing_budget = IntegerField(
        'Marketing Budget (in Crores ₹)', 
        validators=[
            DataRequired(),
            NumberRange(min=1, max=200, message="Marketing budget must be between 1 and 200 crores")
        ],
        default=20
    )
    
    target_audience = SelectField('Target Audience', choices=[
        ('general', 'General Audience'),
        ('family', 'Family'),
        ('youth', 'Youth'),
        ('adult', 'Adult')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Start Analysis')