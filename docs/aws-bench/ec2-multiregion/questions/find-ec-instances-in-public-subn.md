# Find my EC2 instances that are in a public subnet.

`find-ec-instances-in-public-subn` · the answer aws-bench grades against: **5**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

3 commands, from `chant-p3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-east-1 attr:internetFacing=true" --at latest --env floci --explain
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-west-1 attr:internetFacing=true" --at latest --env floci --explain
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-west-2 attr:internetFacing=true" --at latest --env floci --explain
```

## No tool (AWS CLI) — answered

4 commands, from `bare-g3`.

```sh
aws ec2 describe-subnets --region us-east-1 --output json | jq '.Subnets[] | {SubnetId, VpcId}' | head -20
cat > /tmp/find_public_instances.sh << 'EOF' #!/bin/bash REGIONS=("us-east-1" "us-west-1" "us-west-2") RESULTS="" for REGION in "${REGIONS[@]}"; do echo "=== Processing region: $REGION ===" >&2 # Get all subnets SUBNETS=$(aws ec2 describe-subnets --region "$REGION" --output json) # For each subnet, check if it's public (has route to IGW) PUBLIC_SUBNETS=$(echo "$SUBNETS" | jq -r '.Subnets[] | .SubnetId' | while read SUBNET_ID; do # Get route tables associated with this subnet ROUTES=$(aws ec2 describe-route-tables \ --region "$REGION" \ --filters "Name=association.subnet-id,Values=$SUBNET_ID" \ --output json) # If no explicit route table, check main route table if [ "$(echo "$ROUTES" | jq '.RouteTables | length')" -eq 0 ]; then ROUTES=$(aws ec2 describe-route-tables \ --region "$REGION" \ --filters "Name=vpc-id,Values=$(echo "$SUBNETS" | jq -r ".Subnets[] | select(.SubnetId==\"$SUBNET_ID\") | .VpcId")" \ --output json | jq '.RouteTables[] | select(.Associations[].Main == true)') fi # Check if any route goes to IGW (0.0.0.0/0 -> igw-*) IS_PUBLIC=$(echo "$ROUTES" | jq 'select(any(.Routes[]; .DestinationCidrBlock == "0.0.0.0/0" and .GatewayId | startswith("igw-")))' | jq -r '.RouteTableId' | head -1) if [ ! -z "$IS_PUBLIC" ]; then echo "$SUBNET_ID" fi done) # For each public subnet, get instances while read SUBNET_ID; do if [ ! -z "$SUBNET_ID" ]; then INSTANCES=$(aws ec2 describe-instances \ --region "$REGION" \ --filters "Name=subnet-id,Values=$SUBNET_ID" \ --output json) # Extract instance details echo "$INSTANCES" | jq -r ".Reservations[] | .Instances[] | { Region: \"$REGION\", InstanceId: .InstanceId, InstanceType: .InstanceType, SubnetId: .SubnetId, State: .State.Name, PublicIp: .PublicIpAddress, PrivateIp: .PrivateIpAddress, Tags: .Tags }" fi done <<< "$PUBLIC_SUBNETS" done EOF chmod +x /tmp/find_public_instances.sh /tmp/find_public_instances.sh
cat > /tmp/find_public_instances.sh << 'EOF' #!/bin/bash REGIONS=("us-east-1" "us-west-1" "us-west-2") for REGION in "${REGIONS[@]}"; do echo "=== Region: $REGION ===" >&2 # Get all subnets and their VPCs aws ec2 describe-subnets --region "$REGION" --output json | jq -r '.Subnets[] | "\(.SubnetId) \(.VpcId)"' | while read SUBNET_ID VPC_ID; do # Get route tables for this subnet ROUTE_TABLES=$(aws ec2 describe-route-tables \ --region "$REGION" \ --filters "Name=association.subnet-id,Values=$SUBNET_ID" \ --output json | jq -r '.RouteTables[].RouteTableId') # If no explicit route table, get main route table for the VPC if [ -z "$ROUTE_TABLES" ]; then ROUTE_TABLES=$(aws ec2 describe-route-tables \ --region "$REGION" \ --filters "Name=vpc-id,Values=$VPC_ID" "Name=association.main,Values=true" \ --output json | jq -r '.RouteTables[].RouteTableId') fi # Check if any route table has a route to IGW IS_PUBLIC=0 for RT in $ROUTE_TABLES; do if aws ec2 describe-route-tables \ --region "$REGION" \ --route-table-ids "$RT" \ --output json | jq -e '.RouteTables[0].Routes[] | select(.DestinationCidrBlock == "0.0.0.0/0" and (.GatewayId // "" | startswith("igw-")))' > /dev/null 2>&1; then IS_PUBLIC=1 break fi done # If public subnet, get instances if [ $IS_PUBLIC -eq 1 ]; then aws ec2 describe-instances \ --region "$REGION" \ --filters "Name=subnet-id,Values=$SUBNET_ID" "Name=instance-state-name,Values=running,stopped,pending,stopping" \ --output json | jq -r ".Reservations[] | .Instances[] | \"$REGION\t\(.InstanceId)\t\(.InstanceType)\t\(.State.Name)\t\(.PublicIpAddress // \"N/A\")\t\(.PrivateIpAddress)\t$SUBNET_ID\"" fi done done EOF chmod +x /tmp/find_public_instances.sh /tmp/find_public_instances.sh 2>/dev/null | sort -u
cat > /tmp/get_instance_details.sh << 'EOF' #!/bin/bash REGIONS=("us-east-1" "us-west-1" "us-west-2") # Temporary file to store results TEMP_FILE=$(mktemp) for REGION in "${REGIONS[@]}"; do # Get all subnets and their VPCs aws ec2 describe-subnets --region "$REGION" --output json | jq -r '.Subnets[] | "\(.SubnetId) \(.VpcId)"' | while read SUBNET_ID VPC_ID; do # Get route tables for this subnet ROUTE_TABLES=$(aws ec2 describe-route-tables \ --region "$REGION" \ --filters "Name=association.subnet-id,Values=$SUBNET_ID" \ --output json | jq -r '.RouteTables[].RouteTableId') # If no explicit route table, get main route table for the VPC if [ -z "$ROUTE_TABLES" ]; then ROUTE_TABLES=$(aws ec2 describe-route-tables \ --region "$REGION" \ --filters "Name=vpc-id,Values=$VPC_ID" "Name=association.main,Values=true" \ --output json | jq -r '.RouteTables[].RouteTableId') fi # Check if any route table has a route to IGW IS_PUBLIC=0 for RT in $ROUTE_TABLES; do if aws ec2 describe-route-tables \ --region "$REGION" \ --route-table-ids "$RT" \ --output json | jq -e '.RouteTables[0].Routes[] | select(.DestinationCidrBlock == "0.0.0.0/0" and (.GatewayId // "" | startswith("igw-")))' > /dev/null 2>&1; then IS_PUBLIC=1 break fi done # If public subnet, get instances with full details if [ $IS_PUBLIC -eq 1 ]; then aws ec2 describe-instances \ --region "$REGION" \ --filters "Name=subnet-id,Values=$SUBNET_ID" "Name=instance-state-name,Values=running,stopped,pending,stopping" \ --output json | jq -r ".Reservations[] | .Instances[] | { Region: \"$REGION\", SubnetId: \"$SUBNET_ID\", VpcId: \"$VPC_ID\", InstanceId, InstanceType, State: .State.Name, PublicIpAddress: (.PublicIpAddress // \"N/A\"), PrivateIpAddress, LaunchTime, Name: ((.Tags[] | select(.Key==\"Name\") | .Value) // \"N/A\") }" >> "$TEMP_FILE" fi done done # Sort and output if [ -f "$TEMP_FILE" ] && [ -s "$TEMP_FILE" ]; then cat "$TEMP_FILE" | jq -s 'sort_by(.Region, .InstanceId)' else echo "[]" fi rm -f "$TEMP_FILE" EOF chmod +x /tmp/get_instance_details.sh /tmp/get_instance_details.sh 2>/dev/null
```

