# Find my EC2 instances that are in a public subnet.

`find-ec-instances-in-public-subn` · the answer aws-bench grades against: **5**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

3 commands, from `chant-m3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance attr:internetFacing=true attr:region=us-east-1" --at latest --env floci --explain
cd /workspace/chant && chant search "kind:EC2::Instance attr:internetFacing=true attr:region=us-west-1" --at latest --env floci --explain
cd /workspace/chant && chant search "kind:EC2::Instance attr:internetFacing=true attr:region=us-west-2" --at latest --env floci --explain
```

## No tool (AWS CLI) — answered

10 commands, from `bare-m3`.

```sh
aws ec2 describe-instances --region us-east-1 --output json
aws ec2 describe-instances --region us-west-1 --output json
aws ec2 describe-instances --region us-west-2 --output json
aws ec2 describe-subnets --subnet-ids subnet-75f1c56f subnet-db00e426 subnet-default-c --region us-east-1 --output json
aws ec2 describe-subnets --subnet-ids subnet-a2688b5e --region us-west-1 --output json
aws ec2 describe-subnets --subnet-ids subnet-8e8eb4fe --region us-west-2 --output json
aws ec2 describe-route-tables --filters Name=vpc-id,Values=vpc-a6155e20 --region us-east-1 --output json
aws ec2 describe-route-tables --filters Name=vpc-id,Values=vpc-default --region us-east-1 --output json
aws ec2 describe-route-tables --filters Name=vpc-id,Values=vpc-9ad31e31 --region us-west-1 --output json
aws ec2 describe-route-tables --filters Name=vpc-id,Values=vpc-4ae644ae --region us-west-2 --output json
```

## Terraform — answered

16 commands, from `terraform-m3`.

```sh
cd /workspace/terraform && ./terraform show -json | jq . | head -50
cd /workspace/terraform && ./terraform show -json > /tmp/state.json && cat /tmp/state.json | jq '.values.root_module.resources[] | select(.type == "aws_instance") | {address, region: .values.availability_zone | .[:-1], subnet_id: .values.subnet_id, private_ip: .values.private_ip, public_ip: .values.public_ip}'
cd /workspace/terraform && ./terraform state list | grep aws_instance
cd /workspace/terraform && ./terraform state show module.primary.aws_instance.default_vpc_server
cd /workspace/terraform && ./terraform show -json | jq ' .values.root_module.resources | map(select(.type == "aws_instance")) | map({ address: .address, id: .values.id, region: .values.region, availability_zone: .values.availability_zone, subnet_id: .values.subnet_id, private_ip: .values.private_ip, public_ip: .values.public_ip, associate_public_ip: .values.associate_public_ip_address }) '
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.resources | length'
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module | keys'
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.child_modules[] | {module_address: .address, resources_count: (.resources | length)}'
cd /workspace/terraform && ./terraform show -json | jq ' .values.root_module.child_modules[] | . as $module | .resources[] | select(.type == "aws_instance" or .type == "aws_subnet") | { module: $module.address, type: .type, address: .address, id: .values.id, region: .values.region, availability_zone: .values.availability_zone, subnet_id: .values.subnet_id, map_public_ip_on_launch: .values.map_public_ip_on_launch, private_ip: .values.private_ip, public_ip: .values.public_ip } ' | head -100
cd /workspace/terraform && ./terraform show -json | jq ' def get_instances_and_subnets: .values.root_module.child_modules[] | . as $module | .resources[] | select(.type == "aws_instance" or .type == "aws_subnet") | { module: $module.address, type: .type, address: .address, id: .values.id, region: .values.region, subnet_id: .values.subnet_id, map_public_ip_on_launch: .values.map_public_ip_on_launch, public_ip: .values.public_ip }; get_instances_and_subnets ' > /tmp/all_resources.json && cat /tmp/all_resources.json
cd /workspace/terraform && ./terraform state show module.primary.aws_subnet.private module.primary.aws_subnet.public
cd /workspace/terraform && ./terraform state show module.primary.aws_subnet.public | grep -A 10 "map_public_ip_on_launch"
# … 4 more
```

## Pulumi — answered

