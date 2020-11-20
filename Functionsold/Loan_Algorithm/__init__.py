import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(status_code=404)
    else:
        amount = req_body.get('Amount')
        loan = req_body.get('Loan')

        if loan/amount < 0.75:
            return func.HttpResponse(status_code=200, body=json.dumps({"isValidLoan": True}))
        else:
            return func.HttpResponse(status_code=403, body=json.dumps({"isValidLoan": False}))