from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.form import FormMeta

class DynamicSurveyFormMeta(FormMeta):
    def __call__(cls, survey, *args, **kwargs):
        if survey:
            cls.survey_name = survey["name"]
            for f in survey["fields"]:
                field = globals()[f["type"]](f["name"])
                setattr(cls, f["slug"], field)
        return super(DynamicSurveyFormMeta, cls).__call__(*args, **kwargs)

class DynamicSurveyForm(Form):
    """Create a Flask-WTF form based on settings saved in MongoDB."""
    __metaclass__ = DynamicSurveyFormMeta
