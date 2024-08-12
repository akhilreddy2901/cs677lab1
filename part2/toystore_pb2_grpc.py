# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import toystore_pb2 as toystore__pb2


class ToyStoreStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Query = channel.unary_unary(
                '/ToyStore/Query',
                request_serializer=toystore__pb2.ItemName.SerializeToString,
                response_deserializer=toystore__pb2.Item.FromString,
                )
        self.Buy = channel.unary_unary(
                '/ToyStore/Buy',
                request_serializer=toystore__pb2.ItemName.SerializeToString,
                response_deserializer=toystore__pb2.BuyResponse.FromString,
                )


class toy_store_server(object):
    """Missing associated documentation comment in .proto file."""

    def Query(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Buy(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_toy_store_server_to_server(servicer, server):
    rpc_method_handlers = {
            'Query': grpc.unary_unary_rpc_method_handler(
                    servicer.Query,
                    request_deserializer=toystore__pb2.ItemName.FromString,
                    response_serializer=toystore__pb2.Item.SerializeToString,
            ),
            'Buy': grpc.unary_unary_rpc_method_handler(
                    servicer.Buy,
                    request_deserializer=toystore__pb2.ItemName.FromString,
                    response_serializer=toystore__pb2.BuyResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ToyStore', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ToyStore(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Query(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ToyStore/Query',
            toystore__pb2.ItemName.SerializeToString,
            toystore__pb2.Item.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Buy(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ToyStore/Buy',
            toystore__pb2.ItemName.SerializeToString,
            toystore__pb2.BuyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
