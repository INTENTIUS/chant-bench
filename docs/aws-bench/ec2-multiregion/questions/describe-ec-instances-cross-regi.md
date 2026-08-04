# Describe my EC2 instances across the three regions.

`describe-ec-instances-cross-regi` · the answer aws-bench grades against: **4 / 1 / 1 by region**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-p3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show region,VpcId --explain
```

## No tool (AWS CLI) — answered

4 commands, from `bare-g3`.

```sh
aws ec2 describe-instances --region us-east-1 --output json | jq '.Reservations[].Instances[] | {InstanceId: .InstanceId, InstanceType: .InstanceType, State: .State.Name, VpcId: .VpcId, PrivateIpAddress: .PrivateIpAddress, Tags: .Tags}' > /tmp/us-east-1-instances.json
aws ec2 describe-instances --region us-west-1 --output json | jq '.Reservations[].Instances[] | {InstanceId: .InstanceId, InstanceType: .InstanceType, State: .State.Name, VpcId: .VpcId, PrivateIpAddress: .PrivateIpAddress, Tags: .Tags}' > /tmp/us-west-1-instances.json
aws ec2 describe-instances --region us-west-2 --output json | jq '.Reservations[].Instances[] | {InstanceId: .InstanceId, InstanceType: .InstanceType, State: .State.Name, VpcId: .VpcId, PrivateIpAddress: .PrivateIpAddress, Tags: .Tags}' > /tmp/us-west-2-instances.json
cat > /tmp/summary.txt << 'EOF' EC2 INSTANCES ACROSS REGIONS ============================ INSTANCE COUNT BY REGION: - us-east-1: 4 instances - us-west-1: 1 instance - us-west-2: 1 instance TOTAL: 6 instances US-EAST-1 INSTANCES (Grouped by VPC): ====================================== VPC: vpc-default (1 instance) ---- • i-a43810d9812ac7df0 (MyEC2Instance) - Type: t3.micro - State: running - Private IP: 172.31.32.10 VPC: vpc-dd9a4e4c (3 instances - SHARE NETWORK CONNECTIVITY) ----- • i-ce170d8eeade8435a (WebServerInstance) - Type: t3.micro - State: running - Private IP: 10.0.0.10 • i-debeba7e0e617a8ba (LaunchTemplateInstance) - Type: t3.micro - State: running - Private IP: 10.0.0.11 • i-de23d8cd841d5ea4a (PrivateInstance) - Type: t3.micro - State: running - Private IP: 10.0.1.10 OTHER REGIONS: ============== US-WEST-1 (1 instance): • i-5e9bf0c5296ba27f8 (WebServerInstance) - VPC: vpc-f5602c6d - Type: t3.micro - State: running - Private IP: 10.0.0.10 US-WEST-2 (1 instance): • i-a579a9be83b34ef4f (WebServerInstance) - VPC: vpc-deb73ab2 - Type: t3.micro - State: running - Private IP: 10.0.0.10 NETWORK CONNECTIVITY SUMMARY: ============================= The 3 instances in us-east-1 that share vpc-dd9a4e4c have network connectivity to each other within the same VPC. They can communicate directly via their private IP addresses: - 10.0.0.10 (WebServerInstance) - 10.0.0.11 (LaunchTemplateInstance) - 10.0.1.10 (PrivateInstance) The instance in vpc-default (172.31.32.10) is isolated in the default VPC and does not share network connectivity with the other three instances in us-east-1. EOF cat /tmp/summary.txt
```

## Terraform — answered

11 commands, from `terraform-g3`.

```sh
cd /workspace/terraform && ./terraform show -json > /tmp/state.json && jq '.values.root_module.resources[] | select(.type == "aws_instance") | {address, values: {instance_id, availability_zone, subnet_id, vpc_id, associate_public_ip_address, security_groups}}' /tmp/state.json
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.resources[] | select(.type == "aws_instance")'
cd /workspace/terraform && ./terraform show -json | head -50
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.resources[] | select(.type == "aws_instance") | {address, region: .values.availability_zone | .[:-1], availability_zone: .values.availability_zone, instance_id: .values.id, vpc_id: .values.vpc_id, subnet_id: .values.subnet_id, security_groups: .values.security_groups}'
cd /workspace/terraform && ./terraform state list | grep -i instance
cd /workspace/terraform && ./terraform state show module.primary.aws_instance.default_vpc_server && echo "---" && ./terraform state show module.primary.aws_instance.launch_template_server && echo "---" && ./terraform state show module.primary.aws_instance.private_server && echo "---" && ./terraform state show module.primary.aws_instance.web_server
cd /workspace/terraform && ./terraform state show module.primary.aws_instance.default_vpc_server | grep -E "subnet_id|vpc_security_group" && echo "---" && ./terraform state show module.primary.aws_instance.launch_template_server | grep -E "subnet_id|vpc_security_group" && echo "---" && ./terraform state show module.primary.aws_instance.private_server | grep -E "subnet_id|vpc_security_group" && echo "---" && ./terraform state show module.primary.aws_instance.web_server | grep -E "subnet_id|vpc_security_group"
cd /workspace/terraform && ./terraform state list | grep -E "aws_subnet|aws_vpc"
cd /workspace/terraform && ./terraform state show module.primary.aws_vpc.main && echo "---" && ./terraform state show module.primary.aws_subnet.public && echo "---" && ./terraform state show module.primary.aws_subnet.private && echo "---" && ./terraform state show 'module.primary.data.aws_vpc.default'
cd /workspace/terraform && ./terraform state show module.west1.aws_instance.server && echo "---" && ./terraform state show module.west2.aws_instance.server
cd /workspace/terraform && ./terraform state show module.west1.aws_vpc.main && echo "---" && ./terraform state show module.west2.aws_vpc.main
```

## Pulumi — answered

12 commands, from `pulumi-g3`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, region: .outputs.availabilityZone | gsub("[a-z]$"; ""), vpcId: .outputs.vpcId, instanceId: .outputs.id}' | head -100
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | .outputs | keys' | head -50
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[-1], region: (.outputs.availabilityZone | gsub("[a-z]$"; "")), subnetId: .outputs.networkInterfaces[0].subnetId, instanceId: .outputs.id, launchTemplate: .outputs.launchTemplate}' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[-1], region: (.outputs.availabilityZone | gsub("[a-z]$"; "")), instanceId: .outputs.id, networkInterfaces: .outputs.networkInterfaces}' 2>/dev/null | head -150
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[-1], inputs: .inputs | keys, dependencies: .dependencies}' 2>/dev/null | head -200
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {name: .urn | split("::")[-1], vpcId: .outputs.vpcId, subnetId: .outputs.id, availabilityZone: .outputs.availabilityZone}' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[-1], region: (.outputs.availabilityZone | gsub("[a-z]$"; "")), subnetId: .inputs.subnetId}' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | {name: .urn | split("::")[-1], vpcId: .outputs.id, cidr: .outputs.cidrBlock}' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | [.urn | split("::")[-1], (.outputs.availabilityZone | gsub("[a-z]$"; "")), .outputs.id, .outputs.instanceType] | @csv' | sort
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[-1], instanceId: .outputs.id, instanceType: .outputs.instanceType, region: (.outputs.availabilityZone | gsub("[a-z]$"; "")), subnetId: .inputs.subnetId}' 2>/dev/null | jq -s 'sort_by(.region, .name)'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {subnetId: .outputs.id, vpcId: .outputs.vpcId, name: .urn | split("::")[-1]}' 2>/dev/null | jq -s 'index_by(.subnetId)'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {subnetId: .outputs.id, vpcId: .outputs.vpcId, name: .urn | split("::")[-1]}' 2>/dev/null | jq -s 'map({(.subnetId): .vpcId}) | add'
```

