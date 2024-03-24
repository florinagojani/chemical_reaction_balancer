# views.py
from django.shortcuts import render
from utils.openai_client import OpenAIClient
from django.http import HttpResponseServerError
from chempy import Substance


class InvalidReactionError(Exception):
    pass

def validate_reaction(reaction):
    if '0' in reaction:
        raise InvalidReactionError("Unexpected character ('0'). Did you mean 'O' instead?")

    reactants, products = map(str.strip, reaction.split('='))

    reactant_set = set(reactants.split(" + "))
    product_set = set(products.split(" + "))
    
    if any(compound in reactant_set for compound in product_set):
        raise InvalidReactionError("The same compound or substance cannot appear on both sides of the equation.")

    for side in [reactants, products]:
        for compound in side.split(" + "):
            try:
                Substance.from_formula(compound)
            except ValueError:
                raise InvalidReactionError(f"Invalid compound or substance: {compound}")

def reaction_balancer(request):
    balanced_reaction = None 

    if request.method == 'POST':
        reaction = request.POST.get('reaction', '')

        try:
            validate_reaction(reaction)
            
            openai_client = OpenAIClient()
            balanced_reaction = openai_client.balance_reaction(reaction)

        except InvalidReactionError as e:
            return render(request, 'custom_error_page.html', {'error_message': str(e)})

        except Exception as e:
            return HttpResponseServerError("Internal Server Error")

    return render(request, 'balancer_template.html', {'balanced_reaction': balanced_reaction})
