from __future__ import annotations

from sys import version_info
from typing import TYPE_CHECKING


from google.cloud import network_management_v1

if TYPE_CHECKING:
    from rich.console import Console


if version_info < (3, 10):  # pragma: nocover
    from dma.utils import anext_ as anext  # noqa: A001

async def create_test(
    console: Console,
    client: network_management_v1.ReachabilityServiceAsyncClient,
    test_id: str,
    gcp_project: str,
    target_db_ip: str,
    source_db_ip: str,
    source_db_port: int,
    ) -> network_management_v1.types.connectivity_test.ConnectivityTest:
    # Initialize request argument(s)
    resource = network_management_v1.ConnectivityTest()
    resource.name = f"projects/{gcp_project}/locations/global/connectivityTests/{test_id}"
    # During migration, connectivity is setup from target DB to source DB.
    resource.source.ip_address = target_db_ip
    resource.destination.ip_address = source_db_ip
    resource.destination.port = source_db_port
    resource.protocol = "TCP"

    request = network_management_v1.CreateConnectivityTestRequest(
        parent=f"projects/{gcp_project}/locations/global",
        test_id=test_id,
        resource=resource,
    )

    # Make the request
    operation = await client.create_connectivity_test(request=request)

    print("Waiting for operation to complete...")

    return await operation.result()

async def rerun_test(
    console: Console,
    client: network_management_v1.ReachabilityServiceAsyncClient,
    test_id: str,
    gcp_project: str,
    ) -> network_management_v1.types.connectivity_test.ConnectivityTest:

    # Initialize request argument(s)
    request = network_management_v1.RerunConnectivityTestRequest(
        name= f"projects/{gcp_project}/locations/global/connectivityTests/{test_id}",
    )

    # Make the request
    operation = await client.rerun_connectivity_test(request=request)

    print("Waiting for operation to complete...")
    return await operation.result()

async def delete_test(
    console: Console,
    client: network_management_v1.ReachabilityServiceAsyncClient,
    test_id: str,
    gcp_project: str,
    ) -> network_management_v1.types.connectivity_test.ConnectivityTest:

    # Initialize request argument(s)
    request = network_management_v1.DeleteConnectivityTestRequest(
        name= f"projects/{gcp_project}/locations/global/connectivityTests/{test_id}",
    )
    # Make the request
    operation = await client.delete_connectivity_test(request=request)

    print("Waiting for operation to complete...")
    return await operation.result()

async def connectivity_check(
    console: Console,
    operation_type: str,
    test_id: str,
    gcp_project: str,
    target_db_ip: str,
    source_db_ip: str,
    source_db_port: int,
) -> None:
    """Check the connectivity from target instance to source instance"""
    # Create a client
    client = network_management_v1.ReachabilityServiceAsyncClient()

    if operation_type == "create":
        response = await create_test(console, client, test_id, gcp_project, target_db_ip, source_db_ip, source_db_port)
    elif operation_type == "rerun":
        response = await rerun_test(console, client, test_id, gcp_project)
    elif operation_type == "delete":
        response = await delete_test(console, client, test_id, gcp_project)
    else:
        console.print("Invalid operation type")
        return
    # Handle the response
    console.print(response)
    
