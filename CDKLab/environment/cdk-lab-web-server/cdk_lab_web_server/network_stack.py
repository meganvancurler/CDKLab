from aws_cdk import core, aws_ec2 as ec2

class NetworkStack(Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc(self, "MyVPC",
                      max_azs=2,
                      subnet_configuration=[
                          ec2.SubnetConfiguration(name="PublicSubnet", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
                          ec2.SubnetConfiguration(name="PrivateSubnet", subnet_type=ec2.SubnetType.PRIVATE, cidr_mask=24)
                      ])

        self.vpc = vpc
