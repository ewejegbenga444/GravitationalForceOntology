import tkinter as tk
from tkinter import messagebox
from owlready2 import *
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_gravitational_force_problem(request):
    # Response structure
    response = {
        "masses": [],
        "distance": "",
        "gravitational_constant": "",
        "steps": [],
        "hints": [],
        "force": "",
    }

    # Load the ontology
    ontology_path = "api/PhysicsGravitationalforce.owx"  # Adjust the path to your file location
    onto = get_ontology(ontology_path).load()

    # Fetch the problem instance
    problem = onto.search_one(iri="*Problem1")
    print(problem.hasMass[1].value)

    if not problem:
        return Response({"error": "Problem1 not found in the ontology"}, status=404)

    # Extract masses
    if hasattr(problem, 'hasMass'):
        for mass in problem.hasMass:
            mass_value = mass.value[0] if hasattr(mass, 'value') else "N/A"
            response['masses'].append(mass_value)

    # Extract distance
    if hasattr(problem, 'hasDistance'):
        distance = problem.hasDistance[0]
        response['distance'] = distance.value[0] if hasattr(distance, 'value') else "N/A"

    # Extract gravitational constant
    if hasattr(problem, 'hasGravitationalConstant'):
        g_constant = problem.hasGravitationalConstant[0]
        response['gravitational_constant'] = g_constant.value[0] if hasattr(g_constant, 'value') else "N/A"

    # Extract steps, hints, and feedback
    if hasattr(problem, 'hasStep'):
        for step in problem.hasStep:
            step_desc = step.description[0] if hasattr(step, 'description') else "N/A"
            response['steps'].append(step_desc)

            if hasattr(step, 'hasHint'):
                hint = step.hasHint[0]
                hint_text = hint.text[0] if hasattr(hint, 'text') else "N/A"
                response['hints'].append(hint_text)

    # Extract the force value
    if hasattr(problem, 'hasForce'):
        force = problem.hasForce[0]
        response['force'] = force.value[0] if hasattr(force, 'value') else "N/A"

    # Return the JSON response
    return Response(response)