6 commands, from `pulumi-m3`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.' | head -100
cd /workspace/pulumi && ./pulumi-export | jq ' .deployment.resources as $resources | # Create a map of resource IDs to resources for quick lookup ($resources | map({((.outputs.id // .outputs.arn // .urn): .)}) | add) as $idMap | # Find all EC2 instances ($resources[] | select(.type == "aws:ec2/instance:Instance")) as $instance | # Get the region - look in outputs ($instance.outputs.availabilityZone // $instance.inputs.availabilityZone) as $az | ($az | gsub("[a-z]$"; "")) as $region | # Only include instances from requested regions select($region == "us-east-1" or $region == "us-west-1" or $region == "us-west-2") | # Get subnet ID ($instance.outputs.subnetId // $instance.inputs.subnetId) as $subnetId | # Find the subnet resource ($resources[] | select(.outputs.id == $subnetId or .outputs.subnetId == $subnetId)) as $subnet | # Determine if subnet is public by checking if it has a route to an internet gateway ($subnet.outputs.tags // {}) as $subnetTags | # Get route table for this subnet - find the route table that has routes to internet gateway ($resources[] | select(.type == "aws:ec2/routeTable:RouteTable") | select( (.outputs.subnetId == $subnetId) or (.outputs.tags.Name // "" | contains("public")) or (.inputs.subnetId == $subnetId) ) ) as $rt | # Check if route table has a route to internet gateway (0.0.0.0/0) ($resources[] | select(.type == "aws:ec2/route:Route") | select(.outputs.routeTableId == $rt.outputs.id or .inputs.routeTableId == $rt.outputs.id) | select(.outputs.destinationCidrBlock == "0.0.0.0/0" or .inputs.destinationCidrBlock == "0.0.0.0/0") ) as $igwRoute | # Also check for mapPublicIpOnLaunch which indicates public subnet ($subnet.outputs.mapPublicIpOnLaunch // false) as $isPublic | select($isPublic or $igwRoute) | { instanceId: $instance.outputs.id, instanceName: ($instance.outputs.tags.Name // "N/A"), region: $region, subnetId: $subnetId, subnetName: ($subnet.outputs.tags.Name // "N/A"), isPublic: ($isPublic or ($igwRoute != null)), availabilityZone: $az } ' 2>/dev/null | jq -s 'sort_by(.region, .instanceId)'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | {type: .type, id: .outputs.id, name: (.outputs.tags.Name // .inputs.tags.Name // "N/A")} | select(.type | contains("ec2") or contains("subnet") or contains("route"))' | head -80
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {id: .outputs.id, name: (.outputs.tags.Name // "N/A"), subnetId: .outputs.subnetId, availabilityZone: .outputs.availabilityZone, region: (.outputs.availabilityZone | gsub("[a-z]$"; ""))} '
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {id: .outputs.id, name: (.outputs.tags.Name // "N/A"), mapPublicIpOnLaunch: .outputs.mapPublicIpOnLaunch, availabilityZone: .outputs.availabilityZone, region: (.outputs.availabilityZone | gsub("[a-z]$"; ""))}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet" or (.outputs.id | contains("subnet-default"))) | {id: .outputs.id, name: (.outputs.tags.Name // "N/A"), mapPublicIpOnLaunch: .outputs.mapPublicIpOnLaunch, type: .type}'
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

## Alchemy — answered

12 commands, from `alchemy-m3`.

```sh
cd /workspace/alchemy && alchemy state list | head -50
cd /workspace/alchemy && alchemy state list | grep -E '(instance|Instance)'
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/instance
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && grep -l "aws::Instance" *.json
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && head -20 *.json | grep -A5 '"kind"' | head -50
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && grep -l "AWS::EC2::Instance" *.json
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && for f in ltServer.json defaultVpcServer.json usw1-server.json privateServer.json webServer.json usw2-server.json; do echo "=== $f ==="; jq '.output | {id, subnetId, region, availabilityZone, privateIpAddress, publicIpAddress, associatePublicIpAddress}' "$f"; echo ""; done
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && for f in ltServer.json defaultVpcServer.json usw1-server.json privateServer.json webServer.json usw2-server.json; do echo "=== $f ==="; jq '{id: .output.id, region: .output.region, subnetId: .output.SubnetId, vpcId: .output.VpcId, privateIp: .output.PrivateIp}' "$f"; done
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && grep -l "Subnet\|aws::Subnet" *.json | head -10
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && jq -r '.output | {routeTableId, subnetId}' usw1-route.json
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && grep -l "rtb-d3adf990\|subnet-7d86b02c" *.json
cd /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench && jq -r '.fqn + ": " + .output.id + " (" + .output.region + ") - subnet: " + .output.SubnetId' ltServer.json defaultVpcServer.json usw1-server.json privateServer.json webServer.json usw2-server.json
```
