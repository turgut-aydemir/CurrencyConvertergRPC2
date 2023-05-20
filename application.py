from concurrent import futures
import grpc
import currency_converter_pb2
import currency_converter_pb2_grpc
from forex_python.converter import CurrencyRates

class CurrencyConverterServicer(currency_converter_pb2_grpc.CurrencyConverterServicer):
    def ConvertCurrency(self, request, context):
        amount = request.amount
        from_currency = request.from_currency
        to_currency = request.to_currency
        c = CurrencyRates()
        rate = c.get_rate(from_currency, to_currency)
        result = amount * rate
        return currency_converter_pb2.CurrencyConversionResponse(result=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    currency_converter_pb2_grpc.add_CurrencyConverterServicer_to_server(CurrencyConverterServicer(), server)
    server.add_insecure_port('[::]:8282')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
