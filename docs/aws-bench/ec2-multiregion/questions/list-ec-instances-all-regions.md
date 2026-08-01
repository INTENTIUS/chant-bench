# List my account's EC2 instance ids in all regions.

`list-ec-instances-all-regions` · the answer aws-bench grades against: **6 instances across 3 regions**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

1 commands, from `chant-m1`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show region
```

## Terraform — answered

3 commands, from `terraform-m2`.

```sh
cd /workspace/terraform && ./terraform state list | grep -E 'aws_instance'
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.child_modules[] | {module_name: .address, instances: [.resources[] | select(.type == "aws_instance") | {resource_address: .address, instance_id: .values.id, region: .values.provider[0]}]}'
cd /workspace/terraform && find . -name "*.tf" -type f | head -20
```

## Pulumi — answered

4 commands, from `pulumi-m2`.

```sh
cd /workspace/pulumi && ./pulumi-export | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn: .urn, id: .outputs.id, region: .outputs.availabilityZone}'
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | "\(.outputs.availabilityZone[0:-1])\t\(.outputs.id)\t\(.urn | split("::")[2])"' | sort
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {region: .outputs.availabilityZone[0:-1], instance_id: .outputs.id, resource_name: .outputs.tags.Name // (.urn | split("::")[-1])} | @tsv' | sort && echo "" && echo "Summary:" && cd /workspace/pulumi && ./pulumi-export | jq -r '[.deployment.resources[] | select(.type == "aws:ec2/instance:Instance")] | group_by(.outputs.availabilityZone[0:-1]) | map({region: .[0].outputs.availabilityZone[0:-1], count: length}) | .[] | "\(.region): \(.count) instances"' | sort
cd /workspace/pulumi && ./pulumi-export | jq -r '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | "\(.outputs.availabilityZone[0:-1]): \(.outputs.id) (\(.urn | split("::")[-1]))"' | sort
```

## AWS CDK — answered

8 commands, from `cdk-cur`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-QARoles-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, type: .value.Type, properties: .value.Properties}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, type: .value.Type}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, type: .value.Type}'
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {logicalId: .key, type: .value.Type}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 --region us-east-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {Region: "us-east-1", LogicalId: .LogicalResourceId, InstanceId: .PhysicalResourceId}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-1 --region us-west-1 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {Region: "us-west-1", LogicalId: .LogicalResourceId, InstanceId: .PhysicalResourceId}'
aws cloudformation describe-stack-resources --stack-name ec2-multiregion-EC2-ls9fuhb522-us-west-2 --region us-west-2 2>/dev/null | jq '.StackResources[] | select(.ResourceType == "AWS::EC2::Instance") | {Region: "us-west-2", LogicalId: .LogicalResourceId, InstanceId: .PhysicalResourceId}'
```
