# Describe my EC2 instances across the three regions.

`describe-ec-instances-cross-regi` · the answer aws-bench grades against: **4 / 1 / 1 by region**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-m3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show region,VpcId,PrivateIpAddress --explain
```

## Terraform — answered

21 commands, from `terraform-m3`.

```sh
cd /workspace/terraform && ./terraform show -json | jq . > /tmp/tf_state.json && wc -l /tmp/tf_state.json
cd /workspace/terraform && jq -r '.values.root_module.resources[] | select(.type=="aws_instance") | "\(.address) | \(.values.availability_zone) | \(.values.vpc_id) | \(.values.tags // {})' /tmp/tf_state.json
cd /workspace/terraform && jq '.values.root_module.resources[] | select(.type=="aws_instance") | {address: .address, region: .values.availability_zone, vpc: .values.vpc_id, instance_id: .values.id}' /tmp/tf_state.json
jq 'keys' /tmp/tf_state.json
jq '.values.root_module | keys' /tmp/tf_state.json
jq '.values.root_module.resources | length' /tmp/tf_state.json
jq '.values.root_module.resources[] | {type: .type, address: .address}' /tmp/tf_state.json
jq '.values.root_module.child_modules | length' /tmp/tf_state.json
jq '.values.root_module.child_modules[] | .address' /tmp/tf_state.json
jq -r ' def get_instances: (.resources // []) | map(select(.type=="aws_instance") | { address: .address, instance_id: .values.id, availability_zone: .values.availability_zone, vpc_id: .values.vpc_id, subnet_id: .values.subnet_id, tags: .values.tags }) as $root_instances | $root_instances + ((.child_modules // []) | map(get_instances | .[])); [.values.root_module | get_instances] ' /tmp/tf_state.json
jq '.values.root_module.child_modules[] | select(.address | startswith("module")) | {module: .address, instance_count: (.resources // [] | map(select(.type=="aws_instance")) | length)}' /tmp/tf_state.json
jq ' .values.root_module.child_modules[] | { module: .address, instances: [(.resources // [] | map(select(.type=="aws_instance") | { address: .address, instance_id: .values.id, availability_zone: .values.availability_zone, vpc_id: .values.vpc_id, subnet_id: .values.subnet_id, private_ip: .values.private_ip, tags: .values.tags }))] } ' /tmp/tf_state.json
# … 9 more
```

## Pulumi — answered

3 commands, from `pulumi-m3`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, inputs: {availability_zone: .inputs.availability_zone}, outputs: {id: .outputs.id, vpc_id: .outputs.vpc_id, subnet_id: .outputs.subnet_id, security_groups: .outputs.vpc_security_group_ids}}' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance")' 2>/dev/null
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {urn: .urn, outputs: {id: .outputs.id, vpcId: .outputs.vpcId}}' 2>/dev/null
```

## AWS CDK — answered

11 commands, from `cdk-cur`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::VPC" or .value.Type == "AWS::EC2::Subnet") | {logicalId: .key, type: .value.Type, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, subnet: .value.Properties.SubnetId}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, subnet: .value.Properties.SubnetId}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance" or .value.Type == "AWS::EC2::VPC" or .value.Type == "AWS::EC2::Subnet") | {logicalId: .key, type: .value.Type, subnet: .value.Properties.SubnetId, vpcId: .value.Properties.VpcId}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance" or .value.Type == "AWS::EC2::VPC" or .value.Type == "AWS::EC2::Subnet") | {logicalId: .key, type: .value.Type, subnet: .value.Properties.SubnetId, vpcId: .value.Properties.VpcId}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {name: .key, instance_name: .value.Properties.Tags[]? | select(.Key == "Name") | .Value, subnet: .value.Properties.SubnetId}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources.LaunchTemplateInstance'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance")'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance")'
```

## Alchemy — answered

3 commands, from `alchemy-m3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -i instance
cd /workspace/alchemy && alchemy state get alchemy-ec2-multiregion/bench/exp-DefaultVPCInstanceId
cd /workspace/alchemy && alchemy state list | grep "aws::Instance"
```
