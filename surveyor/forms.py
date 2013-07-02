from flask.ext.wtf import Form
from wtforms.form import FormMeta

class DynamicSurveyFormMeta(FormMeta):
    def __call__(cls, survey, *args, **kwargs):
        if survey:
            cls.survey_name = survey["name"]
            for f in survey["fields"]:
                # Search for an object matching _type in the global namespace.
                # Failing that, try importing said object from wtforms.
                # If found, set the object as a class attribute.
                _name, _slug, _type = f["name"], f["slug"], str(f["type"])
                field = globals().get(_type)
                if not field:
                    _tmp = __import__("wtforms", globals(), locals(), [_type], -1)
                    field = getattr(_tmp, _type)
                field = field(_name)
                setattr(cls, _slug, field)
        return super(DynamicSurveyFormMeta, cls).__call__(*args, **kwargs)

class DynamicSurveyForm(Form):
    """Create a Flask-WTF form based on settings saved in MongoDB."""
    __metaclass__ = DynamicSurveyFormMeta
