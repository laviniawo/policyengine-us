from openfisca_us.model_api import *

class il_k12_education_expense_credit(Variable):
    value_type = float
    entity = TaxUnit
    label = "IL K-12 Education Expense Credit"
    unit = USD
    definition_period = YEAR
    reference = ""

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.states.il.tax.income.credits.k12
        tuition_and_fees = tax_unit("k12_tuition_and_fees", period)
        reduced_tuition_and_fees = max_(0, tuition_and_fees - p.reduction)
        max_credit = reduced_tuition_and_fees * p.rate
        return min_(max_credit, p.cap)