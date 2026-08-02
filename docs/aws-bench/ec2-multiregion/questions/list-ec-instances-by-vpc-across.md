# Which EC2 instances are in which VPCs across all regions?

`list-ec-instances-by-vpc-across` · the answer aws-bench grades against: **6 instances across 4 VPCs**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

2 commands, from `chant-m1`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show VpcId,region --explain
cd /workspace/chant && chant search "kind:EC2::VPC" --at latest --env floci --show region,CidrBlock --explain
```

## No tool (AWS CLI) — answered

3 commands, from `bare-m3`.

```sh
aws ec2 describe-instances --region us-east-1 --output json
aws ec2 describe-instances --region us-west-1 --output json
aws ec2 describe-instances --region us-west-2 --output json
```

## Terraform — answered

8 commands, from `terraform-m1`.

```sh
cd /workspace/terraform && ./terraform state list | grep -E "aws_instance|aws_vpc" | head -50
cd /workspace/terraform && ./terraform show -json
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module | (.child_modules[] as $mod | { "region": ($mod.resources[] | select(.type == "aws_vpc") | .values.region), "instances": [ $mod.resources[] | select(.type == "aws_instance") | { "name": .address, "id": .values.id, "vpc_id": .values.vpc_id, "subnet_id": .values.subnet_id, "availability_zone": .values.availability_zone } ] } | select(.instances | length > 0) )'
cd /workspace/terraform && ./terraform show -json | jq -r '.values.root_module | (.child_modules[] as $mod | { "region": ($mod.resources[] | select(.type == "aws_subnet" or .type == "aws_vpc") | .values.region // empty), "vpcs": [ $mod.resources[] | select(.type == "aws_vpc") | { "id": .values.id, "name": .address, "cidr": .values.cidr_block } ], "subnets": [ $mod.resources[] | select(.type == "aws_subnet") | { "id": .values.id, "vpc_id": .values.vpc_id, "cidr": .values.cidr_block } ] } | select(.vpcs | length > 0 or .subnets | length > 0) ) | select(.region)'
cd /workspace/terraform && ./terraform show -json > /tmp/state.json && jq '.values.root_module.child_modules[] | select(.resources[0].type != null) | { "module": .resources[0].provider_name, "vpcs": [.resources[] | select(.type == "aws_vpc") | {id: .values.id, name: .address, region: .values.region, cidr: .values.cidr_block}], "subnets": [.resources[] | select(.type == "aws_subnet") | {id: .values.id, vpc_id: .values.vpc_id, name: .address}] }' /tmp/state.json
cd /workspace/terraform && jq '.values.root_module.child_modules[] | { "module_name": .address, "instances": [.resources[] | select(.type == "aws_instance") | { id: .values.id, address: .address, subnet_id: .values.subnet_id, region: .values.region }] } | select(.instances | length > 0)' /tmp/state.json
cd /workspace/terraform && jq '.values.root_module.child_modules[] | (.resources[] | select(.type == "aws_vpc" or .type == "aws_subnet" or .type == "data.aws_vpc" or .type == "data.aws_subnet"))' /tmp/state.json | jq -s '.'
cat > /logs/agent/agent-output.txt << 'EOF' EC2 INSTANCES BY VPC AND REGION ================================ REGION: us-east-1 ----------------- VPC: vpc-default (Default VPC) - CIDR: 172.31.0.0/16 Instances: - i-702137d810a7d56fd (default_vpc_server) Subnet: subnet-default-c (AZ: us-east-1c) Name: default_vpc_server VPC: vpc-a45be95e (ResourcesVpc) - CIDR: 10.0.0.0/16 Instances: - i-7ed39183343ec7319 (launch_template_server) Subnet: subnet-74f30a2b (Public, CIDR: 10.0.0.0/24, AZ: us-east-1a) Name: launch_template_server - i-d65111136e4920bca (private_server) Subnet: subnet-d6845f2f (Private, CIDR: 10.0.1.0/24, AZ: us-east-1a) Name: private_server - i-ef9c24a234de9b352 (web_server) Subnet: subnet-74f30a2b (Public, CIDR: 10.0.0.0/24, AZ: us-east-1a) Name: web_server REGION: us-west-1 ----------------- VPC: vpc-8bf18bc2 (ResourcesVpc) - CIDR: 10.0.0.0/16 Instances: - i-1946ed4c443149f19 (server) Subnet: subnet-f82a16d3 (Public, CIDR: 10.0.0.0/24, AZ: us-west-1a) Name: server REGION: us-west-2 ----------------- VPC: vpc-fd8cc1c7 (ResourcesVpc) - CIDR: 10.0.0.0/16 Instances: - i-9eed568209b248421 (server) Subnet: subnet-1fb6074c (Public, CIDR: 10.0.0.0/24, AZ: us-west-2a) Name: server SUMMARY ======= Total VPCs: 4 - 1 Default VPC (us-east-1) - 3 Custom VPCs (ResourcesVpc in each region) Total Instances: 6 - us-east-1: 4 instances (1 in default VPC, 3 in vpc-a45be95e) - us-west-1: 1 instance (in vpc-8bf18bc2) - us-west-2: 1 instance (in vpc-fd8cc1c7) Instance Distribution by VPC: - vpc-default: 1 instance - vpc-a45be95e: 3 instances - vpc-8bf18bc2: 1 instance - vpc-fd8cc1c7: 1 instance EOF cat /logs/agent/agent-output.txt
```

## Pulumi — answered

9 commands, from `pulumi-m1`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, region: .outputs.availabilityZone | capture("(?<region>[a-z0-9-]+)[a-z]$") | .region, vpcId: .outputs.vpcId, subnetId: .outputs.subnetId, instanceId: .outputs.id}' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq ' .deployment.resources as $resources | [ $resources[] | select(.type == "aws:ec2/instance:Instance") | .outputs.subnetId as $subnetId | ( $resources[] | select(.type == "aws:ec2/subnet:Subnet" and .outputs.id == $subnetId) | .outputs.vpcId as $vpcId | ( $resources[] | select(.type == "aws:ec2/instance:Instance" and .outputs.subnetId == $subnetId) | { instanceName: .urn | split("::")[-1], instanceId: .outputs.id, region: (.outputs.availabilityZone | capture("(?<r>[a-z0-9-]+)[a-z]$") | .r), vpcId: $vpcId, subnetId: $subnetId } ) ) ] | group_by(.vpcId) | map({ vpcId: .[0].vpcId, instances: map({name: .instanceName, id: .instanceId, region: .region}) }) ' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq ' .deployment.resources as $resources | [ $resources[] | select(.type == "aws:ec2/instance:Instance") | .outputs.subnetId as $subnetId | ($resources[] | select(.type == "aws:ec2/subnet:Subnet" and .outputs.id == $subnetId) | .outputs.vpcId) as $vpcId | { instanceName: .urn | split("::")[-1], instanceId: .outputs.id, region: (.outputs.availabilityZone | capture("(?<r>[a-z0-9-]+)[a-z]$") | .r), vpcId: $vpcId, subnetId: $subnetId } ] | unique_by(.instanceId) | group_by(.vpcId) | map({ vpcId: (if .[0].vpcId == null then "default" else .[0].vpcId end), region: .[0].region, instances: map({name: .instanceName, id: .instanceId}) | unique_by(.id) }) | sort_by(.vpcId) ' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance" and (.urn | contains("defaultVpcServer"))) | {instanceName: .urn | split("::")[-1], instanceId: .outputs.id, region: (.outputs.availabilityZone | capture("(?<r>[a-z0-9-]+)[a-z]$") | .r), vpcId: .outputs.vpcId, subnetId: .outputs.subnetId}' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq ' .deployment.resources as $resources | [ $resources[] | select(.type == "aws:ec2/instance:Instance") | .outputs.subnetId as $subnetId | ($resources[] | select(.type == "aws:ec2/subnet:Subnet" and .outputs.id == $subnetId) | .outputs.vpcId) as $vpcId | { instanceName: .urn | split("::")[-1], instanceId: .outputs.id, region: (.outputs.availabilityZone | capture("(?<r>[a-z0-9-]+)[a-z]$") | .r), vpcId: (if .outputs.vpcId != null then .outputs.vpcId else ($vpcId // "default") end), subnetId: $subnetId } ] | unique_by(.instanceId) | group_by(.vpcId) | sort_by(.[0].vpcId) | map({ vpcId: .[0].vpcId, instances: (map({name: .instanceName, id: .instanceId, region: .region}) | sort_by(.name)) }) ' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq ' .deployment.resources as $resources | [ $resources[] | select(.type == "aws:ec2/instance:Instance") as $inst | ( if $inst.outputs.vpcId != null then { instanceName: $inst.urn | split("::")[-1], instanceId: $inst.outputs.id, region: ($inst.outputs.availabilityZone | capture("(?<r>[a-z0-9-]+)[a-z]$") | .r), vpcId: $inst.outputs.vpcId, subnetId: $inst.outputs.subnetId } else # VPC ID is in outputs but null, try to get from subnet ($resources[] | select(.type == "aws:ec2/subnet:Subnet" and .outputs.id == $inst.outputs.subnetId) | .outputs.vpcId) as $vpcId | { instanceName: $inst.urn | split("::")[-1], instanceId: $inst.outputs.id, region: ($inst.outputs.availabilityZone | capture("(?<r>[a-z0-9-]+)[a-z]$") | .r), vpcId: ($vpcId // "default"), subnetId: $inst.outputs.subnetId } end ) ] | unique_by(.instanceId) | group_by(.vpcId) | sort_by(.[0].vpcId) | map({ vpcId: .[0].vpcId, instances: (map({name: .instanceName, id: .instanceId, region: .region}) | sort_by(.name)) }) ' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[-1], id: .outputs.id, region: (.outputs.availabilityZone | capture("(?<r>[a-z0-9-]+)[a-z]$") | .r), vpcId: .outputs.vpcId}' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export > /tmp/pulumi-state.json && jq ' .deployment.resources as $resources | # Create a map of subnet ID to VPC ID ($resources | map(select(.type == "aws:ec2/subnet:Subnet") | {(.outputs.id): .outputs.vpcId}) | add) as $subnetToVpc | # Get all instances [ $resources[] | select(.type == "aws:ec2/instance:Instance") | .outputs.subnetId as $subnetId | { name: .urn | split("::")[-1], id: .outputs.id, region: (.outputs.availabilityZone | capture("(?<r>[a-z0-9-]+)[a-z]$") | .r), vpcId: ($subnetToVpc[$subnetId] // (if .outputs.vpcId then .outputs.vpcId else "default (AWS managed)" end)), subnetId: $subnetId } ] | sort_by(.region, .name) ' /tmp/pulumi-state.json 2>/dev/null
cat > /logs/agent/agent-output.txt << 'EOF' EC2 INSTANCES BY VPC AND REGION ================================ SUMMARY ------- Total instances: 6 Total VPCs: 4 (1 AWS managed default + 3 custom) Regions: us-east-1, us-west-1, us-west-2 INSTANCES GROUPED BY VPC ------------------------ 1. DEFAULT VPC (AWS Managed) - us-east-1 └─ defaultVpcServer (i-b7ce59997740761a3) Subnet: subnet-default-c 2. vpc-209676c6 - us-east-1 (3 instances) ├─ ltServer (i-dd98868a196b5b609) │ Subnet: subnet-48b173fc ├─ privateServer (i-77ea5a355fd3b0c38) │ Subnet: subnet-52a8630e └─ webServer (i-31f8aa5ea3b5e7375) Subnet: subnet-48b173fc 3. vpc-d7675f73 - us-west-1 (1 instance) └─ usw1-server (i-0e60377b9d285b3e3) Subnet: subnet-64ea3205 4. vpc-f177c74b - us-west-2 (1 instance) └─ usw2-server (i-8a60e750df29eb589) Subnet: subnet-d4b68c0e INSTANCES BY REGION ------------------- us-east-1: • defaultVpcServer (i-b7ce59997740761a3) → default (AWS managed) • ltServer (i-dd98868a196b5b609) → vpc-209676c6 • privateServer (i-77ea5a355fd3b0c38) → vpc-209676c6 • webServer (i-31f8aa5ea3b5e7375) → vpc-209676c6 us-west-1: • usw1-server (i-0e60377b9d285b3e3) → vpc-d7675f73 us-west-2: • usw2-server (i-8a60e750df29eb589) → vpc-f177c74b INSTANCES BY VPC ---------------- default (AWS managed): ├─ Region: us-east-1 └─ Count: 1 vpc-209676c6: ├─ Region: us-east-1 └─ Count: 3 vpc-d7675f73: ├─ Region: us-west-1 └─ Count: 1 vpc-f177c74b: ├─ Region: us-west-2 └─ Count: 1 EOF cat /logs/agent/agent-output.txt
```

