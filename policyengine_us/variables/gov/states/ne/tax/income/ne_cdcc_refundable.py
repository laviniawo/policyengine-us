from policyengine_us.model_api import *


class ne_cdcc_refundable(Variable):
    value_type = float
    entity = TaxUnit
    label = "NE refundable cdcc"
    unit = USD
    definition_period = YEAR
    reference = (
        "https://revenue.nebraska.gov/files/doc/tax-forms/2021/f_2441n.pdf"
        "https://revenue.nebraska.gov/sites/revenue.nebraska.gov/files/doc/Form_2441N_Ne_Child_and_Dependent_Care_Expenses_8-618-2022_final_2.pdf"
    )
    defined_for = StateCode.NE

    def formula(tax_unit, period, parameters):
        p = parameters(period).gov.states.ne.tax.income.credits.cdcc.refundable
        # determine AGI eligibility
        us_agi = tax_unit("adjusted_gross_income", period)
        max_match_percentage = p.match
        reduction_start = p.reduction.start
        increment = p.reduction.increment
        reduction_per_increment = p.reduction.amount
        excess = max_(us_agi - reduction_start, 0)
        increments = np.ceil(excess / increment)
        total_match_reduction_amount = increments * reduction_per_increment
        match = max_(max_match_percentage - total_match_reduction_amount, 0)
        # determine NE refundable cdcc amount
        us_cdcc = tax_unit("cdcc", period)
        # The refundable credit is limited to filers
        # with income below a certain threshold which is not mathematically
        # derived from the reduction structure
        income_eligible = us_agi < p.income_threshold
        return us_cdcc * match * income_eligible
