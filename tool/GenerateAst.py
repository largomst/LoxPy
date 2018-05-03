import sys
from typing import List
from jinja2 import Template


def main():
    if len(sys.argv) != 2:
        print(sys.argv)
        print('Usage: generate_ast <output directory>')
        sys.exit(1)
    outputDir = sys.argv[1]

    defineAst(outputDir, "Expr", [
        "Binary   : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "Literal  : Object value",
        "Unary    : Token operator, Expr right"
    ])


def defineAst(outputDir: str, baseName: str, types: List[str]):
    path = f'{outputDir}/{baseName}.py'
    typesDict = {}
    # REVIEW: 这相当与建立符号表 def 阶段
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
    template = Template("""from lox import Token

__all__ = [
    "{{baseName}}Visitor",
    "{{baseName}}",{% for typeName, fields in typesDict.items() %}
    "{{typeName}}",{% endfor %}
]


class {{baseName}}:
    def accept(self, visitor: {{baseName}}Visitor): raise NotImplementedError


class {{baseName}}Visitor:{% for typeName,fields in typesDict.items() %}
    def visit{{typeName}}(self, {{baseName|lower}}: "{{typeName}}"): raise NotImplementedError
{% endfor %}

{# 这相当于建立符号表的 ref 阶段 #}
{% for typeName, fields in typesDict.items() %}
class {{typeName}}({{baseName}}):

    def __init__(self{% for k,v in fields.items() %}, {{k}}: {{v}}{%endfor%}):{% for k,v in fields.items() %}
        self.{{k}} = {{k}}{%endfor%}

    def accept(self, visitor: {{baseName}}Visitor):
        return visitor.visit{{typeName}}(self)

{% endfor %}
    """)

    context = template.render(baseName=baseName, typesDict=typesDict)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(context)


if __name__ == '__main__':
    main()