## AWS CDK — answered

8 commands, from `cdk-m3`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-QARoles-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type=="AWS::EC2::Instance" or .value.Type=="AWS::EC2::VPC" or .value.Type=="AWS::EC2::Subnet") | {logicalId: .key, type: .value.Type, properties: .value.Properties}'
cd /workspace/cdk_app && for stack in "ec2-multiregion-QARoles-us-east-1" "ec2-multiregion-EC2-ks84v1fh12-us-east-1" "ec2-multiregion-EC2-ls9fuhb522-us-west-1" "ec2-multiregion-EC2-ls9fuhb522-us-west-2"; do echo "=== Stack: $stack ===" npx cdk synth "$stack" --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type=="AWS::EC2::Instance") | {logicalId: .key, vpcId: .value.Properties.SubnetId, securityGroups: .value.Properties.SecurityGroupIds}' 2>/dev/null done
cd /workspace/cdk_app && for stack in "ec2-multiregion-QARoles-us-east-1" "ec2-multiregion-EC2-ks84v1fh12-us-east-1" "ec2-multiregion-EC2-ls9fuhb522-us-west-1" "ec2-multiregion-EC2-ls9fuhb522-us-west-2"; do echo "=== Template for: $stack ===" npx cdk synth "$stack" --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type=="AWS::EC2::VPC" or .value.Type=="AWS::EC2::Subnet") | {logicalId: .key, type: .value.Type, vpcId: .value.Properties.VpcId}' 2>/dev/null | head -30 done
cd /workspace/cdk_app && for stack in "ec2-multiregion-QARoles-us-east-1" "ec2-multiregion-EC2-ks84v1fh12-us-east-1" "ec2-multiregion-EC2-ls9fuhb522-us-west-1" "ec2-multiregion-EC2-ls9fuhb522-us-west-2"; do region=$(echo $stack | grep -oE '(us-east-1|us-west-1|us-west-2)') echo "=== Stack: $stack (Region: $region) ===" aws cloudformation describe-stack-resources --stack-name "$stack" --region "$region" 2>/dev/null | jq '.StackResources[] | select(.ResourceType=="AWS::EC2::Instance" or .ResourceType=="AWS::EC2::VPC" or .ResourceType=="AWS::EC2::Subnet") | {logicalId: .LogicalResourceId, physicalId: .PhysicalResourceId, type: .ResourceType}' 2>/dev/null done
aws ec2 describe-instances --instance-ids i-6a62f03f1b63e02cb i-d49fa51ee7943b064 i-99a5057f76dd16760 i-3e459933b4e4a49c1 --region us-east-1 --query 'Reservations[*].Instances[*].[InstanceId,SubnetId,VpcId]' --output json
aws ec2 describe-instances --instance-ids i-006e65b4905bccbb5 --region us-west-1 --query 'Reservations[*].Instances[*].[InstanceId,SubnetId,VpcId]' --output json
aws ec2 describe-instances --instance-ids i-1018901c5ceef586e --region us-west-2 --query 'Reservations[*].Instances[*].[InstanceId,SubnetId,VpcId]' --output json
```

## Alchemy — answered

9 commands, from `alchemy-m3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -E "aws::Instance|aws::Vpc" | head -30
cd /workspace/alchemy && alchemy state list
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/instance
cd /workspace/alchemy && for name in webServer defaultVpcServer ltServer privateServer usw1-server usw2-server; do echo "=== $name ==="; alchemy state get alchemy-ec2-multiregion/bench/$name | jq '.output | {id, region, vpcId, subnetId}' 2>/dev/null || echo "Not found"; done
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/webServer | jq '.output' 2>/dev/null
cd /workspace/alchemy && for name in webServer defaultVpcServer ltServer privateServer usw1-server usw2-server; do echo "=== $name ==="; alchemy state get alchemy-ec2-multiregion/bench/$name 2>/dev/null | jq '.output | {region, InstanceId, VpcId}'; done
cd /workspace/alchemy && for vpc in vpc usw1-vpc usw2-vpc; do echo "=== $vpc ==="; alchemy state get alchemy-ec2-multiregion/bench/$vpc 2>/dev/null | jq '.output | {VpcId, region, CidrBlock}'; done
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/vpc | jq '.output'
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/usw1-vpc | jq '.output' && echo "---" && alchemy state get alchemy-ec2-multiregion/bench/usw2-vpc | jq '.output'
```

## Alchemy v2 (Effect) — answered

16 commands, from `alchemy-effect-m3`.

```sh
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-east-1 us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-west-1 us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-west-2 us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-2 --stage bench us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn Vpc us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench --fqn Vpc us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-west-2 --stage bench --fqn Vpc us-west-1.run.ts --local
cd /workspace/alchemy && for instance in DefaultVpcServer WebServer PrivateServer LaunchTemplateServer; do echo "=== us-east-1: $instance ==="; alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn "$instance" us-west-1.run.ts --local 2>/dev/null | jq '{fqn: .fqn, resourceType: .resourceType, attr: {instanceId: .attr.instanceId, vpcId: .attr.vpcId, subnetId: .attr.subnetId}}'; done
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn LaunchTemplateServer us-west-1.run.ts --local | jq '{fqn: .fqn, resourceType: .resourceType, attr: {instanceId: .attr.instanceId, vpcId: .attr.vpcId, subnetId: .attr.subnetId}}'
# … 4 more
```