## Terraform — answered

7 commands, from `terraform-g3`.

```sh
cd /workspace/terraform && ./terraform state list | grep -E 'aws_instance|aws_subnet' | head -20
cd /workspace/terraform && ./terraform show -json > /tmp/state.json && echo "State exported successfully"
cd /workspace/terraform && cat /tmp/state.json | jq ' .values.root_module.child_modules[] | { module_name: .address, instances: [ .resources[] | select(.type == "aws_instance") | { name: .address, subnet_id: .values.subnet_id, region: .values.region, availability_zone: .values.availability_zone, id: .values.id, private_ip: .values.private_ip, public_ip: .values.public_ip } ], subnets: [ .resources[] | select(.type == "aws_subnet") | { name: .address, subnet_id: .values.id, cidr: .values.cidr_block, map_public_ip_on_launch: .values.map_public_ip_on_launch, tags: .values.tags } ] } ' > /tmp/parsed_state.json && cat /tmp/parsed_state.json
cd /workspace/terraform && cat /tmp/state.json | jq ' .values.root_module.child_modules[0] | .resources[] | select(.type == "aws_instance" or .type == "data.*") | { type: .type, address: .address, subnet_id: .values.subnet_id, values: .values | keys } '
cd /workspace/terraform && find . -name "*.tf" -type f | head -10
cat > /tmp/final_report.txt << 'EOF' EC2 INSTANCES IN PUBLIC SUBNETS ================================ Query Results: Terraform State Analysis Regions: us-east-1, us-west-1, us-west-2 US-EAST-1 (3 instances in public subnets) ───────────────────────────────────────── 1. WebServerInstance (web_server) Instance ID: i-8c275ddc0a1f16d11 Private IP: 10.0.0.10 Public IP: 54.144.215.22 Subnet ID: subnet-8a3ad4ce (Custom VPC - Public) AZ: us-east-1a Terraform Address: module.primary.aws_instance.web_server 2. LaunchTemplateInstance (launch_template_server) Instance ID: i-16275595eeb7307f0 Private IP: 10.0.0.11 Public IP: 54.144.101.123 Subnet ID: subnet-8a3ad4ce (Custom VPC - Public) AZ: us-east-1a Terraform Address: module.primary.aws_instance.launch_template_server 3. MyEC2Instance (default_vpc_server) Instance ID: i-05652f1099c1bee3e Private IP: 172.31.32.10 Public IP: 54.144.107.163 Subnet ID: subnet-default-c (Default VPC - Internet-facing public subnet) AZ: us-east-1c Terraform Address: module.primary.aws_instance.default_vpc_server US-WEST-1 (1 instance in public subnet) ─────────────────────────────────────── 1. server Instance ID: i-0c9aa1b333cfdb2d1 Private IP: 10.0.0.10 Public IP: 54.144.190.196 Subnet ID: subnet-c65450fa (Public) AZ: us-west-1a Terraform Address: module.west1.aws_instance.server US-WEST-2 (1 instance in public subnet) ─────────────────────────────────────── 1. server Instance ID: i-5f2b8dad45b9f48c0 Private IP: 10.0.0.10 Public IP: 54.144.139.25 Subnet ID: subnet-1b25111e (Public) AZ: us-west-2a Terraform Address: module.west2.aws_instance.server SUMMARY ─────── Total Public Instances: 5 - us-east-1: 3 instances - us-west-1: 1 instance - us-west-2: 1 instance Excluded Instances (Private Subnet) ────────────────────────────────── - PrivateInstance (private_server) in us-east-1 Instance ID: i-38bc74b950427faec Subnet ID: subnet-cf7e926e (Private, 10.0.1.0/24) No Public IP Data Source: Terraform Applied State (terraform show -json) EOF cat /tmp/final_report.txt
cp /tmp/final_report.txt /logs/agent/agent-output.txt && cat /logs/agent/agent-output.txt
```

