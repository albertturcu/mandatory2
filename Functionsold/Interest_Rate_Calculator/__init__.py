import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(status_code=404)
    else:
        amount = req_body.get('Amount')
        interest_rate = 0.20
        amount_with_interest = float(amount) + float(amount) * interest_rate
        return func.HttpResponse(status_code=200, body=json.dumps({"amount_with_interest": amount_with_interest}))
