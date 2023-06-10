import grpc
from concurrent import futures
import threading

from flask import Flask

import currency_converter_pb2
import currency_converter_pb2_grpc
from forex_python.converter import CurrencyRates

app = Flask(__name__)


@app.route('/')
def func():
    return "Currency Converter Server by Turgut Aydemir"


class CurrencyConverterServicer(currency_converter_pb2_grpc.CurrencyConverterServicer):
    def ConvertCurrency(self, request, context):
        amount = request.amount
        from_currency = request.from_currency
        to_currency = request.to_currency

        c = CurrencyRates()
        try:
            result = c.convert(from_currency, to_currency, amount)
        except:
            result = 1000
        return currency_converter_pb2.CurrencyConversionResponse(result=result)


def run_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    currency_converter_pb2_grpc.add_CurrencyConverterServicer_to_server(CurrencyConverterServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC Server started. Listening on port 50051.")
    server.wait_for_termination()


if __name__ == '__main__':
    grpc_server_thread = threading.Thread(target=run_grpc_server)
    grpc_server_thread.start()
    app.run(host="0.0.0.0", port=8000)
