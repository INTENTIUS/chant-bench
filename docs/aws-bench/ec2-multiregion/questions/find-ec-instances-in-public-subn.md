# Find my EC2 instances that are in a public subnet.

`find-ec-instances-in-public-subn` · the answer aws-bench grades against: **5**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-m1`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance attr:internetFacing=true" --at latest --env floci --show region,InstanceType,PrivateIpAddress --explain
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

12 commands, from `terraform-m1`.

```sh
cd /workspace/terraform && ./terraform state list | grep -E '(aws_instance|aws_subnet|aws_route_table)' | head -50
cd /workspace/terraform && ./terraform show -json > /tmp/terraform_state.json && echo "State exported to JSON"
cd /workspace/terraform && jq '.values.root_module.child_modules[] | {module_name: .address, instances: [.resources[] | select(.type == "aws_instance") | {address: .address, region: .values.availability_zone, instance_id: .values.id, subnet_id: .values.subnet_id}]} | select(.instances | length > 0)' /tmp/terraform_state.json
cd /workspace/terraform && jq '.values.root_module.child_modules[] | {module: .address, subnets: [.resources[] | select(.type == "aws_subnet") | {address: .address, subnet_id: .values.id, region: .values.availability_zone, cidr: .values.cidr_block}], route_tables: [.resources[] | select(.type == "aws_route_table") | {address: .address, rt_id: .values.id, routes: .values.routes}]}' /tmp/terraform_state.json
cd /workspace/terraform && jq '.values.root_module.child_modules[] | {module: .address, rtassoc: [.resources[] | select(.type == "aws_route_table_association") | {address: .address, subnet_id: .values.subnet_id, route_table_id: .values.route_table_id}]}' /tmp/terraform_state.json
cd /workspace/terraform && jq '.values.root_module.child_modules[] | .resources[] | select(.type == "aws_route_table") | {address: .address, id: .values.id, module: .path[-1], routes: .values.routes}' /tmp/terraform_state.json
cd /workspace/terraform && jq '.values.root_module.child_modules[] | {module: .address, routes: [.resources[] | select(.type == "aws_route") | {address: .address, route_table_id: .values.route_table_id, destination: .values.destination_cidr_block // .values.destination_ipv6_cidr_block, gateway_id: .values.gateway_id, nat_gateway_id: .values.nat_gateway_id}]}' /tmp/terraform_state.json
cd /workspace/terraform && jq '.values.root_module.child_modules[] | {module: .address, routes: [.resources[] | select(.type == "aws_route") | {address: .address, route_table_id: .values.route_table_id, destination: (.values.destination_cidr_block | select(. != null)), gateway_id: .values.gateway_id}]}' /tmp/terraform_state.json
cd /workspace/terraform && jq '.values.root_module.child_modules[] | .resources[] | select(.type == "data" or .type | contains("data")) | {type: .type, address: .address, values: .values}' /tmp/terraform_state.json
cd /workspace/terraform && jq '.values.root_module.child_modules[] | select(.address | contains("primary")) | {module: .address, datasources: [.resources[] | select(.type == "aws_subnets" or .type == "data" ) | {type: .type, address: .address}]}' /tmp/terraform_state.json
cd /workspace/terraform && jq '.values.root_module.child_modules[] | select(.address == "module.primary") | .resources[] | select(.type == "aws_subnets")' /tmp/terraform_state.json
cat > /tmp/analysis.txt << 'EOF' # EC2 Instances in Public Subnets ## Summary Found 5 EC2 instances deployed across public subnets in us-east-1, us-west-1, and us-west-2. ## US-EAST-1 Region (3 instances) ### Instance 1: web_server - Instance ID: i-ef9c24a234de9b352 - Availability Zone: us-east-1a - Subnet ID: subnet-74f30a2b (public subnet in custom VPC) - Subnet CIDR: 10.0.0.0/24 - Route Table: rtb-ff459b98 - Internet Gateway: igw-b2666be8 - Public Access: YES (via route 0.0.0.0/0 → igw-b2666be8) ### Instance 2: launch_template_server - Instance ID: i-7ed39183343ec7319 - Availability Zone: us-east-1a - Subnet ID: subnet-74f30a2b (public subnet in custom VPC) - Subnet CIDR: 10.0.0.0/24 - Route Table: rtb-ff459b98 - Internet Gateway: igw-b2666be8 - Public Access: YES (via route 0.0.0.0/0 → igw-b2666be8) - Note: Security group configured via launch template ### Instance 3: default_vpc_server - Instance ID: i-702137d810a7d56fd - Availability Zone: us-east-1c - Subnet ID: subnet-default-c (default VPC public subnet) - VPC: vpc-default - Public Access: YES (default VPC subnets are internet-facing) - Note: Deployed in AWS account default VPC --- ## US-WEST-1 Region (1 instance) ### Instance: server - Instance ID: i-1946ed4c443149f19 - Availability Zone: us-west-1a - Subnet ID: subnet-f82a16d3 (public subnet) - Subnet CIDR: 10.0.0.0/24 - Route Table: rtb-0613f412 - Internet Gateway: igw-7d57d43b - Public Access: YES (via route 0.0.0.0/0 → igw-7d57d43b) --- ## US-WEST-2 Region (1 instance) ### Instance: server - Instance ID: i-9eed568209b248421 - Availability Zone: us-west-2a - Subnet ID: subnet-1fb6074c (public subnet) - Subnet CIDR: 10.0.0.0/24 - Route Table: rtb-d11e7122 - Internet Gateway: igw-dc7d6945 - Public Access: YES (via route 0.0.0.0/0 → igw-dc7d6945) --- ## Instances NOT in Public Subnets (excluded) ### US-EAST-1: private_server - Instance ID: i-d65111136e4920bca - Availability Zone: us-east-1a - Subnet ID: subnet-d6845f2f (PRIVATE subnet) - Subnet CIDR: 10.0.1.0/24 - Public Access: NO (no internet gateway route) - Reason: Isolated private subnet by design --- ## Instance List Summary All EC2 instances in public subnets across us-east-1, us-west-1, and us-west-2: 1. i-702137d810a7d56fd (us-east-1, default VPC) 2. i-7ed39183343ec7319 (us-east-1, custom VPC) 3. i-ef9c24a234de9b352 (us-east-1, custom VPC) 4. i-1946ed4c443149f19 (us-west-1) 5. i-9eed568209b248421 (us-west-2) EOF cat /tmp/analysis.txt
```

## Pulumi — answered

6 commands, from `pulumi-m1`.

```sh
cd /workspace/pulumi && ./pulumi-export > /tmp/pulumi-state.json && echo "State exported successfully"
jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, region: .outputs.availabilityZone, subnetId: .outputs.subnetId}' /tmp/pulumi-state.json | head -50
jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {id: .outputs.id, arn: .arn, vpcId: .outputs.vpcId, mapPublicIpOnLaunch: .outputs.mapPublicIpOnLaunch, tags: .outputs.tags}' /tmp/pulumi-state.json
cat > /tmp/query.jq << 'EOF' # Build a map of subnet id to public status ( .deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {(.outputs.id): .outputs.mapPublicIpOnLaunch} ) as $subnet_map | # Build map of subnet id to vpc id ( .deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {(.outputs.id): .outputs.vpcId} ) as $subnet_vpc | # Find EC2 instances in target regions and public subnets .deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | select( (.outputs.availabilityZone | startswith("us-east-1")) or (.outputs.availabilityZone | startswith("us-west-1")) or (.outputs.availabilityZone | startswith("us-west-2")) ) | select($subnet_map[.outputs.subnetId] == true or .outputs.subnetId == "subnet-default-c") | { name: (.urn | split("::")[3]), instanceId: .outputs.id, region: (.outputs.availabilityZone | .[:-1]), availabilityZone: .outputs.availabilityZone, subnetId: .outputs.subnetId, vpcId: .outputs.vpcId, isPublic: ($subnet_map[.outputs.subnetId] // (if .outputs.subnetId == "subnet-default-c" then "default-vpc" else false end)) } EOF jq -f /tmp/query.jq /tmp/pulumi-state.json
jq -s ' # Build subnet map ( [.[0].deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet")] | map({(.outputs.id): {isPublic: .outputs.mapPublicIpOnLaunch, name: .outputs.tags.Name}}) | add ) as $subnets | # Get instances [.[0].deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | select( (.outputs.availabilityZone | startswith("us-east-1")) or (.outputs.availabilityZone | startswith("us-west-1")) or (.outputs.availabilityZone | startswith("us-west-2")) )] | # Filter to public subnets or default VPC map(select($subnets[.outputs.subnetId].isPublic == true or .outputs.subnetId == "subnet-default-c")) | unique_by(.outputs.id) | .[] | { name: (.urn | split("::")[3]), instanceId: .outputs.id, region: (.outputs.availabilityZone | .[:-1]), availabilityZone: .outputs.availabilityZone, subnetId: .outputs.subnetId, subnetName: $subnets[.outputs.subnetId].name } ' /tmp/pulumi-state.json
cat > /logs/agent/agent-output.txt << 'EOF' # EC2 Instances in Public Subnets ## Query Scope: us-east-1, us-west-1, us-west-2 ## Summary 5 EC2 instances found in public subnets across the specified regions: - us-east-1: 3 instances - us-west-1: 1 instance - us-west-2: 1 instance ## Instances ### us-east-1 Region 1. Instance Name: webServer Instance ID: i-31f8aa5ea3b5e7375 Availability Zone: us-east-1a Subnet ID: subnet-48b173fc Subnet Name: Public 2. Instance Name: ltServer Instance ID: i-dd98868a196b5b609 Availability Zone: us-east-1a Subnet ID: subnet-48b173fc Subnet Name: Public 3. Instance Name: defaultVpcServer Instance ID: i-b7ce59997740761a3 Availability Zone: us-east-1c Subnet ID: subnet-default-c Subnet Name: Default VPC (implicitly public) ### us-west-1 Region 1. Instance Name: usw1-server Instance ID: i-0e60377b9d285b3e3 Availability Zone: us-west-1a Subnet ID: subnet-64ea3205 Subnet Name: Public ### us-west-2 Region 1. Instance Name: usw2-server Instance ID: i-8a60e750df29eb589 Availability Zone: us-west-2a Subnet ID: subnet-d4b68c0e Subnet Name: Public ## Data Source Queried from Pulumi state export at /workspace/pulumi/. Public subnet determination: mapPublicIpOnLaunch = true, or instance in default VPC subnet. EOF cat /logs/agent/agent-output.txt
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

16 commands, from `alchemy-effect-m3`.

```sh
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-east-1 us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-west-1.run.ts --local | grep -i -E "(instance|subnet|route)" | head -30
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-west-1.run.ts --local | grep -i instance | grep -v "Profile\|Role\|Metadata\|Action\|Launch"
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn WebServer us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn PublicSubnet us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn LaunchTemplateServer us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn DefaultVpcServer us-west-1.run.ts --local && echo "---" && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn PrivateServer us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench --fqn WebServer us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench --fqn PublicSubnet us-west-1.run.ts --local
# … 4 more
```
