# Find my EC2 instances that are in a public subnet.

`find-ec-instances-in-public-subn` · the answer aws-bench grades against: **5**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

3 commands, from `chant-h3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance attr:internetFacing=true attr:region=us-east-1" --at latest --env floci --show VpcId,PrivateIpAddress,PublicIpAddress,region
cd /workspace/chant && chant search "kind:EC2::Instance attr:internetFacing=true attr:region=us-west-1" --at latest --env floci --show VpcId,PrivateIpAddress,PublicIpAddress,region
cd /workspace/chant && chant search "kind:EC2::Instance attr:internetFacing=true attr:region=us-west-2" --at latest --env floci --show VpcId,PrivateIpAddress,PublicIpAddress,region
```

## No tool (AWS CLI) — answered

2 commands, from `bare-h3`.

```sh
cat > /tmp/find_public_instances.sh << 'EOF' #!/bin/bash REGIONS=("us-east-1" "us-west-1" "us-west-2") PUBLIC_SUBNETS=() INSTANCES=() # Function to check if a subnet is public is_subnet_public() { local region=$1 local subnet_id=$2 # Get route tables associated with this subnet route_tables=$(aws ec2 describe-route-tables \ --region "$region" \ --filters "Name=association.subnet-id,Values=$subnet_id" \ --query 'RouteTables[*].RouteTableId' \ --output text) # If no explicit route table, check the main route table if [ -z "$route_tables" ]; then route_tables=$(aws ec2 describe-route-tables \ --region "$region" \ --filters "Name=association.main,Values=true" "Name=vpc-id,Values=$(aws ec2 describe-subnets --region "$region" --subnet-ids "$subnet_id" --query 'Subnets[0].VpcId' --output text)" \ --query 'RouteTables[*].RouteTableId' \ --output text) fi # Check if any route table has a route to an Internet Gateway for rt in $route_tables; do has_igw=$(aws ec2 describe-route-tables \ --region "$region" \ --route-table-ids "$rt" \ --query "RouteTables[0].Routes[?GatewayId!='local' && starts_with(GatewayId, 'igw-')].GatewayId" \ --output text) if [ -n "$has_igw" ]; then return 0 fi done return 1 } # Query each region for region in "${REGIONS[@]}"; do echo "Querying region: $region" >&2 # Get all instances with their subnet information aws ec2 describe-instances \ --region "$region" \ --query 'Reservations[*].Instances[*].[InstanceId,State.Name,InstanceType,SubnetId,PublicIpAddress,PrivateIpAddress,Tags[?Key==`Name`].Value|[0]]' \ --output json | jq -r '.[] | .[] | @json' | while read -r instance_json; do instance=$(echo "$instance_json" | jq -r '.') instance_id=$(echo "$instance" | jq -r '.[0]') subnet_id=$(echo "$instance" | jq -r '.[3]') # Check if subnet is public if is_subnet_public "$region" "$subnet_id"; then echo "$region|$instance" fi done done EOF chmod +x /tmp/find_public_instances.sh /tmp/find_public_instances.sh
cat > /logs/agent/agent-output.txt << 'EOF' EC2 INSTANCES IN PUBLIC SUBNETS ================================ REGION: us-east-1 ----------------- 1. Instance ID: i-96320d62e99beed98 Name: MyEC2Instance State: running Instance Type: t3.micro Subnet: subnet-default-c Public IP: 54.144.54.135 Private IP: 172.31.32.10 2. Instance ID: i-d451a3c39d8af7d4b Name: WebServerInstance State: running Instance Type: t3.micro Subnet: subnet-fd6bc7e6 Public IP: 54.144.123.66 Private IP: 10.0.0.10 3. Instance ID: i-36670ff4c187d213b Name: LaunchTemplateInstance State: running Instance Type: t3.micro Subnet: subnet-fd6bc7e6 Public IP: 54.144.217.19 Private IP: 10.0.0.11 REGION: us-west-1 ----------------- 1. Instance ID: i-9acb2e9325cc501ed Name: WebServerInstance State: running Instance Type: t3.micro Subnet: subnet-0bf04d09 Public IP: 54.144.58.12 Private IP: 10.0.0.10 REGION: us-west-2 ----------------- 1. Instance ID: i-887f6168c29802b1e Name: WebServerInstance State: running Instance Type: t3.micro Subnet: subnet-a861087c Public IP: 54.144.246.2 Private IP: 10.0.0.10 SUMMARY ======= Total instances in public subnets: 5 - us-east-1: 3 instances - us-west-1: 1 instance - us-west-2: 1 instance EOF cat /logs/agent/agent-output.txt
```

