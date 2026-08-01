# Which EC2 instances are reachable via SSH from the internet?

`list-ec-instances-all-regions-1` · the answer aws-bench grades against: **2 — one only through its launch template**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-b1`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --explain --show region,internetFacing,effectiveIngress
```

## Terraform — answered

10 commands, from `terraform-m2`.

```sh
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module | keys' 2>/dev/null || echo "Trying alternate approach"
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.resources[] | select(.type == "aws_instance" or .type == "aws_security_group") | {type: .type, address: .address, values: .values}' 2>/dev/null | head -100
cd /workspace/terraform && ./terraform state list
cd /workspace/terraform && ./terraform state show 'module.primary.aws_instance.default_vpc_server'
cd /workspace/terraform && ./terraform state show 'module.primary.aws_instance.launch_template_server' && echo "---" && ./terraform state show 'module.primary.aws_instance.private_server' && echo "---" && ./terraform state show 'module.primary.aws_instance.web_server'
cd /workspace/terraform && ./terraform state show 'module.west1.aws_instance.server' && echo "---" && ./terraform state show 'module.west2.aws_instance.server'
cd /workspace/terraform && ./terraform state show 'module.primary.aws_launch_template.this'
cd /workspace/terraform && ./terraform state show 'module.primary.aws_security_group.web'
cd /workspace/terraform && ./terraform state list | grep -i "security_group_rule"
cd /workspace/terraform && ./terraform state show 'module.primary.aws_security_group.unused'
```

## Pulumi — answered

13 commands, from `pulumi-m2`.

```sh
cd /workspace/pulumi && ./pulumi-export > /tmp/pulumi-state.json && wc -l /tmp/pulumi-state.json
jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, outputs: {id: .outputs.id, availabilityZone: .outputs.availabilityZone, vpcSecurityGroupIds: .outputs.vpcSecurityGroupIds}, inputs: {subnetId: .inputs.subnetId, vpcSecurityGroupIds: .inputs.vpcSecurityGroupIds, iamInstanceProfile: .inputs.iamInstanceProfile, launchTemplate: .inputs.launchTemplate}}' /tmp/pulumi-state.json
jq '.deployment.resources[] | select(.type == "aws:ec2/securityGroup:SecurityGroup") | {urn, outputs: {id: .outputs.id, name: .outputs.name}, inputs: {name: .inputs.name, vpcId: .inputs.vpcId, ingress: .inputs.ingress}}' /tmp/pulumi-state.json
jq '.deployment.resources[] | select(.type == "aws:ec2/launchTemplate:LaunchTemplate") | {urn, outputs: {id: .outputs.id}, inputs: {vpcSecurityGroupIds: .inputs.vpcSecurityGroupIds}}' /tmp/pulumi-state.json
jq '.deployment.resources[] | select(.type == "aws:ec2/defaultSecurityGroup:DefaultSecurityGroup" or .type == "aws:ec2/securityGroupRule:SecurityGroupRule") | {urn, type: .type, outputs: {id: .outputs.id, groupId: .outputs.groupId}, inputs: {groupId: .inputs.groupId, cidrBlocks: .inputs.cidrBlocks, fromPort: .inputs.fromPort, toPort: .inputs.toPort}}' /tmp/pulumi-state.json
jq '.deployment.resources[] | select(.outputs.id == "sg-default") | {urn, type: .type, outputs: .outputs, inputs: .inputs}' /tmp/pulumi-state.json
jq '.deployment.resources | map(select(.type | contains("SecurityGroup"))) | .[] | {urn, type, outputs: (.outputs | keys), inputs: (.inputs | keys)}' /tmp/pulumi-state.json
jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: (.urn | split("::")[-1]), instanceId: .outputs.id, az: .outputs.availabilityZone, securityGroupIds: .outputs.vpcSecurityGroupIds}' /tmp/pulumi-state.json
aws ec2 describe-security-groups --group-ids sg-default --region us-east-1 2>/dev/null | jq '.SecurityGroups[0] | {GroupId, GroupName, VpcId, IpPermissions: .IpPermissions[]}'
aws ec2 describe-security-groups --group-ids sg-default --region us-east-1 2>&1 | head -50
aws ec2 describe-security-groups --group-ids sg-971cf528e004feafb --region us-east-1 2>&1 | jq '.SecurityGroups[0] | {GroupId, GroupName, IpPermissions: .IpPermissions[]}'
aws ec2 describe-security-groups --group-ids sg-default --region us-west-1 2>&1 | jq '.SecurityGroups[0] | {GroupId, GroupName, VpcId, IpPermissions}'
# … 1 more
```

## AWS CDK — answered

11 commands, from `cdk-cur`.

```sh
cd /workspace/cdk_app && npx cdk ls 2>/dev/null
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance" or .value.Type == "AWS::EC2::SecurityGroup") | {key: .key, type: .value.Type, properties: .value.Properties}' | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance" or .value.Type == "AWS::EC2::SecurityGroup") | {key: .key, type: .value.Type, properties: .value.Properties}' | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance" or .value.Type == "AWS::EC2::SecurityGroup") | {key: .key, type: .value.Type, properties: .value.Properties}' | head -100
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {LogicalId: .LogicalResourceId, PhysicalId: .PhysicalResourceId}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {name: .key, instance_name: .value.Properties.Tags[0].Value, security_groups: .value.Properties.SecurityGroupIds}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::SecurityGroup") | {name: .key, ingress: .value.Properties.SecurityGroupIngress}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources.LaunchTemplateInstance'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.key | contains("LaunchTemplate")) | {name: .key, type: .value.Type, properties: .value.Properties}'
```
