# Find my EC2 instances that are in a public subnet.

`find-ec-instances-in-public-subn` · the answer aws-bench grades against: **5**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

3 commands, from `chant-i3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-east-1 attr:internetFacing=true" --at latest --env floci --explain
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-west-1 attr:internetFacing=true" --at latest --env floci --explain
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-west-2 attr:internetFacing=true" --at latest --env floci --explain
```

## No tool (AWS CLI) — answered

9 commands, from `bare-i3`.

```sh
# Get all subnets and route tables for us-east-1 to determine which are public echo "=== us-east-1: Subnets and Route Tables ===" aws ec2 describe-subnets --region us-east-1 --output json | jq -r '.Subnets[] | "\(.SubnetId) \(.AvailabilityZone)"' > /tmp/us-east-1-subnets.txt cat /tmp/us-east-1-subnets.txt echo "" echo "=== us-east-1: Route Tables ===" aws ec2 describe-route-tables --region us-east-1 --output json | jq '.RouteTables[] | select(.Routes[] | select(.GatewayId | startswith("igw-"))) | .Associations[].SubnetId' > /tmp/us-east-1-public-subnets.txt cat /tmp/us-east-1-public-subnets.txt
# Get EC2 instances in us-east-1 echo "=== us-east-1: Instances ===" aws ec2 describe-instances --region us-east-1 --output json | jq '.Reservations[] | .Instances[] | {InstanceId, SubnetId, InstanceType, State: .State.Name, PublicIp: .PublicIpAddress, PrivateIp: .PrivateIpAddress}'
# Check if subnet-default-c is public by checking its route table aws ec2 describe-route-tables --region us-east-1 --output json | jq '.RouteTables[] | select(.Associations[]? | .SubnetId == "subnet-default-c") | .Routes'
# Get route tables and check which have IGW routes aws ec2 describe-route-tables --region us-east-1 --output json | jq '.RouteTables[] | {TableId: .RouteTableId, Associations: [.Associations[].SubnetId | select(. != null)], HasIGW: (.Routes[] | select(.GatewayId | startswith("igw-")) | true)}'
# Get public subnets and instances for us-west-1 echo "=== us-west-1: Public Subnets ===" aws ec2 describe-route-tables --region us-west-1 --output json | jq '.RouteTables[] | select(.Routes[] | select(.GatewayId | startswith("igw-"))) | .Associations[].SubnetId' | sort -u echo "" echo "=== us-west-1: Instances ===" aws ec2 describe-instances --region us-west-1 --output json | jq '.Reservations[] | .Instances[] | {InstanceId, SubnetId, InstanceType, State: .State.Name, PublicIp: .PublicIpAddress, PrivateIp: .PrivateIpAddress}'
# Get public subnets and instances for us-west-2 echo "=== us-west-2: Public Subnets ===" aws ec2 describe-route-tables --region us-west-2 --output json | jq '.RouteTables[] | select(.Routes[] | select(.GatewayId | startswith("igw-"))) | .Associations[].SubnetId' | sort -u echo "" echo "=== us-west-2: Instances ===" aws ec2 describe-instances --region us-west-2 --output json | jq '.Reservations[] | .Instances[] | {InstanceId, SubnetId, InstanceType, State: .State.Name, PublicIp: .PublicIpAddress, PrivateIp: .PrivateIpAddress}'
# Check route tables more carefully for each region to identify all public subnets for region in us-east-1 us-west-1 us-west-2; do echo "=== $region: Route Tables ===" aws ec2 describe-route-tables --region $region --output json | jq '.RouteTables[] | {TableId: .RouteTableId, Associations: [.Associations[].SubnetId | select(. != null)], IsDefault: .Associations[0].Main, HasIGW: (if (.Routes[] | select(.GatewayId | startswith("igw-"))) then true else false end)}' echo "" done
# Get all subnets and identify their route tables for region in us-east-1 us-west-1 us-west-2; do echo "=== $region: All Subnets ===" aws ec2 describe-subnets --region $region --output json | jq '.Subnets[] | {SubnetId, VpcId, AvailabilityZone}' echo "" done
# Compile the final result cat > /logs/agent/agent-output.txt << 'EOF' EC2 INSTANCES IN PUBLIC SUBNETS ================================ A subnet is considered PUBLIC if it has a route to an Internet Gateway (IGW) in its route table. SUMMARY ======= Total instances in public subnets: 4 us-east-1 (3 instances) us-west-1 (1 instance) us-west-2 (1 instance) DETAILED RESULTS ================ us-east-1: ---------- 1. Instance ID: i-5c8da84c9f36669a2 Subnet ID: subnet-11443658 Availability Zone: us-east-1a Instance Type: t3.micro State: running Public IP: 54.144.246.78 Private IP: 10.0.0.11 VPC ID: vpc-9db1ce60 2. Instance ID: i-428719f07db4ec1d6 Subnet ID: subnet-11443658 Availability Zone: us-east-1a Instance Type: t3.micro State: running Public IP: 54.144.179.171 Private IP: 10.0.0.10 VPC ID: vpc-9db1ce60 3. Instance ID: i-6463ecc6e20894a62 Subnet ID: subnet-default-c Availability Zone: us-east-1c Instance Type: t3.micro State: running Public IP: 54.144.29.136 Private IP: 172.31.32.10 VPC ID: vpc-default us-west-1: ---------- 1. Instance ID: i-794ef32b4de64a6f7 Subnet ID: subnet-93c6244d Availability Zone: us-west-1a Instance Type: t3.micro State: running Public IP: 54.144.69.12 Private IP: 10.0.0.10 VPC ID: vpc-f8f29d71 us-west-2: ---------- 1. Instance ID: i-ca26e23ef677e8e1a Subnet ID: subnet-20459abe Availability Zone: us-west-2a Instance Type: t3.micro State: running Public IP: 54.144.141.142 Private IP: 10.0.0.10 VPC ID: vpc-081a956d EOF cat /logs/agent/agent-output.txt
```

