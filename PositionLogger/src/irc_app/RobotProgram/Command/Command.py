from abc import ABC, abstractmethod

from irc_app.rpc import robotcontrolapp_pb2


class ICommand(ABC):
    @abstractmethod
    def GetCmdParameters(self) -> robotcontrolapp_pb2.AddCommandRequest.CmdParameters:
        """Gets the command parameters for AddCommandRequest"""
        return robotcontrolapp_pb2.AddCommandRequest.CmdParameters()
