from unified_planning.io import PDDLReader, PDDLWriter
from unified_planning.io.pddl_writer import  ObjectsExtractor
from unified_planning.model.operators import OperatorKind

import sys
import json

reader = PDDLReader()

domain_filename = sys.argv[1]
problem_filename = sys.argv[2]


problem = reader.parse_problem(domain_filename, problem_filename)
writer = PDDLWriter(problem)


types = []

user_types_hierarchy = problem.user_types_hierarchy
stack: list["unified_planning.model.Type"] = (
    user_types_hierarchy[None] if None in user_types_hierarchy else []
)

for t in stack:
    types.append({
        'name': t.name,
        'parent': 'object'
    })

while stack:
    current_type = stack.pop()
    direct_sons: list["unified_planning.model.Type"] = user_types_hierarchy[
        current_type
    ]
    if direct_sons:
        stack.extend(direct_sons)
        for t in stack:
            types.append({
                'name': t.name,
                'parent': current_type.name,
            })


predicates = []

for f in problem._fluents:

    predicates.append({
        'name': f.name,
        'negated': False,
        'parameters': [{'name': '?' + p.name, 'type': p.type.name} for p in f._signature]
    })


writer._populate_domain_objects(ObjectsExtractor())
domain_objects = writer.domain_objects

constants = []
constants_names = []

for ut, os in domain_objects.items():
    for c in os:
        constants_names.append(c.name)
        constants.append({
            'name': c.name,
            'type': ut.name
        })

# print(constants)


objects = []

for o in problem._objects:

    if o.name not in constants_names:

        objects.append({
            'name': o.name,
            'type': o.type.name
        })



actions = []

for a in problem.actions:

    # print(a.name)

    na = {
        'name': a.name,
        'parameters': [],
        'precondition': [],
        'effect': []
    }

    parameters_name  = []
    for ap in a.parameters:
        parameters_name.append(ap.name)
        na['parameters'].append({
            'name': '?' + ap.name,
            'type': ap.type.name
        })

    for precondition in a.preconditions:
        if not precondition.is_true():
            if precondition.is_and():
                for c in precondition._content.args:
                    if c.node_type == OperatorKind.NOT:
                        not_c = c.args[0]
                        # print(not_c._content.args[0]._content.payload.type)
                        na['precondition'].append({
                            'name': '='  if not_c._content.node_type == OperatorKind.EQUALS else not_c._content.payload.name,
                            'negated': True,
                            # 'arguments': [{'name': par._content.payload.name, 'type': par._content.payload.type.name} for par in not_c._content.args],
                            'arguments': [('?' if par._content.payload.name in parameters_name else '') + par._content.payload.name for par in not_c._content.args]
                        })
                    else:
                        # print(c._content)
                        # print(c._content.payload)
                        na['precondition'].append({
                            'name': c._content.payload.name,
                            'negated': False,
                            # 'arguments': [{'name': arg._content.payload.name, 'type':  arg.type.name} for arg in c._content.args]
                            'arguments': [('?' if arg._content.payload.name in parameters_name else '') + arg._content.payload.name for arg in c._content.args]
                        })
            else:
                # print(precondition)
                c = precondition
                if c.node_type == OperatorKind.NOT:
                        not_c = c.args[0]
                        # print(not_c._content.args[0]._content.payload.type)
                        na['precondition'].append({
                            'name': '='  if not_c._content.node_type == OperatorKind.EQUALS else not_c._content.payload.name,
                            'negated': True,
                            # 'arguments': [{'name': par._content.payload.name, 'type': par._content.payload.type.name} for par in not_c._content.args],
                            'arguments': [('?' if par._content.payload.name in parameters_name else '') + par._content.payload.name for par in not_c._content.args]
                        })
                else:
                    # print(c._content)
                    # print(c._content.payload)
                    na['precondition'].append({
                        'name': c._content.payload.name,
                        'negated': False,
                        # 'arguments': [{'name': arg._content.payload.name, 'type':  arg.type.name} for arg in c._content.args]
                        'arguments': [('?' if arg._content.payload.name in parameters_name else '') + arg._content.payload.name for arg in c._content.args]
                    })

    # print(na['precondition'])

    for effect in a.effects:
        c = effect.fluent._content
        # print(c.args[0]._content.payload)
        na['effect'].append({
            'name': c.payload.name,
            'negated': effect.value._content.payload == False,
            # 'arguments': [{'name': arg._content.payload.name, 'type': arg.type.name} for arg in c.args]
            'arguments': [('?' if arg._content.payload.name in parameters_name else '') + arg._content.payload.name for arg in c.args]
        })


    actions.append(na)


# print(json.dumps(actions, indent=1))

initial = []

for f, v in problem.initial_values.items():
    if v.is_true():
        # print(f._content)
        initial.append({
            'name': f._content.payload.name,
            'negated': False,
            # 'arguments': [{'name': arg._content.payload.name, 'type': arg.type.name} for arg in f._content.args]
            'arguments': [ arg._content.payload.name for arg in f._content.args]
        })



goal = []

for g in problem.goals:
    for c in g._content.args:
        if c.node_type == OperatorKind.NOT:
            not_c = c.args[0]
            # print(not_c._content.args[0]._content.payload.type)
            goal.append({
                'name': '='  if not_c._content.node_type == OperatorKind.EQUALS else not_c._content.payload.name,
                'negated': True,
                # 'arguments': [{'name': par._content.payload.name, 'type': par._content.payload.type.name} for par in not_c._content.args]
                'arguments': [par._content.payload.name for par in not_c._content.args]
            })
        else:
            # print(c._content)
            # print(c._content.payload)
            goal.append({
                'name': c._content.payload.name,
                'negated': False,
                # 'arguments': [{'name': arg._content.payload.name, 'type':  arg.type.name} for arg in c._content.args],
                'arguments': [arg._content.payload.name for arg in c._content.args]
            })


model = {
    'constants': constants,
    'objects': objects,
    'initial': initial,
    'goal': goal,
    'types': types,
    'predicates': predicates,
    'actions': actions
}


print(json.dumps(model, indent=1))