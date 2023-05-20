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
        conversion_rate = c.get_rate(from_currency, to_currency)
        result = amount * conversion_rate

        return currency_converter_pb2.CurrencyConversionResponse(result=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    currency_converter_pb2_grpc.add_CurrencyConverterServicer_to_server(CurrencyConverterServicer(), server)
    app.logger.error("Adding insecure port 8282")
    p = server.add_insecure_port('0.0.0.0:8282')
    app.logger.error("Opened up on port ")
    app.logger.error(p)
    server.start()
    return server


if __name__ == '__main__':
    app.logger.error("Hello! Starting up")
    grpc_server = serve()
    app.logger.error("Serving gRPC!")
    app.run(host="0.0.0.0", port=8000)
