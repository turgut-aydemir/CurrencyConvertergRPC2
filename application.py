from concurrent import futures
import grpc
import currency_converter_pb2
import currency_converter_pb2_grpc
from forex_python.converter import CurrencyRates
from flask import Flask

app = Flask(__name__)

@app.route('/')
def func():
    return "Currency Converter Server, serving with HTTP/1.1"


class CurrencyConverterServicer(currency_converter_pb2_grpc.CurrencyConverterServicer):
    def ConvertCurrency(self, request, context):
        amount = request.amount
        from_currency = request.from_currency
        to_currency = request.to_currency
        c = CurrencyRates()
        result = c.convert(from_currency, to_currency, amount)

        return currency_converter_pb2.CurrencyConversionResponse(result=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    currency_converter_pb2_grpc.add_CurrencyConverterServicer_to_server(CurrencyConverterServicer(), server)
    p = server.add_insecure_port('0.0.0.0:8282')
    server.start()
    return server


if __name__ == '__main__':
    serve()
    app.run(host='0.0.0.0', port=8000)