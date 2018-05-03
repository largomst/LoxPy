types = [
    "Binary   : Expr left, Token operator, Expr right",
    "Grouping : Expr expression",
    "Literal  : Object value",
    "Unary    : Token operator, Expr right"
]
typesDict = {}
for item in types:
    typeName, fieldsText = item.split(':')
    typeName, fieldsText = typeName.strip(), fieldsText.strip()
    fields = fieldsText.split(',')
    fields = [field.strip() for field in fields]
    fieldsDict = {}
    for field in fields:
        v, k = field.split(' ')
        k, v = k.strip(), v.strip()
        fieldsDict[k] = v
    typesDict[typeName] = fieldsDict

baseName = 'Expr'

from jinja2 import Template

template = Template("""
class {{baseName}}Visitor:
{% for typeName,fields in typesDict.items() %}
    def visit{{typeName}}(self, {{baseName|lower}}): raise NotImplementedError
{% endfor %}


class {{baseName}}:
    def accept(self, visitor: {{baseName}}Visitor)： raise NotImplementedError
    
{% for typeName, fields in typesDict.items() %}
class {{typeName}}({{baseName}}):
    
    def __init__(self{% for k,v in fields.items() %}, {{k}}: {{v}}{%endfor%}):
{% for k,v in fields.items() %}        self.{{k}} = {{k}}
{%endfor%}
        
    def accept(self, visitor: {{baseName}}Visitor):
        return visitor.visit{{typeName}}(self)

{% endfor %}
""")
print(template.render(baseName=baseName, typesDict=typesDict))
