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

12 commands, from `cdk-m2`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq . > /tmp/us-east-1.json && echo "Synthesized us-east-1"
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq . > /tmp/us-west-1.json && echo "Synthesized us-west-1"
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq . > /tmp/us-west-2.json && echo "Synthesized us-west-2"
jq '.Resources | keys[] | select(. | contains("Subnet") or contains("Instance") or contains("RouteTable") or contains("InternetGateway"))' /tmp/us-east-1.json | head -20
cat > /tmp/find_instances.sh << 'EOF' #!/bin/bash declare -A results for region in us-east-1 us-west-1 us-west-2; do template_file="/tmp/${region}.json" # Find public subnet IDs (logical IDs) public_subnets=$(jq -r '.Resources | to_entries[] | select(.key | contains("PublicSubnet")) | select(.value.Type == "AWS::EC2::Subnet") | .key' "$template_file") echo "=== Region: $region ===" echo "Public Subnets (Logical IDs):" echo "$public_subnets" echo "" # For each instance, check its subnet jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | "\(.key)|\(.value.Properties.SubnetId)"' "$template_file" | while IFS='|' read -r instance_id subnet_ref; do echo "Instance: $instance_id, Subnet Ref: $subnet_ref" # Resolve subnet reference if [[ $subnet_ref == "Ref:"* ]] || [[ $subnet_ref == *"GetAtt"* ]]; then subnet_key=$(echo "$subnet_ref" | jq -r 'keys[0]' 2>/dev/null || echo "$subnet_ref") else subnet_key=$(echo "$subnet_ref" | sed 's/Ref: //') fi echo " Subnet Key: $subnet_key" done echo "" done EOF chmod +x /tmp/find_instances.sh bash /tmp/find_instances.sh
cat > /tmp/get_instances.sh << 'EOF' #!/bin/bash declare -A stack_map=( ["us-east-1"]="ec2-multiregion-EC2-ks84v1fh12-us-east-1" ["us-west-1"]="ec2-multiregion-EC2-ls9fuhb522-us-west-1" ["us-west-2"]="ec2-multiregion-EC2-ls9fuhb522-us-west-2" ) for region in us-east-1 us-west-1 us-west-2; do stack_name="${stack_map[$region]}" template_file="/tmp/${region}.json" echo "=== Region: $region (Stack: $stack_name) ===" # Get public subnet logical to physical ID mapping aws cloudformation describe-stack-resources \ --stack-name "$stack_name" \ --region "$region" \ --query 'StackResources[?LogicalResourceId==`ResourcesVpcPublicSubnet1Subnet7103FD34`].{Logical:LogicalResourceId, Physical:PhysicalResourceId}' \ --output text 2>/dev/null | while read -r logical physical; do [ -n "$logical" ] && echo "Public Subnet: $logical -> $physical" done # Get all EC2 instance resources with their physical IDs aws cloudformation describe-stack-resources \ --stack-name "$stack_name" \ --region "$region" \ --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].{Logical:LogicalResourceId, Physical:PhysicalResourceId}' \ --output text 2>/dev/null | while read -r logical physical; do [ -n "$logical" ] && echo "Instance: $logical -> $physical" done echo "" done EOF chmod +x /tmp/get_instances.sh bash /tmp/get_instances.sh
jq '.Resources.MyEC2InstanceB097982C' /tmp/us-east-1.json
aws ec2 describe-subnets \ --subnet-ids subnet-default-a \ --region us-east-1 \ --query 'Subnets[0].{SubnetId:SubnetId, AvailabilityZone:AvailabilityZone, MapPublicIpOnLaunch:MapPublicIpOnLaunch, CidrBlock:CidrBlock}' \ --output table 2>/dev/null || echo "Subnet not found or error checking"
cat > /tmp/verify_instances.sh << 'EOF' #!/bin/bash # Function to check if a subnet is public by verifying it has a route to IGW check_public_subnet() { local region=$1 local subnet_id=$2 # Check route table for internet gateway route aws ec2 describe-route-tables \ --region "$region" \ --filters "Name=association.subnet-id,Values=$subnet_id" \ --query 'RouteTables[0].Routes[?GatewayId!=null && starts_with(GatewayId, `igw-`)].GatewayId' \ --output text 2>/dev/null | grep -q "igw-" && echo "public" || echo "private" } # Verify instances in public subnets for region in us-east-1 us-west-1 us-west-2; do echo "=== Region: $region ===" aws ec2 describe-instances \ --region "$region" \ --query 'Reservations[].Instances[].{InstanceId:InstanceId, InstanceType:InstanceType, SubnetId:SubnetId, State:State.Name, PrivateIp:PrivateIpAddress}' \ --output text | while read -r instance_id instance_type subnet_id state private_ip; do if [ -n "$instance_id" ] && [[ "$instance_id" == i-* ]]; then is_public=$(check_public_subnet "$region" "$subnet_id") if [ "$is_public" = "public" ]; then echo "✓ Instance: $instance_id | Type: $instance_type | Subnet: $subnet_id | State: $state | PrivateIP: $private_ip" fi fi done echo "" done EOF chmod +x /tmp/verify_instances.sh bash /tmp/verify_instances.sh
cat > /tmp/find_public_instances.sh << 'EOF' #!/bin/bash for region in us-east-1 us-west-1 us-west-2; do echo "=== Region: $region ===" # Get all instances with their subnet IDs aws ec2 describe-instances \ --region "$region" \ --query 'Reservations[].Instances[].[InstanceId, SubnetId, InstanceType, State.Name, PrivateIpAddress]' \ --output text 2>/dev/null | while read -r instance_id subnet_id instance_type state private_ip; do if [ -z "$instance_id" ] || [[ ! "$instance_id" =~ ^i- ]]; then continue fi # Check if subnet is public by looking for IGW route igw_route=$(aws ec2 describe-route-tables \ --region "$region" \ --filters "Name=association.subnet-id,Values=$subnet_id" \ --query 'RouteTables[0].Routes[?GatewayId!=null].GatewayId' \ --output text 2>/dev/null | grep -c "igw-" || echo 0) # Also check MapPublicIpOnLaunch map_public=$(aws ec2 describe-subnets \ --region "$region" \ --subnet-ids "$subnet_id" \ --query 'Subnets[0].MapPublicIpOnLaunch' \ --output text 2>/dev/null) if [ "$igw_route" -gt 0 ] || [ "$map_public" = "True" ]; then echo "✓ $instance_id (Subnet: $subnet_id, Type: $instance_type, State: $state, PrivateIP: $private_ip)" fi done echo "" done EOF chmod +x /tmp/find_public_instances.sh bash /tmp/find_public_instances.sh
cat > /tmp/final_report.sh << 'EOF' #!/bin/bash echo "EC2 INSTANCES IN PUBLIC SUBNETS - us-east-1, us-west-1, us-west-2" > /logs/agent/agent-output.txt echo "======================================================================" >> /logs/agent/agent-output.txt echo "" >> /logs/agent/agent-output.txt echo "Report Generated: $(date)" >> /logs/agent/agent-output.txt echo "" >> /logs/agent/agent-output.txt for region in us-east-1 us-west-1 us-west-2; do echo "REGION: $region" >> /logs/agent/agent-output.txt echo "-------------------" >> /logs/agent/agent-output.txt aws ec2 describe-instances \ --region "$region" \ --query 'Reservations[].Instances[].[InstanceId, SubnetId, InstanceType, State.Name, PrivateIpAddress, Tags[?Key==`Name`].Value|[0]]' \ --output text 2>/dev/null | while read -r instance_id subnet_id instance_type state private_ip name; do if [ -z "$instance_id" ] || [[ ! "$instance_id" =~ ^i- ]]; then continue fi # Check if subnet is public map_public=$(aws ec2 describe-subnets \ --region "$region" \ --subnet-ids "$subnet_id" \ --query 'Subnets[0].MapPublicIpOnLaunch' \ --output text 2>/dev/null) if [ "$map_public" = "True" ]; then echo "" >> /logs/agent/agent-output.txt echo "Instance ID: $instance_id" >> /logs/agent/agent-output.txt echo "Instance Type: $instance_type" >> /logs/agent/agent-output.txt echo "State: $state" >> /logs/agent/agent-output.txt echo "Subnet ID: $subnet_id" >> /logs/agent/agent-output.txt echo "Private IP: $private_ip" >> /logs/agent/agent-output.txt [ -n "$name" ] && [ "$name" != "None" ] && echo "Name: $name" >> /logs/agent/agent-output.txt fi done echo "" >> /logs/agent/agent-output.txt done # Add summary echo "" >> /logs/agent/agent-output.txt echo "======================================================================" >> /logs/agent/agent-output.txt echo "SUMMARY" >> /logs/agent/agent-output.txt echo "======================================================================" >> /logs/agent/agent-output.txt total_instances=0 for region in us-east-1 us-west-1 us-west-2; do count=$(aws ec2 describe-instances \ --region "$region" \ --query 'Reservations[].Instances[].[InstanceId, SubnetId]' \ --output text 2>/dev/null | while read -r instance_id subnet_id; do if [[ "$instance_id" =~ ^i- ]] && [ -n "$subnet_id" ]; then map_public=$(aws ec2 describe-subnets \ --region "$region" \ --subnet-ids "$subnet_id" \ --query 'Subnets[0].MapPublicIpOnLaunch' \ --output text 2>/dev/null) [ "$map_public" = "True" ] && echo "1" fi done | wc -l) echo "$region: $count instances in public subnets" >> /logs/agent/agent-output.txt total_instances=$((total_instances + count)) done echo "" >> /logs/agent/agent-output.txt echo "Total: $total_instances EC2 instances in public subnets across all regions" >> /logs/agent/agent-output.txt cat /logs/agent/agent-output.txt EOF chmod +x /tmp/final_report.sh bash /tmp/final_report.sh
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

