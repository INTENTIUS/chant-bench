# Find my EC2 instances that are in a public subnet.

`find-ec-instances-in-public-subn` · the answer aws-bench grades against: **5**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

3 commands, from `chant-b1`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-east-1 attr:internetFacing=true" --at latest --env floci --explain --show VpcId,PrivateIpAddress,SubnetId
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-west-1 attr:internetFacing=true" --at latest --env floci --explain --show VpcId,PrivateIpAddress,SubnetId
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-west-2 attr:internetFacing=true" --at latest --env floci --explain --show VpcId,PrivateIpAddress,SubnetId
```

## Terraform — answered

7 commands, from `terraform-m2`.

```sh
cd /workspace/terraform && ./terraform show -json 2>/dev/null | head -c 100000
cd /workspace/terraform && ./terraform show -json 2>/dev/null | jq '.values.root_module.child_modules[] | .resources[] | select(.type=="aws_instance") | {address, region: .values.region, instance_id: .values.id, subnet_id: .values.subnet_id, availability_zone: .values.availability_zone, public_ip: .values.public_ip, private_ip: .values.private_ip, tags: .values.tags}' 2>/dev/null
cd /workspace/terraform && ./terraform show -json 2>/dev/null | jq '.values.root_module.child_modules[] | .resources[] | select(.type=="aws_subnet") | {address, region: .values.region, subnet_id: .values.id, cidr_block: .values.cidr_block, vpc_id: .values.vpc_id, availability_zone: .values.availability_zone, map_public_ip_on_launch: .values.map_public_ip_on_launch}' 2>/dev/null
cd /workspace/terraform && ./terraform show -json 2>/dev/null | jq '.values.root_module.child_modules[] | .resources[] | select(.type=="aws_route_table") | {address, region: .values.region, route_table_id: .values.id, vpc_id: .values.vpc_id, routes: .values.route}' 2>/dev/null
cd /workspace/terraform && ./terraform show -json 2>/dev/null | jq '.values.root_module.child_modules[] | .resources[] | select(.type=="aws_route") | {address, region: .values.region, route_table_id: .values.route_table_id, destination_cidr: .values.destination_cidr_block, gateway_id: .values.gateway_id}' 2>/dev/null
cd /workspace/terraform && ./terraform show -json 2>/dev/null | jq '.values.root_module.child_modules[] | .resources[] | select(.type=="aws_route_table_association") | {address, region: .values.region, route_table_id: .values.route_table_id, subnet_id: .values.subnet_id}' 2>/dev/null
cd /workspace/terraform && ./terraform show -json 2>/dev/null | jq '.values.root_module.child_modules[] | .resources[] | select(.type=="aws_subnets" or .type=="aws_vpc") | {address, type: .type, region: .values.region, ids: .values.ids, vpc_id: .values.id}' 2>/dev/null
```

## Pulumi — answered

10 commands, from `pulumi-m2`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, region: .outputs.availabilityZone, subnetId: .outputs.subnetId, instanceId: .outputs.id}' | head -100
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {subnetId: .outputs.id, vpcId: .outputs.vpcId, arn: .arn}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/routeTable:RouteTable") | {routeTableId: .outputs.id, vpcId: .outputs.vpcId, routes: .outputs.routes}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/routeTableAssociation:RouteTableAssociation") | {subnetId: .outputs.subnetId, routeTableId: .outputs.routeTableId}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/route:Route") | {routeTableId: .outputs.routeTableId, destinationCidrBlock: .outputs.destinationCidrBlock, gatewayId: .outputs.gatewayId, transitGatewayId: .outputs.transitGatewayId, natGatewayId: .outputs.natGatewayId}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | { name: (.urn | split("::")[3]), instanceId: .outputs.id, region: .outputs.availabilityZone, subnetId: .outputs.subnetId } | select(.region | startswith("us-east-1") or startswith("us-west-1") or startswith("us-west-2"))'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/routeTableAssociation:RouteTableAssociation" or .type == "aws:ec2/mainRouteTableAssociation:MainRouteTableAssociation") | { subnetId: .outputs.subnetId, routeTableId: .outputs.routeTableId, type: .type }'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.subnetId == "subnet-default-c" or .subnetId == "subnet-c8d665c6" or (.type == "aws:ec2/subnet:Subnet" and (.outputs.id == "subnet-default-c" or .outputs.id == "subnet-c8d665c6")))'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet" and .outputs.id == "subnet-default-c")'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance" and .outputs.id == "i-f716c50fc0536b860")'
```

## AWS CDK — answered

23 commands, from `cdk-cur`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | keys'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet") | {logicalId: .key, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::RouteTable" or .value.Type == "AWS::EC2::Route") | {logicalId: .key, type: .value.Type, properties: .value.Properties}' | head -50
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::SubnetRouteTableAssociation") | {logicalId: .key, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, subnet: .value.Properties.SubnetId}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance" or .value.Type == "AWS::EC2::Subnet") | {logicalId: .key, type: .value.Type, subnet: .value.Properties.SubnetId, subnetTags: .value.Properties.Tags}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance" or .value.Type == "AWS::EC2::Subnet") | {logicalId: .key, type: .value.Type, subnet: .value.Properties.SubnetId, subnetTags: .value.Properties.Tags}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {logicalId: .LogicalResourceId, physicalId: .PhysicalResourceId, subnet: .Metadata.SubnetId}'
aws ec2 describe-instances --instance-ids i-99224a9cff337e5b0 i-5fdf2028dd5a7a28d i-f5d8c3aa998285b73 i-754790856a4ef8150 --region us-east-1 2>/dev/null | jq '.Reservations[].Instances[] | {instanceId: .InstanceId, subnetId: .SubnetId, vpcId: .VpcId, tags: .Tags}'
aws ec2 describe-subnets --subnet-ids subnet-default-a subnet-ed687450 subnet-71ad586d --region us-east-1 2>/dev/null | jq '.Subnets[] | {subnetId: .SubnetId, cidr: .CidrBlock, mapPublicIp: .MapPublicIpOnLaunch, tags: .Tags}'
# … 11 more
```
