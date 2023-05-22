import grpc
from concurrent import futures
import currency_converter_pb2
import currency_converter_pb2_grpc
from forex_python.converter import CurrencyRates


class CurrencyConverterServicer(currency_converter_pb2_grpc.CurrencyConverterServicer):
    def ConvertCurrency(self, request, context):
        amount = request.amount
        from_currency = request.from_currency
        to_currency = request.to_currency

        c = CurrencyRates()
        result = c.convert(from_currency, to_currency, amount)

        return currency_converter_pb2.CurrencyConversionResponse(result=result)


def serve():
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        currency_converter_pb2_grpc.add_CurrencyConverterServicer_to_server(CurrencyConverterServicer(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        print("Server started. Listening on port 50051.")
        server.wait_for_termination()
    except Exception as e:
        print("Error occurred: ", e)


if __name__ == '__main__':
    serve()
