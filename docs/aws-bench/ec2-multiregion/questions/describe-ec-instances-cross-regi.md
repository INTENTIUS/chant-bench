# Describe my EC2 instances across the three regions.

`describe-ec-instances-cross-regi` · the answer aws-bench grades against: **4 / 1 / 1 by region**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-b1`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show region,PrivateIpAddress,VpcId --explain
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