## Pulumi — missed

7 commands, from `pulumi-g3`.

```sh
cd /workspace/pulumi && ./pulumi-export > /tmp/pulumi-state.json && jq '.deployment.resources | length' /tmp/pulumi-state.json
jq '.deployment.resources[].type' /tmp/pulumi-state.json | sort | uniq -c
jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, region: .outputs.tags.pulumi_region, subnetId: .outputs.subnetId, publicIp: .outputs.publicIp}' /tmp/pulumi-state.json
jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {urn, availabilityZone: .outputs.availabilityZone, subnetId: .outputs.id, vpcId: .outputs.vpcId}' /tmp/pulumi-state.json
jq '.deployment.resources[] | select(.type == "aws:ec2/routeTableAssociation:RouteTableAssociation") | {urn, subnetId: .inputs.subnetId, routeTableId: .inputs.routeTableId}' /tmp/pulumi-state.json
jq '.deployment.resources[] | select(.type == "aws:ec2/route:Route") | {urn, routeTableId: .inputs.routeTableId, destinationCidrBlock: .inputs.destinationCidrBlock, gatewayId: .inputs.gatewayId}' /tmp/pulumi-state.json
cat > /tmp/find_instances.jq << 'EOF' # First, build a map of subnet to region (from AZ) def subnet_region: .deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {id: .outputs.id, region: .outputs.availabilityZone[:-1]}; # Build a map of subnet to public status def public_subnets: (.deployment.resources[] | select(.type == "aws:ec2/routeTableAssociation:RouteTableAssociation") | {subnet: .inputs.subnetId, routeTable: .inputs.routeTableId}) as $assoc | (.deployment.resources[] | select(.type == "aws:ec2/route:Route" and .inputs.destinationCidrBlock == "0.0.0.0/0") | .inputs.routeTableId) as $igw_route_tables | if $assoc.routeTable == $igw_route_tables then $assoc.subnet else empty end; # Find EC2 instances def instances: .deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {id: .outputs.id, subnet: .outputs.subnetId, publicIp: .outputs.publicIp, name: (.outputs.tags.Name // .urn | split("::")[-1])}; # Get all subnets with their regions (reduce subnet_region as $sr ({}; .[$sr.id] = $sr.region)) as $subnet_regions # Get all public subnets | (public_subnets | [.]) as $public_subnet_list # Find instances | (instances) as $instance | if ($public_subnet_list | index($instance.subnet)) then (if ($subnet_regions[$instance.subnet] == "us-east-1" or $subnet_regions[$instance.subnet] == "us-west-1" or $subnet_regions[$instance.subnet] == "us-west-2") then $instance + {region: $subnet_regions[$instance.subnet]} else empty end) else empty end EOF jq -f /tmp/find_instances.jq /tmp/pulumi-state.json
```

