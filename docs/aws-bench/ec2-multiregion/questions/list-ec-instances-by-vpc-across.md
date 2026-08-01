# Which EC2 instances are in which VPCs across all regions?

`list-ec-instances-by-vpc-across` · the answer aws-bench grades against: **6 instances across 4 VPCs**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-m3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show VpcId,PrivateIpAddress,PublicIpAddress,region --explain
```

## Terraform — answered

10 commands, from `terraform-m3`.

```sh
cd /workspace/terraform && ./terraform state list | grep -E 'aws_instance|aws_ec2_instance|aws_vpc' | head -30
cd /workspace/terraform && ./terraform show -json > /tmp/state.json && echo "State exported to JSON"
cd /workspace/terraform && jq -r '.values.root_module | .. | select(type == "object" and .type == "aws_instance") | "\(.address): vpc_id=\(.values.vpc_id), subnet_id=\(.values.subnet_id), private_ip=\(.values.private_ip)"' /tmp/state.json
cd /workspace/terraform && ./terraform state show module.primary.aws_instance.web_server
cd /workspace/terraform && jq -r ' .values.root_module | ( [.. | select(type == "object" and .type == "aws_subnet") | {address: .address, values: .values}] as $subnets | [.. | select(type == "object" and .type == "aws_vpc") | {address: .address, values: .values}] as $vpcs | [.. | select(type == "object" and .type == "aws_instance") | {address: .address, values: .values}] as $instances | $instances[] | .values.subnet_id as $subnet_id | ($subnets[] | select(.values.id == $subnet_id)) as $subnet | ($vpcs[] | select(.values.id == $subnet.values.vpc_id)) as $vpc | "\(.address) | Region: \($instances[] | select(.values | has("region")) | select(.values.id == .values.id) .values.region // "unknown") | VPC: \($vpc.address) (id: \($vpc.values.id)) | Subnet: \($subnet.address) (id: \($subnet_id))" ) ' /tmp/state.json 2>/dev/null | sort
cd /workspace/terraform && ./terraform state list | grep 'aws_instance\.' | while read instance; do echo "=== $instance ===" ./terraform state show "$instance" | grep -E '^\s+(id|region|subnet_id|arn)\s*=' | head -10 done
cd /workspace/terraform && ./terraform state list | grep 'aws_subnet\.' | while read subnet; do echo "=== $subnet ===" ./terraform state show "$subnet" | grep -E '^\s+(id|vpc_id)\s*=' done
cd /workspace/terraform && ./terraform state list | grep 'aws_vpc\.' | while read vpc; do echo "=== $vpc ===" ./terraform state show "$vpc" | grep -E '^\s+(id|cidr_block)' | head -2 done
cd /workspace/terraform && ./terraform state show 'module.primary.data.aws_vpc.default' | grep -E '^\s+id\s*=' | head -1
cat > /logs/agent/agent-output.txt << 'EOF' EC2 INSTANCES BY REGION AND VPC ================================ REGION: us-east-1 ================= VPC: vpc-default (Default VPC, 172.31.0.0/16) - Instance: default_vpc_server ID: i-300b21df4a83914d9 Subnet: subnet-default-c Private IP: 172.31.32.10 VPC: vpc-2bab67cb (Custom VPC, 10.0.0.0/16) - Instance: web_server ID: i-0ba6a42ade430f176 Subnet: subnet-7a6b81fa (public) Private IP: 10.0.0.10 Public IP: 54.144.13.131 - Instance: launch_template_server ID: i-b41235d7d93348f6e Subnet: subnet-7a6b81fa (public) Private IP: 10.0.0.11 - Instance: private_server ID: i-58d75f672379b0574 Subnet: subnet-4fb8565b (private) Private IP: 10.0.1.10 REGION: us-west-1 ================= VPC: vpc-6d5e4dff (Custom VPC, 10.0.0.0/16) - Instance: server ID: i-6b85edfbf78860085 Subnet: subnet-84ebef7c (public) Private IP: 10.0.0.10 REGION: us-west-2 ================= VPC: vpc-7f5be42b (Custom VPC, 10.0.0.0/16) - Instance: server ID: i-0a3101c51d65b7d3c Subnet: subnet-7f98cb00 (public) Private IP: 10.0.0.10 SUMMARY ======= Total Instances: 6 - us-east-1: 4 instances (2 VPCs: 1 default + 1 custom) - us-west-1: 1 instance (1 custom VPC) - us-west-2: 1 instance (1 custom VPC) VPC Summary: - vpc-default (AWS default VPC in us-east-1): 1 instance - vpc-2bab67cb (module.primary, us-east-1): 3 instances - vpc-6d5e4dff (module.west1, us-west-1): 1 instance - vpc-7f5be42b (module.west2, us-west-2): 1 instance EOF cat /logs/agent/agent-output.txt
```

## Pulumi — answered

13 commands, from `pulumi-m3`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, region: .outputs.availabilityZone | rtrimstr((.outputs.availabilityZone[-1:])), vpc: .outputs.vpcId, subnetId: .outputs.subnetId, instanceId: .outputs.id, tags: .outputs.tags}' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, outputs: {vpcId, id, availabilityZone, tags}}' | head -100
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance")' | jq . | head -200
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn | split("::")[-1], instanceId: .outputs.id, region: .outputs.arn | match("arn:aws:ec2:([^:]+):").captures[0].string, availabilityZone: .outputs.availabilityZone, subnetId: .outputs.subnetId, tags: .outputs.tags}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {subnetId: .outputs.id, subnetArn: .outputs.arn, vpcId: .outputs.vpcId}' | grep -E '(subnetId|vpcId)'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/vpc:Vpc") | {vpcId: .outputs.id, arn: .outputs.arn, tags: .outputs.tags}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet" or .type == "aws:ec2/defaultSubnet:DefaultSubnet") | {subnetId: .outputs.id, vpcId: .outputs.vpcId, arn: .outputs.arn}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type | contains("default")) | {type, id: .outputs.id, vpcId: .outputs.vpcId, arn: .outputs.arn}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ssm/parameter:Parameter" and .inputs.name | contains("DefaultVpcId")) | {name: .inputs.name, value: .outputs.value}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type == "aws:ssm/parameter:Parameter" and (.inputs.name | type == "string" and contains("DefaultVpcId"))) | {name: .inputs.name, value: .outputs.value}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type | contains("Vpc") or contains("Subnet")) | {type, id: .outputs.id, vpcId: .outputs.vpcId}'
cd /workspace/pulumi && ./pulumi-export 2>/dev/null | jq '.deployment.resources[] | select(.type | contains("get") or contains("data")) | {type, id: .outputs.id, urn}'
# … 1 more
```

