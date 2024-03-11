from aws_cdk import core, aws_ec2 as ec2, aws_rds as rds

from aws_cdk.core import Stack, Construct
from aws_cdk import aws_ec2 as ec2, aws_rds as rds

class ServerStack(Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Security Group for Web Servers
        sg_web = ec2.SecurityGroup(self, "WebSG", vpc=vpc, allow_all_outbound=True)
        sg_web.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80))

        # Security Group for RDS
        sg_rds = ec2.SecurityGroup(self, "RDSSG", vpc=vpc, allow_all_outbound=True)
        sg_rds.add_ingress_rule(sg_web, ec2.Port.tcp(3306))

        # Launch web servers
        for i in range(2):  # Assuming 2 public subnets
            ec2.Instance(self, f"WebServer{i}",
                         instance_type=ec2.InstanceType("t3.micro"),
                         machine_image=ec2.MachineImage.latest_amazon_linux(),
                         vpc=vpc,
                         vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                         security_group=sg_web)

        # RDS MySQL instance
        rds.DatabaseInstance(self, "MyRDS",
                             engine=rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0_21),
                             instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
                             vpc=vpc,
                             vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
                             security_groups=[sg_rds])

        
        web_server_sg = ec2.SecurityGroup.from_security_group_id(
            self, "WebServerSG", security_group_id=cdk_lab_web_instance.security_group.security_group_id
        )
        web_server_sg.add_egress_rule(
            peer=rds_instance.connections.security_groups[0],  # Assuming RDS instance's first security group
            connection=ec2.Port.tcp(3306),
            description="Allow web servers to connect to RDS on port 3306"
        )  