## Terraform — answered

8 commands, from `terraform-h3`.

```sh
cd /workspace/terraform && ./terraform show -json 2>/dev/null | jq -r '.values.root_module | [.resources, .child_modules[].resources] | flatten | .[] | select(.type == "aws_instance" or .type == "aws_subnet" or .type == "aws_route_table" or .type == "aws_route_table_association") | "\(.type)|\(.address)|\(.values | tostring)"' | head -100
cd /workspace/terraform && ./terraform show -json 2>/dev/null | jq -r '.values.root_module | [.resources, .child_modules[].resources] | flatten | .[] | select(.type == "aws_route" or .type == "aws_internet_gateway" or .type == "aws_subnet" and .values.id == "subnet-default-c") | "\(.type)|\(.address)|\(.values | tostring)"'
cd /workspace/terraform && ./terraform show -json 2>/dev/null | jq -r '.values.root_module | [.resources, .child_modules[].resources] | flatten | .[] | select(.type == "aws_subnet") | {id: .values.id, region: .values.region, cidr: .values.cidr_block, public: .values.map_public_ip_on_launch, tags: .values.tags}'
cd /workspace/terraform && ./terraform state list | grep -E "aws_instance|aws_subnet|aws_route_table" | sort
cd /workspace/terraform && ./terraform state show 'module.primary.aws_instance.default_vpc_server' | grep -E "subnet_id|public_ip|region"
cd /workspace/terraform && ./terraform state show 'module.primary.data.aws_subnets.default' 2>/dev/null || echo "Not found in state"
cd /workspace/terraform && ./terraform show -json 2>/dev/null | jq -r '.values.root_module | [.resources, .child_modules[].resources] | flatten | .[] | select(.type == "aws_route" or .type == "aws_internet_gateway") | select(.values.vpc_id == "vpc-default" or .values.region == "us-east-1") | "\(.type)|\(.values | tostring)"' | head -20
cat > /logs/agent/agent-output.txt << 'EOF' EC2 INSTANCES IN PUBLIC SUBNETS ================================ Across us-east-1, us-west-1, and us-west-2: US-EAST-1 (3 instances): 1. Instance ID: i-62ccf56ba1006698c Name: MyEC2Instance Subnet: subnet-default-c (AWS Default VPC) Public IP: 54.144.25.99 Private IP: 172.31.32.10 State: running 2. Instance ID: i-f31259f86e98bc791 Name: LaunchTemplateInstance Subnet: subnet-cd94f5f7 (10.0.0.0/24) Public IP: 54.144.152.120 Private IP: 10.0.0.11 State: running 3. Instance ID: i-a1fb067e4816f9a1c Name: WebServerInstance Subnet: subnet-cd94f5f7 (10.0.0.0/24) Public IP: 54.144.83.223 Private IP: 10.0.0.10 State: running US-WEST-1 (1 instance): 1. Instance ID: i-420f89c6443add7ba Name: WebServerInstance Subnet: subnet-a18ebf60 (10.0.0.0/24) Public IP: 54.144.92.11 Private IP: 10.0.0.10 State: running US-WEST-2 (1 instance): 1. Instance ID: i-583cb9324c5db36d5 Name: WebServerInstance Subnet: subnet-eb439eb5 (10.0.0.0/24) Public IP: 54.144.107.87 Private IP: 10.0.0.10 State: running SUMMARY: ======== Total instances in public subnets: 5 - us-east-1: 3 instances - us-west-1: 1 instance - us-west-2: 1 instance All instances have: ✓ Public IP addresses assigned ✓ Subnets with routes to Internet Gateways (IGW) ✓ Public IP auto-assignment enabled (except default VPC which inherits from account default) EOF cat /logs/agent/agent-output.txt
```

## Pulumi — answered

