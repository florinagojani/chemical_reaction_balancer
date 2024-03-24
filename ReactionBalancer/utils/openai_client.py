# utils/openai_client.py
import chempy

class OpenAIClient:
    def balance_reaction(self, reaction):
        if '->' in reaction:
            reactants, products = reaction.split('->')
        elif '=' in reaction:
            reactants, products = reaction.split('=')
        else:
            return "Invalid reaction format. Please use '->' or '=' to separate reactants from products."
        
        reactants = [r.strip() for r in reactants.split('+')]
        products = [p.strip() for p in products.split('+')]
        
        balanced_reaction = chempy.balance_stoichiometry(reactants, products)
        
        balanced_equation = ''
        for reactant, coefficient in balanced_reaction[0].items():
            if coefficient != 1:
                balanced_equation += f"{coefficient} "
            balanced_equation += f"{reactant} + "
        balanced_equation = balanced_equation[:-3]  
        balanced_equation += ' -> '
        for product, coefficient in balanced_reaction[1].items():
            if coefficient != 1:
                balanced_equation += f"{coefficient} "
            balanced_equation += f"{product} + "
        balanced_equation = balanced_equation[:-3]  
        
        return balanced_equation