## AWS CDK — answered

6 commands, from `cdk-g3`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logical_id: .key, properties: .value.Properties}' > /tmp/us-east-1-instances.json && cat /tmp/us-east-1-instances.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logical_id: .key, properties: .value.Properties}' > /tmp/us-west-1-instances.json && cat /tmp/us-west-1-instances.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logical_id: .key, properties: .value.Properties}' > /tmp/us-west-2-instances.json && cat /tmp/us-west-2-instances.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Subnet" or .value.Type == "AWS::EC2::VPC") | {logical_id: .key, type: .value.Type, properties: .value.Properties}'
cat > /logs/agent/agent-output.txt << 'EOF' # EC2 Instances Across Regions ## Summary by Region ### us-east-1: 4 instances - **WebServerInstance** (t3.micro) - Subnet: ResourcesVpcPublicSubnet1Subnet7103FD34 (Public, 10.0.0.0/24) - VPC: ResourcesVpc (10.0.0.0/16) - AZ: us-east-1a - **LaunchTemplateInstance** (t3.micro) - Subnet: ResourcesVpcPublicSubnet1Subnet7103FD34 (Public, 10.0.0.0/24) - VPC: ResourcesVpc (10.0.0.0/16) - AZ: us-east-1a - **PrivateInstance** (t3.micro) - Subnet: ResourcesVpcPrivateSubnet1Subnet98586872 (Private, 10.0.1.0/24) - VPC: ResourcesVpc (10.0.0.0/16) - AZ: us-east-1a - **MyEC2Instance** (t3.micro) - Subnet: subnet-default-a - VPC: Default VPC - AZ: us-east-1a ### us-west-1: 1 instance - **WebServerInstance** (t3.micro) - Subnet: ResourcesVpcPublicSubnet1Subnet7103FD34 (Public) - VPC: ResourcesVpc - AZ: us-west-1a ### us-west-2: 1 instance - **WebServerInstance** (t3.micro) - Subnet: ResourcesVpcPublicSubnet1Subnet7103FD34 (Public) - VPC: ResourcesVpc - AZ: us-west-2a --- ## Network Connectivity in us-east-1 ### Instances Sharing the Same VPC (ResourcesVpc - 10.0.0.0/16): **Same Subnet (Public - 10.0.0.0/24):** - WebServerInstance - LaunchTemplateInstance - → These two share the same public subnet and VPC, so they have direct Layer 2 connectivity **Different Subnet (Private - 10.0.1.0/24) in Same VPC:** - PrivateInstance - → Connected to the above two via the VPC's internal routing, assuming the route tables allow inter-subnet traffic **Isolated in Default VPC:** - MyEC2Instance - → In a separate VPC (default VPC), no VPC-native connectivity to the ResourcesVpc instances without VPC peering or Transit Gateway --- ## Total Instance Count: - **us-east-1**: 4 instances (3 in ResourcesVpc, 1 in default VPC) - **us-west-1**: 1 instance (in ResourcesVpc) - **us-west-2**: 1 instance (in ResourcesVpc) - **TOTAL**: 6 instances across all three regions --- ## Key Findings: 1. **WebServerInstance** is deployed consistently across all three regions (one per region). 2. **us-east-1 has specialized instance types**: - LaunchTemplateInstance (appears only in us-east-1) - PrivateInstance (appears only in us-east-1) - MyEC2Instance (appears only in us-east-1) 3. **VPC Network Topology in us-east-1**: - 3 instances are in the same custom VPC (ResourcesVpc): WebServerInstance, LaunchTemplateInstance, PrivateInstance - 1 instance is isolated in the default VPC: MyEC2Instance - The three instances in ResourcesVpc can communicate if security groups and NACLs permit - MyEC2Instance is network-isolated from the other three unless you set up VPC peering or a Transit Gateway EOF cat /logs/agent/agent-output.txt
```

## Alchemy — answered

6 commands, from `alchemy-g3`.

```sh
cd /workspace/alchemy && alchemy state list
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/instance
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/webServer alchemy-ec2-multiregion/bench/ltServer alchemy-ec2-multiregion/bench/defaultVpcServer alchemy-ec2-multiregion/bench/privateServer alchemy-ec2-multiregion/bench/usw1-server alchemy-ec2-multiregion/bench/usw2-server
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/webServer
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/ltServer && echo "---" && alchemy state get alchemy-ec2-multiregion/bench/defaultVpcServer && echo "---" && alchemy state get alchemy-ec2-multiregion/bench/privateServer
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/usw1-server && echo "---" && alchemy state get alchemy-ec2-multiregion/bench/usw2-server
```

## Alchemy v2 (Effect) — answered

15 commands, from `alchemy-effect-g2`.

```sh
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state stages --stack alchemy-effect-ec2-multiregion-us-east-1 us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-west-1.run.ts --local | grep -i instance
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench us-west-1.run.ts --local | grep -i instance
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-2 --stage bench us-west-1.run.ts --local | grep -i instance
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench us-west-1.run.ts --local
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn DefaultVpcServer us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn WebServer us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn PrivateServer us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state get --stack alchemy-effect-ec2-multiregion-us-east-1 --stage bench --fqn LaunchTemplateServer us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state resources --stack alchemy-effect-ec2-multiregion-us-west-1 --stage bench us-west-1.run.ts --local
# … 3 more
```