## AWS CDK — answered

14 commands, from `cdk-cur`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | with_entries(select(.value.Type == "AWS::EC2::Instance")) | to_entries[] | {LogicalId: .key, Properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | with_entries(select(.value.Type == "AWS::EC2::VPC" or .value.Type == "AWS::EC2::Subnet")) | to_entries[] | {LogicalId: .key, Type: .value.Type, Properties: .value.Properties}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Type: .ResourceType}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::VPC" or .ResourceType == "AWS::EC2::Subnet") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Type: .ResourceType}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources.ResourcesVpcPublicSubnet1Subnet7103FD34, .Resources.ResourcesVpcPrivateSubnet1Subnet98586872'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | with_entries(select(.value.Type == "AWS::EC2::Instance")) | to_entries[] | {LogicalId: .key, Properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | with_entries(select(.value.Type == "AWS::EC2::VPC" or .value.Type == "AWS::EC2::Subnet")) | to_entries[] | {LogicalId: .key, Type: .value.Type}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance" or .ResourceType == "AWS::EC2::VPC" or .ResourceType == "AWS::EC2::Subnet") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Type: .ResourceType}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance" or .ResourceType == "AWS::EC2::VPC" or .ResourceType == "AWS::EC2::Subnet") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId, Type: .ResourceType}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | with_entries(select(.value.Type == "AWS::EC2::Instance")) | map({LogicalId: .key, SubnetRef: .value.Properties.SubnetId})'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, SubnetId: .value.Properties.SubnetId}'
# … 2 more
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