## Terraform — answered

14 commands, from `terraform-i3`.

```sh
cd /workspace/terraform && ./terraform state list | grep -E "aws_instance|aws_subnet|aws_route_table"
cd /workspace/terraform && ./terraform show -json > /tmp/state.json && cat /tmp/state.json
cd /workspace/terraform && jq '.values.root_module.child_modules[] | select(.resources[0].type == "aws_instance" or .resources[0].type == "aws_subnet") | {address: .resources[0].address, type: .resources[0].type, region: .resources[0].provider_name, values: .resources[0].values}' /tmp/state.json 2>/dev/null | head -200
cd /workspace/terraform && jq ' .values.root_module.child_modules[] | select(.resources[] | select(.type == "aws_instance" or .type == "aws_subnet" or .type == "aws_route_table")) | { module_name: .address, resources: [.resources[] | select(.type == "aws_instance" or .type == "aws_subnet" or .type == "aws_route_table" or .type == "aws_route_table_association") | { type, address, region: .values.region, id: .values.id, name: .values.tags.Name, subnet_id: .values.subnet_id, route_table_id: .values.id, route_table_subnet_ids: [.values.route | select(. != null) | .[].destination_cidr_block], map_public_ip_on_launch: .values.map_public_ip_on_launch, associate_public_ip_address: .values.associate_public_ip_address, routes: .values.route }] } ' /tmp/state.json 2>/dev/null
cd /workspace/terraform && jq ' .values.root_module.child_modules[] | .resources[] | select(.type == "aws_instance") | { instance_id: .values.id, instance_name: .values.tags.Name, region: .values.region, subnet_id: .values.subnet_id, availability_zone: .values.availability_zone, address: .address } ' /tmp/state.json 2>/dev/null | jq -s 'sort_by(.region)'
cd /workspace/terraform && jq ' .values.root_module.child_modules[] | .resources[] | select(.type == "aws_subnet") | { subnet_id: .values.id, region: .values.region, availability_zone: .values.availability_zone, map_public_ip_on_launch: .values.map_public_ip_on_launch, address: .address } ' /tmp/state.json 2>/dev/null | jq -s 'sort_by(.region)'
cd /workspace/terraform && jq ' .values.root_module.child_modules[] | .resources[] | select(.type == "aws_route_table" or .type == "aws_route_table_association") | { type, route_table_id: .values.id, subnet_id: .values.subnet_id, region: .values.region, routes: .values.route, address: .address } ' /tmp/state.json 2>/dev/null | jq -s 'sort_by(.region)'
cd /workspace/terraform && ./terraform state show module.primary.aws_route_table.public 2>/dev/null
cd /workspace/terraform && ./terraform state list | grep -E "aws_route[^_]|aws_internet_gateway"
cd /workspace/terraform && jq ' .values.root_module.child_modules[] | .resources[] | select(.type == "aws_route") | { region: .values.region, route_table_id: .values.route_table_id, destination_cidr_block: .values.destination_cidr_block, gateway_id: .values.gateway_id, address: .address } ' /tmp/state.json 2>/dev/null
cd /workspace/terraform && jq ' .values.root_module.child_modules[] | .resources[] | select(.type == "data" or (.type | contains("subnet"))) | select(.values.id | contains("subnet")) | { type, id: .values.id, region: .values.region, map_public_ip_on_launch: .values.map_public_ip_on_launch, address: .address } ' /tmp/state.json 2>/dev/null
cd /workspace/terraform && jq ' .values.root_module.child_modules[] | .resources[] | select(.mode == "data") | { type, address, region: .values.region, vpc_id: .values.vpc_id, ids: .values.ids } ' /tmp/state.json 2>/dev/null
# … 2 more
```

