"""An Azure RM Python Pulumi program"""

from pulumi import Config, Output, export

from pulumi_azure_native import resources
from pulumi_azure_native import compute
from pulumi_azure_native import network

config = Config()
values = config.require_object("values")
proyecto = values.get("proyecto")
tags = values.get("tags")


# Create an Azure Resource Group
resource_group = resources.ResourceGroup('devops-resources-'+ proyecto)

net = network.VirtualNetwork(
    "server-network",
    resource_group_name=resource_group.name,
    address_space=network.AddressSpaceArgs(
        address_prefixes=[values.get("address_prefixes")],
    ),
    subnets=[network.SubnetArgs(
        name="devops-subnet-"+proyecto+"0",
        address_prefix=values.get("subnet_address_prefixes")[0],
    ),
    network.SubnetArgs(
        name="devops-subnet-"+proyecto+"1",
        address_prefix=values.get("subnet_address_prefixes")[1],
    )
    ])

public_ip = network.PublicIPAddress(
    "devops-pip"+proyecto,
    resource_group_name=resource_group.name,
    public_ip_allocation_method=network.IPAllocationMethod.DYNAMIC)

network_iface = network.NetworkInterface(
    "devops-nic"+proyecto,
    resource_group_name=resource_group.name,
    ip_configurations=[network.NetworkInterfaceIPConfigurationArgs(
        name="webserveripcfg",
        subnet=network.SubnetArgs(id=net.subnets[0].id),
        private_ip_allocation_method=network.IPAllocationMethod.DYNAMIC,
        public_ip_address=network.PublicIPAddressArgs(id=public_ip.id),
    )])


vm = compute.VirtualMachine(
    "devops-vm"+proyecto,
    resource_group_name=resource_group.name,
    network_profile=compute.NetworkProfileArgs(
        network_interfaces=[
            compute.NetworkInterfaceReferenceArgs(id=network_iface.id),
        ],
    ),
    hardware_profile=compute.HardwareProfileArgs(
        vm_size="Standard_F2",
    ),
    os_profile=compute.OSProfileArgs(
        computer_name="devops-hostname",
        admin_username="adminuser",
        linux_configuration=compute.LinuxConfigurationArgs(
            disable_password_authentication=True,
            ssh=compute.SshConfigurationArgs(
                public_keys=[compute.SshPublicKeyArgs(
                    key_data="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDKGoQF7+n8hJiLE2TXXd7+tUXTEPpIaR6DGh6sXrVGW5jepP28fCP5PZzpxAeJvLQ0n8w7O5Q9zMpenytbILP4fTDa7bQKOkPnvn+D25we9mNW3ZoIbs33b0VQ03WLsnYKbpfc8wpuJDIW9wD1UcNk4GOTzJS7SnU98SWNPn0NfFlO5I3W7Z6iP0SxCKbChIarEKxezG9hOvl05RobCHs/CT2F73qWOdpGVBgWV3LmlAL/E8atI/U7+dFo1QGNUe5S6aXzsLjBZ5K9hjAJwUXXoxsM3OoiLaeYYpEOmaqbhAjDK56QmPKh4zDfPzzJZguChMGVdu+oWbldfkE02lnmMk24BMyAR79lWThlMVdJAX5OYT4q2aL79Pp6DagpR40MbtJD5u6n/xCpiMhEGBsfZ5r3RlkaV0Al11P62Dl+7oHiI93fiDY17DgI8GvQNv6xC1CYl+62Umfdt5Tc/B+e+tlQvPdwBVnA/Kx5TtcUIViyuHni9qG64rWu7Iy+VfU=",
                    path="/home/adminuser/.ssh/authorized_keys",
                )],
            ),
        ),
    ),
    storage_profile=compute.StorageProfileArgs(
        os_disk=compute.OSDiskArgs(
            create_option=compute.DiskCreateOptionTypes.FROM_IMAGE,
            name="myosdisk1",
        ),
        image_reference=compute.ImageReferenceArgs(
            publisher="canonical",
            offer="UbuntuServer",
            sku="16.04-LTS",
            version="latest",
        ),
    ),
    tags=tags
    )

public_ip_addr = vm.id.apply(lambda _: network.get_public_ip_address_output(
    public_ip_address_name=public_ip.name,
    resource_group_name=resource_group.name))

export("public_ip", public_ip_addr.ip_address)