## Alchemy v2 (Effect) — answered

20 commands, from `alchemy-effect-m3`.

```sh
cd /workspace/alchemy && alchemy state tree us-east-1.run.ts --local 2>/dev/null | head -50
cd /workspace/alchemy && alchemy state tree us-west-1.run.ts --local 2>/dev/null | head -50
cd /workspace/alchemy && alchemy state tree us-west-2.run.ts --local 2>/dev/null | head -50
cd /workspace/alchemy && jq . .alchemy/state/alchemy-effect-ec2-multiregion-us-east-1/bench/WebServer.json
cd /workspace/alchemy && jq . .alchemy/state/alchemy-effect-ec2-multiregion-us-east-1/bench/LaunchTemplateServer.json
cd /workspace/alchemy && jq . .alchemy/state/alchemy-effect-ec2-multiregion-us-east-1/bench/PrivateServer.json
cd /workspace/alchemy && jq . .alchemy/state/alchemy-effect-ec2-multiregion-us-east-1/bench/DefaultVpcServer.json
cd /workspace/alchemy && jq . .alchemy/state/alchemy-effect-ec2-multiregion-us-east-1/bench/PublicSubnet.json
cd /workspace/alchemy && jq . .alchemy/state/alchemy-effect-ec2-multiregion-us-east-1/bench/PrivateSubnet.json
cd /workspace/alchemy && jq . .alchemy/state/alchemy-effect-ec2-multiregion-us-east-1/bench/PublicRouteTable.json
cd /workspace/alchemy && jq . .alchemy/state/alchemy-effect-ec2-multiregion-us-east-1/bench/InternetRoute.json
cd /workspace/alchemy && jq . .alchemy/state/alchemy-effect-ec2-multiregion-us-west-1/bench/WebServer.json
# … 8 more
```