## Pulumi — answered

8 commands, from `pulumi-i3`.

```sh
cd /workspace/pulumi && ./pulumi-export | head -100
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, region: .outputs.availabilityZone, subnet_id: .outputs.subnetId, id: .outputs.id}' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {id: .outputs.id, urn, vpc_id: .outputs.vpcId, availability_zone: .outputs.availabilityZone}' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/routeTable:RouteTable" or .type == "aws:ec2/routeTableAssociation:RouteTableAssociation") | {type, urn, subnet_id: .inputs.subnetId, route_table_id: (.outputs.id // .inputs.routeTableId), routes: .inputs.routes}' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/routeTable:RouteTable") | {urn, id: .outputs.id, routes: .outputs.routes}' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/route:Route") | {urn, destination_cidr_block: .inputs.destinationCidrBlock, gateway_id: .inputs.gatewayId, route_table_id: .inputs.routeTableId}' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/routeTableAssociation:RouteTableAssociation") | {urn, subnet_id: .inputs.subnetId, route_table_id: .inputs.routeTableId, dependencies}' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.outputs.id == "subnet-default-c") | {type, urn, id: .outputs.id}' 2>/dev/null
```

## AWS CDK — answered

15 commands, from `cdk-i1`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {name: .key, instance: .value}' > /tmp/us-east-1-instances.json && cat /tmp/us-east-1-instances.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet") | {name: .key, properties: .value.Properties}' > /tmp/us-east-1-subnets.json && cat /tmp/us-east-1-subnets.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {name: .key, instance: .value}' > /tmp/us-west-1-instances.json && cat /tmp/us-west-1-instances.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet") | {name: .key, properties: .value.Properties}' > /tmp/us-west-1-subnets.json && cat /tmp/us-west-1-subnets.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {name: .key, instance: .value}' > /tmp/us-west-2-instances.json && cat /tmp/us-west-2-instances.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet") | {name: .key, properties: .value.Properties}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Subnet") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Name: .LogicalResourceId}' && echo "---" && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Subnet") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}' && echo "---" && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Subnet") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
aws ec2 describe-instances --instance-ids i-7d9001a08d554ad03 --region us-east-1 2>/dev/null | jq '.Reservations[].Instances[] | {InstanceId, SubnetId, AvailabilityZone, State: .State.Name}' || echo "Instance may not exist or cannot be queried"
# … 3 more
```

## Alchemy — answered

16 commands, from `alchemy-i3`.

```sh
cd /workspace/alchemy && alchemy state list
cd /workspace/alchemy && for res in instance ltServer privateServer webServer defaultVpcServer usw1-server usw2-server; do echo "=== $res ==="; alchemy state get alchemy-ec2-multiregion/bench/$res 2>/dev/null | jq '{kind, region: .output.region, subnet_id: .output.subnet_id, instance_id: .output.id}' || echo "Not found"; done
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/ltServer 2>/dev/null | jq '.output'
cd /workspace/alchemy && for res in ltServer privateServer webServer defaultVpcServer usw1-server usw2-server; do alchemy state get alchemy-ec2-multiregion/bench/$res 2>/dev/null | jq '{name: "'$res'", kind: .kind, region: .region, instance_id: .id, subnet_id: .SubnetId}'; done
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && for f in ltServer.json privateServer.json webServer.json defaultVpcServer.json usw1-server.json usw2-server.json; do echo "=== $f ==="; jq '{name: .desiredState | select(.SubnetId) | .SubnetId, id: .id, region: .region, instance_id: .InstanceId, subnet_id: .SubnetId}' "$f"; done
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && jq '.' ltServer.json | head -50
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && for f in ltServer.json privateServer.json webServer.json defaultVpcServer.json usw1-server.json usw2-server.json; do echo "=== $f ==="; jq '.output | {name: input_filename, id: .id, region: .region, instance_id: .InstanceId, subnet_id: .SubnetId, vpc_id: .VpcId}' "$f"; done
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && jq '.output | keys' public.json
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && jq '.output | keys' route.json
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && jq '.output | keys' assoc.json
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && jq '.output | keys' rt.json
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && jq '.output | {route_table_id: .routeTableId, vpc_id: .vpcId, region: .region}' rt.json
# … 4 more
```

## Alchemy v2 (Effect) — answered

8 commands, from `alchemy-effect-i3`.

```sh
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local 2>/dev/null | jq -r ' .resources[] | select(.state.resourceType == "AWS.EC2.Instance" or .state.resourceType == "AWS.EC2.Subnet") | { stack: .stack, fqn: .fqn, resourceType: .state.resourceType, subnetId: .state.attr.subnetId, mapPublicIpOnLaunch: .state.attr.mapPublicIpOnLaunch, instanceId: .state.attr.instanceId, state: .state.attr.state, publicIpAddress: .state.attr.publicIpAddress, vpcId: .state.attr.vpcId, availabilityZone: .state.attr.availabilityZone } ' | jq -s ' { instances: map(select(.resourceType == "AWS.EC2.Instance")), subnets: map(select(.resourceType == "AWS.EC2.Subnet")) } | .instances as $instances | .subnets as $subnets | ($instances | map( .subnetId as $subnet | . + { subnet_info: ($subnets[] | select(.subnetId == $subnet)) } )) as $with_subnet_info | $with_subnet_info[] ' 2>&1 | head -200
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local 2>/dev/null | jq -r ' .resources[] | select(.state.resourceType == "AWS.EC2.Instance" or .state.resourceType == "AWS.EC2.Subnet") | { stack: .stack, fqn: .fqn, resourceType: .state.resourceType, subnetId: .state.attr.subnetId, mapPublicIpOnLaunch: .state.attr.mapPublicIpOnLaunch, instanceId: .state.attr.instanceId, state: .state.attr.state, publicIpAddress: .state.attr.publicIpAddress, region: (.stack | split("-") | .[-1]), tags: .state.attr.tags } ' | jq -s ' .instances = map(select(.resourceType == "AWS.EC2.Instance")) | .subnets = map(select(.resourceType == "AWS.EC2.Subnet")) | .instances as $instances | .subnets as $subnets | ($instances | map( .subnetId as $subnet | . + { is_public: (($subnets[] | select(.subnetId == $subnet) | .mapPublicIpOnLaunch) == true) or (.publicIpAddress != null) } )) as $with_public | $with_public | map(select(.is_public == true)) ' 2>&1
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local 2>/dev/null | jq ' .resources as $all | ($all[] | select(.state.resourceType == "AWS.EC2.Instance")) as $instance | ($all[] | select(.state.resourceType == "AWS.EC2.Subnet" and .state.attr.subnetId == $instance.state.attr.subnetId)) as $subnet | select($subnet.state.attr.mapPublicIpOnLaunch == true) | { region: ($instance.stack | split("-") | .[-1]), instanceId: $instance.state.attr.instanceId, instanceName: ($instance.state.attr.tags.Name // "N/A"), subnetId: $instance.state.attr.subnetId, isPublic: ($subnet.state.attr.mapPublicIpOnLaunch // false), publicIpAddress: $instance.state.attr.publicIpAddress, availabilityZone: $instance.state.attr.availabilityZone, state: $instance.state.attr.state, stack: $instance.stack } ' 2>&1
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local 2>/dev/null | jq ' .resources as $all | [$all[] | select(.state.resourceType == "AWS.EC2.Instance")] as $instances | [$all[] | select(.state.resourceType == "AWS.EC2.Subnet")] as $subnets | $instances[] | . as $instance | ($subnets[] | select(.state.attr.subnetId == $instance.state.attr.subnetId)) as $subnet | select( ($subnet.state.attr.mapPublicIpOnLaunch == true) or ($instance.state.attr.publicIpAddress != null and $instance.state.attr.publicIpAddress != "") ) | { region: (.stack | split("-") | .[-1]), instanceId: .state.attr.instanceId, instanceName: (.state.attr.tags.Name // "N/A"), instanceFqn: .fqn, subnetId: .state.attr.subnetId, hasPublicIp: (.state.attr.publicIpAddress != null), publicIpAddress: .state.attr.publicIpAddress, availabilityZone: .state.attr.availabilityZone, vpcId: .state.attr.vpcId, state: .state.attr.state } | sort_by(.region, .instanceId) ' 2>&1
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local 2>/dev/null | jq '.resources[] | select(.state.resourceType == "AWS.EC2.Instance") | {stack: .stack, fqn: .fqn, instanceId: .state.attr.instanceId, name: (.state.attr.tags.Name // ""), subnetId: .state.attr.subnetId, publicIp: .state.attr.publicIpAddress, az: .state.attr.availabilityZone, state: .state.attr.state}' > /tmp/instances.json && cat /tmp/instances.json
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local 2>/dev/null | jq '.resources[] | select(.state.resourceType == "AWS.EC2.Subnet") | {stack: .stack, fqn: .fqn, subnetId: .state.attr.subnetId, mapPublicIpOnLaunch: .state.attr.mapPublicIpOnLaunch, vpcId: .state.attr.vpcId}' > /tmp/subnets.json && cat /tmp/subnets.json
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local 2>/dev/null | jq '.resources[] | select(.fqn == "LaunchTemplateServer")' > /tmp/launch_template.json && cat /tmp/launch_template.json
```
