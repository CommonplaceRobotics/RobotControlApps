from dataclasses import dataclass, field

import robotcontrolapp_pb2


@dataclass
class DirectoryContent:
    """Description of a directory's content"""

    success: bool = False
    errorMessage: str = ""
    entries: list = field(
        default_factory=list[robotcontrolapp_pb2.ListFilesResponse.DirectoryEntry]
    )


def DirectoryContentFromGrcp(
    grpc: robotcontrolapp_pb2.ListFilesResponse,
) -> DirectoryContent:
    """
    Creates an object from a GRPC ListFilesResponse
    Returns:
        A new DirectoryContent object
    """
    self = DirectoryContent()
    self.success = grpc.success
    self.errorMessage = grpc.error
    self.entries.extend(grpc.entries)
    return self