## AWS CDK — missed

25 commands, from `cdk-g3`.

```sh
cd /workspace/cdk_app && npx cdk ls 2>/dev/null
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq -r '.Resources | keys[] as $key | select(.Resources[$key].Type == "AWS::EC2::Instance") | "\(.Resources[$key].Type): \($key)"' 2>/dev/null | head -20
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries | map(select(.value.Type == "AWS::EC2::Instance")) | length'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries | map(select(.value.Type == "AWS::EC2::Instance")) | .[0]'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries | map(select(.value.Type == "AWS::EC2::Instance")) | map({ InstanceId: .key, SubnetRef: .value.Properties.SubnetId.Ref, InstanceType: .value.Properties.InstanceType, AZ: .value.Properties.AvailabilityZone, Name: (.value.Properties.Tags[] | select(.Key == "Name") | .Value) })'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries | map(select(.value.Type == "AWS::EC2::Instance")) | map({ InstanceId: .key, SubnetRef: .value.Properties.SubnetId.Ref, InstanceType: .value.Properties.InstanceType, AZ: .value.Properties.AvailabilityZone, Name: ((.value.Properties.Tags // []) | map(select(.Key == "Name") | .Value) | .[0]) })'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries | map(select(.value.Type == "AWS::EC2::Instance")) | map({ InstanceId: .key, SubnetId: .value.Properties.SubnetId, InstanceType: .value.Properties.InstanceType, AZ: .value.Properties.AvailabilityZone })'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries | map(select(.value.Type == "AWS::EC2::Subnet")) | map({ SubnetId: .key, Tags: (.value.Properties.Tags // []) })'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries | map(select(.value.Type == "AWS::EC2::Instance")) | map({ InstanceId: .key, SubnetId: .value.Properties.SubnetId, InstanceType: .value.Properties.InstanceType, AZ: .value.Properties.AvailabilityZone })'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries | map(select(.value.Type == "AWS::EC2::Instance")) | map({ InstanceId: .key, SubnetId: .value.Properties.SubnetId, InstanceType: .value.Properties.InstanceType, AZ: .value.Properties.AvailabilityZone })'
cd /workspace/cdk_app && aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
aws ec2 describe-subnets --filters "Name=tag:aws-cdk:subnet-type,Values=Public" --region us-east-1 2>/dev/null | jq '.Subnets[] | {SubnetId: .SubnetId, IsDefault: .DefaultForAz, Tags: .Tags}'
# … 13 more
```

## Alchemy — answered

26 commands, from `alchemy-g3`.

```sh
cd /workspace/alchemy && alchemy state list | head -50
cd /workspace/alchemy && alchemy state list | grep -i instance
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/instance
cd /workspace/alchemy && alchemy state list | grep -E "(Subnet|Instance|Server)" | sort
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/defaultVpcServer
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/ltServer
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/privateServer
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/webServer
cd /workspace/alchemy && alchemy state list | grep -E "usw1|usw2" | grep -v exp
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/usw1-server
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/usw2-server
cd /workspace/alchemy && alchemy state list | grep -E "public|route|rt|igw" | sort
# … 14 more
```

## Alchemy v2 (Effect) — answered

12 commands, from `alchemy-effect-g2`.

```sh
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-east-1 us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-west-1.run.ts --local | grep -E "(Instance|Subnet)"
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench us-west-1.run.ts --local | grep -E "(Instance|Subnet)"
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-2 --stage bench us-west-1.run.ts --local | grep -E "(Instance|Subnet)"
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn ExpInstanceId us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn ExpLaunchTemplateInstanceId us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn ExpPrivateInstanceId us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn ExpDefaultVPCInstanceId us-west-1.run.ts --local
find /workspace/alchemy/.alchemy/state -name "*.json" | xargs grep -l '"resourceType".*Instance' | head -20
find /workspace/alchemy/.alchemy/state -type f -name "*.json" | xargs grep -l "subnet-02d8dbe8\|subnet-57814f3c\|subnet-default-c\|subnet-987d6e23\|subnet-8fa0b49e" | head -20
```
