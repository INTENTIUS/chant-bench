# Describe my EC2 instances across the three regions.

`describe-ec-instances-cross-regi` · the answer aws-bench grades against: **4 / 1 / 1 by region**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-b1`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show region,PrivateIpAddress,VpcId --explain
```

## Terraform — answered

11 commands, from `terraform-m2`.

```sh
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.resources[] | select(.type == "aws_instance") | {address: .address, values: .values}' > /tmp/instances.json && cat /tmp/instances.json | jq -s 'length'
cd /workspace/terraform && ./terraform state list | head -20
cd /workspace/terraform && ./terraform state list | grep -E 'module\.|aws_instance' | sort
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.child_modules[] | select(.address | startswith("module.primary")) | .resources[] | select(.type == "aws_instance") | {name: .address, region: "us-east-1", vpc_id: .values.vpc_id, subnet_id: .values.subnet_id, instance_id: .values.id}' && \ ./terraform show -json | jq '.values.root_module.child_modules[] | select(.address | startswith("module.west1")) | .resources[] | select(.type == "aws_instance") | {name: .address, region: "us-west-1", vpc_id: .values.vpc_id, subnet_id: .values.subnet_id, instance_id: .values.id}' && \ ./terraform show -json | jq '.values.root_module.child_modules[] | select(.address | startswith("module.west2")) | .resources[] | select(.type == "aws_instance") | {name: .address, region: "us-west-2", vpc_id: .values.vpc_id, subnet_id: .values.subnet_id, instance_id: .values.id}'
cd /workspace/terraform && ./terraform state show module.primary.aws_instance.default_vpc_server
cd /workspace/terraform && ./terraform state show module.primary.aws_instance.web_server && echo "---" && ./terraform state show module.primary.aws_instance.private_server && echo "---" && ./terraform state show module.primary.aws_instance.launch_template_server
cd /workspace/terraform && ./terraform state show module.primary.aws_vpc.main && echo "---" && ./terraform state show module.primary.aws_subnet.public && echo "---" && ./terraform state show module.primary.aws_subnet.private
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.child_modules[] | select(.address == "module.primary") | .data_resources[] | select(.type == "aws_vpc") | {type: .type, name: .address, vpc_id: .values.id}' && echo "---" && ./terraform show -json | jq '.values.root_module.child_modules[] | select(.address == "module.primary") | .data_resources[] | select(.type == "aws_subnets") | {type: .type, name: .address, subnets: .values.ids}'
cd /workspace/terraform && ./terraform state show 'module.primary.data.aws_vpc.default'
cd /workspace/terraform && ./terraform state show module.west1.aws_instance.server && echo "---" && ./terraform state show module.west1.aws_vpc.main
cd /workspace/terraform && ./terraform state show module.west2.aws_instance.server && echo "---" && ./terraform state show module.west2.aws_vpc.main
```

## Pulumi — answered

7 commands, from `pulumi-m2`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn: .urn, region: .outputs.availabilityZone | gsub("[a-z]$"; ""), vpcId: .outputs.vpcId, subnetId: .outputs.subnetId, securityGroupIds: .outputs.securityGroupIds}' | head -100
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance")' | jq -s 'map({name: (.urn | split("::")[-1]), region: .outputs.availabilityZone | gsub("[a-z]$"; ""), instanceId: .outputs.id, vpcId: .outputs.vpcId, subnetId: .outputs.subnetId}) | group_by(.region) | map({region: .[0].region, count: length, instances: map(.name)}) | sort_by(.region)'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources | map(select(.type == "aws:ec2/subnet:Subnet") | {arn: .arn, subnetId: .outputs.id, vpcId: .outputs.vpcId}) | map(select(.subnetId != null))' | jq -s 'INDEX(.subnetId)'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {subnetId: .outputs.id, vpcId: .outputs.vpcId}'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet")'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: (.urn | split("::")[-1]), instanceId: .outputs.id, subnetId: .outputs.subnetId, region: .outputs.availabilityZone | gsub("[a-z]$"; ""), vpcId: .outputs.vpcId}' | jq -s '.'
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance")' | head -200
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
