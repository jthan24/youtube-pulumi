from pulumi import Config, Output, export
from pulumi_gcp import compute

config = Config()
values = config.require_object("values")
proyecto = values.get("proyecto")


#
# network and firewall for both virtual machines
#
network = compute.Network("devops-network"+proyecto, auto_create_subnetworks=False)

## Creacion de las subnets
subnet_1 = compute.Subnetwork("devops-subnet-1",
    ip_cidr_range=values.get("subnet_address_prefixes")[0],
    region="us-central1",
    network=network.id,
    )

subnet_2 = compute.Subnetwork("devops-subnet-2",
    ip_cidr_range=values.get("subnet_address_prefixes")[1],
    region="us-central1",
    network=network.id,
    )


## Reglas del Firewall
firewall = compute.Firewall(
    "devops-firewall",
    network=network.name,
    allows=[
        compute.FirewallAllowArgs(
            protocol="tcp",
            ports=["22"]
        ),
    ],
    source_tags=["web"]
)


## Direccion IP para la instancia
instance_addr = compute.address.Address("devops-address-"+proyecto, 
    region="us-central1")


## Aprovisionando la instanci
instance = compute.Instance(
    "devops-instance"+proyecto,
    machine_type="f1-micro",
    boot_disk=compute.InstanceBootDiskArgs(
        initialize_params=compute.InstanceBootDiskInitializeParamsArgs(
            image="ubuntu-os-cloud/ubuntu-1804-bionic-v20200414"
        ),
    ),
    network_interfaces=[
        compute.InstanceNetworkInterfaceArgs(
            network=network.id,
            access_configs=[compute.InstanceNetworkInterfaceAccessConfigArgs(
                nat_ip=instance_addr.address
            )],
            subnetwork=subnet_1.name
        )
    ],
    zone="us-central1-a",
)


export("instance_name", instance.name)
export("instance_external_ip", instance_addr.address)