11 commands, from `pulumi-h3`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, region: .outputs.availabilityZone | .[:-1], subnetId: .outputs.subnetId, instanceId: .outputs.id, tags: .outputs.tags}' | head -100
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {id: .outputs.id, cidrBlock: .outputs.cidrBlock, mapPublicIpOnLaunch: .outputs.mapPublicIpOnLaunch, vpcId: .outputs.vpcId, availabilityZone: .outputs.availabilityZone}'
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/routeTable:RouteTable") | {id: .outputs.id, vpcId: .outputs.vpcId, routes: .outputs.routes}'
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/route:Route") | {destination: .inputs.destinationCidrBlock, gatewayId: .inputs.gatewayId, routeTableId: .inputs.routeTableId}'
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/routeTableAssociation:RouteTableAssociation") | {subnetId: .inputs.subnetId, routeTableId: .inputs.routeTableId}'
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | {id: .outputs.id, isDefault: .outputs.isDefault}'
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {id: .outputs.id, cidrBlock: .outputs.cidrBlock, vpcId: .outputs.vpcId, availabilityZone: .outputs.availabilityZone}' | grep -A 5 "default"
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | select((.outputs.subnetId == "subnet-d7d7fb21") or (.outputs.subnetId == "subnet-b7e0884c") or (.outputs.subnetId == "subnet-d1b65ca9")) | {name: .inputs.tags.Name // "N/A", instanceId: .outputs.id, region: .outputs.availabilityZone | .[:-1], subnetId: .outputs.subnetId}' | tee /tmp/results.json
cd /workspace/pulumi && ./pulumi-export > /tmp/state.json && cat /tmp/state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | select((.outputs.subnetId == "subnet-d7d7fb21") or (.outputs.subnetId == "subnet-b7e0884c") or (.outputs.subnetId == "subnet-d1b65ca9")) | {name: (.inputs.tags.Name | tostring), instanceId: .outputs.id, region: (.outputs.availabilityZone | .[:-1]), subnetId: .outputs.subnetId}'
cd /workspace/pulumi && cat /tmp/state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance" and .inputs.tags.Name == "MyEC2Instance") | {name: .inputs.tags.Name, instanceId: .outputs.id, region: (.outputs.availabilityZone | .[:-1]), subnetId: .outputs.subnetId}'
cat > /logs/agent/agent-output.txt << 'EOF' # EC2 Instances in Public Subnets ## Summary Found 5 EC2 instances in public subnets across us-east-1, us-west-1, and us-west-2. ## Instances by Region ### us-east-1 (3 instances) 1. **i-89c4532190f0f7108** (WebServerInstance) - Subnet: subnet-d7d7fb21 - Subnet Type: Public (mapPublicIpOnLaunch=true, route to IGW) 2. **i-c54ab5b597f3a4356** (LaunchTemplateInstance) - Subnet: subnet-d7d7fb21 - Subnet Type: Public (mapPublicIpOnLaunch=true, route to IGW) 3. **i-438371dd30873e1f7** (MyEC2Instance) - Subnet: subnet-default-c - Subnet Type: Public (Default VPC subnet - inherently public) ### us-west-1 (1 instance) 1. **i-9c5b7c544a8bb8588** (WebServerInstance) - Subnet: subnet-b7e0884c - Subnet Type: Public (mapPublicIpOnLaunch=true, route to IGW) ### us-west-2 (1 instance) 1. **i-ecdd069aef7173854** (WebServerInstance) - Subnet: subnet-d1b65ca9 - Subnet Type: Public (mapPublicIpOnLaunch=true, route to IGW) ## Analysis - All identified subnets have routes to Internet Gateways (IGW) - Default VPC subnets are public by design in AWS - The private server (i-4da5ba4e99a496207) in subnet-ce8ea49d was correctly excluded as it's in a private subnet without IGW route EOF cat /logs/agent/agent-output.txt
```

## AWS CDK — answered

5 commands, from `cdk-h3`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, Properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null > /tmp/us-east-1.json && cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null > /tmp/us-west-1.json && cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null > /tmp/us-west-2.json && echo "Synthesized all templates"
# Query us-east-1 for public subnets and their associated instances echo "=== us-east-1 ===" jq -r ' .Resources as $res | # Find public subnets (those with routes to IGW) ($res | to_entries[] | select(.value.Type == "AWS::EC2::Subnet") | {id: .key, props: .value.Properties}) as $subnet | # Get instances in public subnets ($res | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {name: .value.Properties.Tags[0].Value, subnetId: .value.Properties.SubnetId}) as $instance | ($subnet.props.CidrBlock, $subnet.id, $instance.subnetId) ' /tmp/us-east-1.json 2>/dev/null | head -30 # Get a better view - find subnets with internet gateway routes echo -e "\n=== Public Subnet Analysis us-east-1 ===" jq -r ' .Resources as $res | # Find route tables with IGW routes ($res | to_entries[] | select(.value.Type == "AWS::EC2::RouteTable") | .key) as $rtid | # Find routes in this table that point to IGW ($res | to_entries[] | select(.value.Type == "AWS::EC2::Route" and (.value.Properties.RouteTableId.Ref == $rtid or .value.Properties.RouteTableId == $rtid) and .value.Properties.GatewayId) | .value.Properties.RouteTableId) as $rt | # Find subnet associations with this route table ($res | to_entries[] | select(.value.Type == "AWS::EC2::SubnetRouteTableAssociation" and (.value.Properties.RouteTableId.Ref == $rtid or .value.Properties.RouteTableId == $rtid)) | .value.Properties.SubnetId) as $subnet_ref | # Find the actual subnet ($res | to_entries[] | select(.value.Type == "AWS::EC2::Subnet" and .key == ($subnet_ref.Ref // $subnet_ref)) | {name: .key, id: .value.LogicalResourceId, cidr: .value.Properties.CidrBlock}) as $subnet_info | # Find instances in this subnet ($res | to_entries[] | select(.value.Type == "AWS::EC2::Instance" and (.value.Properties.SubnetId.Ref == $subnet_info.name or .value.Properties.SubnetId == $subnet_info.id)) | .value.Properties.Tags[0].Value) as $instance_name | "\($subnet_info.name): \($subnet_info.cidr) -> Instance: \($instance_name)" ' /tmp/us-east-1.json 2>/dev/null
# Get physical IDs for instances in us-east-1 stack echo "=== US-EAST-1 Instances ===" aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].[LogicalResourceId,PhysicalResourceId]' --output table echo -e "\n=== US-WEST-1 Instances ===" aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].[LogicalResourceId,PhysicalResourceId]' --output table echo -e "\n=== US-WEST-2 Instances ===" aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 --query 'StackResources[?ResourceType==`AWS::EC2::Instance`].[LogicalResourceId,PhysicalResourceId]' --output table
```

## Alchemy — answered

14 commands, from `alchemy-h3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -E "aws::Instance|aws::Subnet" | head -30
cd /workspace/alchemy && alchemy state list
cd /workspace/alchemy && for resource in instance defaultVpcServer ltServer privateServer usw1-server usw2-server webServer; do echo "=== $resource ===" alchemy state get "alchemy-ec2-multiregion/bench/$resource" 2>/dev/null | jq -r '.kind, .output | {region, subnet_id, vpc_id, private_ip_address}' 2>/dev/null | head -10 done
cd /workspace/alchemy && alchemy state get "alchemy-ec2-multiregion/bench/instance" | head -50
cat /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench/defaultVpcServer.json
find /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench -name "*.json" -exec grep -l '"kind": "AWS::EC2::Instance"' {} \;
for file in /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench/{webServer,privateServer,usw2-server,usw1-server,defaultVpcServer,ltServer}.json; do echo "=== $(basename $file) ===" jq -r '.output | {id: .InstanceId, region: .region, subnet: .SubnetId, vpc: .VpcId, private_ip: .PrivateIp}' "$file" done
find /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench -name "*.json" -exec grep -l '"kind": "AWS::EC2::Subnet"' {} \; | sort
grep -r "subnet-" /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench/*.json | grep -E "(public|route)" | head -20
cat /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench/public.json
cat /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench/usw1-public.json | jq '.output | {subnetId, vpcId, region, mapPublicIpOnLaunch}'
cat /workspace/alchemy/.alchemy/alchemy-ec2-multiregion/bench/usw2-public.json | jq '.output | {subnetId, vpcId, region, mapPublicIpOnLaunch}'
# … 2 more
```

## Alchemy v2 (Effect) — answered

5 commands, from `alchemy-effect-h3`.

```sh
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-east-1" "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== $stack ===" alchemy state resources --stack "$stack" us-west-1.run.ts --local done
cd /workspace/alchemy && alchemy state stages us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state tree us-west-1.run.ts --local | head -100
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-east-1" "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== $stack ===" alchemy state resources --stack "$stack" --stage bench us-west-1.run.ts --local done
```
