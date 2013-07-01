from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.form import FormMeta
from surveyor import get_survey

class DynamicSurveyFormMeta(FormMeta):
    def __call__(cls, survey_name, *args, **kwargs):
        if survey_name and not hasattr(cls, "survey_name"):
            survey = get_survey(survey_name)
            if not survey:
                raise Exception("No survey by that name")

            cls.survey_name = survey_name
            for f in survey["fields"]:
                field = globals()[f["type"]](f["name"])
                setattr(cls, f["slug"], field)

        return super(DynamicSurveyFormMeta, cls).__call__(*args, **kwargs)

class DynamicSurveyForm(Form):
    """Create a Flask-WTF form based on settings saved in MongoDB."""
    __metaclass__ = DynamicSurveyFormMeta
