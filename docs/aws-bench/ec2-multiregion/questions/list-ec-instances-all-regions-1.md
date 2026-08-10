# Which EC2 instances are reachable via SSH from the internet?

`list-ec-instances-all-regions-1` · the answer aws-bench grades against: **2 — one only through its launch template**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

3 commands, from `chant-i3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-east-1" --at latest --env floci --show InstanceId,PublicIpAddress,PrivateIpAddress,effectiveIngress,internetFacing --explain
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-west-1" --at latest --env floci --show InstanceId,PublicIpAddress,PrivateIpAddress,effectiveIngress,internetFacing --explain
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-west-2" --at latest --env floci --show InstanceId,PublicIpAddress,PrivateIpAddress,effectiveIngress,internetFacing --explain
```

## No tool (AWS CLI) — missed

14 commands, from `bare-i3`.

```sh
aws ec2 describe-instances --region us-east-1 --output json --query 'Reservations[].Instances[].{InstanceId:InstanceId,State:State.Name,PrivateIP:PrivateIpAddress,SecurityGroups:SecurityGroups[].GroupId,LaunchTemplate:LaunchTemplate}'
aws ec2 describe-instances --region us-west-1 --output json --query 'Reservations[].Instances[].{InstanceId:InstanceId,State:State.Name,PrivateIP:PrivateIpAddress,SecurityGroups:SecurityGroups[].GroupId,LaunchTemplate:LaunchTemplate}'
aws ec2 describe-instances --region us-west-2 --output json --query 'Reservations[].Instances[].{InstanceId:InstanceId,State:State.Name,PrivateIP:PrivateIpAddress,SecurityGroups:SecurityGroups[].GroupId,LaunchTemplate:LaunchTemplate}'
aws ec2 describe-security-groups --region us-east-1 --output json --query 'SecurityGroups[]' | jq '.[] | {GroupId:.GroupId, GroupName:.GroupName, IpPermissions:.IpPermissions[]}'
aws ec2 describe-security-groups --region us-west-1 --output json --query 'SecurityGroups[]' | jq '.[] | {GroupId:.GroupId, GroupName:.GroupName, IpPermissions:.IpPermissions[]}'
aws ec2 describe-security-groups --region us-west-2 --output json --query 'SecurityGroups[]' | jq '.[] | {GroupId:.GroupId, GroupName:.GroupName, IpPermissions:.IpPermissions[]}'
aws ec2 describe-security-groups --region us-east-1 --output json | jq '.SecurityGroups[] | select(.IpPermissions[]? | select(.FromPort == 22 or .FromPort == null)) | {GroupId, GroupName, IpPermissions: [.IpPermissions[] | select(.FromPort == 22 or .FromPort == null)]}'
aws ec2 describe-security-groups --region us-east-1 --output json | jq '.SecurityGroups[] | {GroupId, GroupName, IpPermissions}' | grep -A 50 "sg-default"
aws ec2 describe-security-groups --region us-west-1 --output json | jq '.SecurityGroups[] | {GroupId, GroupName, IpPermissions: [.IpPermissions[] | select(.FromPort == 22)]}'
aws ec2 describe-security-groups --region us-west-2 --output json | jq '.SecurityGroups[] | {GroupId, GroupName, IpPermissions: [.IpPermissions[] | select(.FromPort == 22)]}'
aws ec2 describe-instances --region us-east-1 --output json | jq '.Reservations[].Instances[] | {InstanceId, State: .State.Name, PrivateIP: .PrivateIpAddress, PublicIP: .PublicIpAddress, SecurityGroups: [.SecurityGroups[].GroupId], SubnetId}'
aws ec2 describe-instances --region us-west-1 --output json | jq '.Reservations[].Instances[] | {InstanceId, State: .State.Name, PrivateIP: .PrivateIpAddress, PublicIP: .PublicIpAddress, SecurityGroups: [.SecurityGroups[].GroupId], SubnetId}'
# … 2 more
```

## Terraform — answered

12 commands, from `terraform-i3`.

```sh
cd /workspace/terraform && ./terraform show -json | jq '.' | head -100
cd /workspace/terraform && ./terraform state list | grep -E 'aws_instance|aws_security_group|aws_launch_template'
cd /workspace/terraform && ./terraform show -json > /tmp/state.json && cat /tmp/state.json | jq '.values.root_module | walk(if type == "object" and .address then .address else . end) | .' > /tmp/filtered.json 2>&1 || true
cd /workspace/terraform && for instance in module.primary.aws_instance.default_vpc_server module.primary.aws_instance.launch_template_server module.primary.aws_instance.private_server module.primary.aws_instance.web_server module.west1.aws_instance.server module.west2.aws_instance.server; do echo "=== $instance ===" && ./terraform state show "$instance" 2>&1 | head -30; done
cd /workspace/terraform && for instance in module.primary.aws_instance.default_vpc_server module.primary.aws_instance.launch_template_server module.primary.aws_instance.private_server module.primary.aws_instance.web_server module.west1.aws_instance.server module.west2.aws_instance.server; do echo "=== $instance ===" && ./terraform state show "$instance" 2>&1 | grep -E 'vpc_security_group_ids|launch_template|security_groups'; done
cd /workspace/terraform && ./terraform show -json | jq '.values.root_module.resources[] | select(.type == "aws_instance") | {address, region: .values.availability_zone, vpc_security_group_ids: .values.vpc_security_group_ids, launch_template: .values.launch_template}'
cd /workspace/terraform && ./terraform show -json 2>&1 | jq '.values.root_module.resources[] | select(.type == "aws_instance")' | head -200
find /workspace/terraform/modules -type f -name "*.tf" | head -20
cd /workspace/terraform && cat terraform.tfstate | jq '.resources[] | select(.type == "aws_instance") | {address: .address, id: .instances[0].attributes.id, region: .instances[0].attributes.availability_zone, vpc_sg_ids: .instances[0].attributes.vpc_security_group_ids, launch_template: .instances[0].attributes.launch_template}' 2>/dev/null
cd /workspace/terraform && cat terraform.tfstate | jq '.resources[] | select(.type == "aws_security_group") | {address: .address, id: .instances[0].attributes.id, name: .instances[0].attributes.name, vpc_id: .instances[0].attributes.vpc_id, ingress: .instances[0].attributes.ingress}' 2>/dev/null
cd /workspace/terraform && cat terraform.tfstate | jq '.resources[] | select(.type == "aws_instance") | {name: .name, address: .address, id: .instances[0].attributes.id, region: .instances[0].attributes.availability_zone, vpc_sg_ids: .instances[0].attributes.vpc_security_group_ids}' 2>/dev/null
cat > /logs/agent/agent-output.txt << 'EOF' # EC2 Instances Reachable via SSH from the Internet ## Summary **2 EC2 instances** in your account can be reached via SSH from the internet (0.0.0.0/0). Both instances are in **us-east-1** and have: - Public subnet with internet gateway access - Security group "web" explicitly allowing SSH (port 22) from 0.0.0.0/0 --- ## Reachable Instances ### 1. web_server - **Instance ID**: i-095e44048f818a9e4 - **Region**: us-east-1 (availability zone: us-east-1a) - **Security Group**: sg-022d4d794a4101cde (web-ec2-multiregion-EC2-ks84v1fh12-us-east-1) - **Subnet**: Public (10.0.0.0/24) - **SSH Reachable**: ✓ YES - Security group allows inbound TCP port 22 from 0.0.0.0/0 - Instance is in public subnet with internet gateway route ### 2. launch_template_server - **Instance ID**: i-6fa3bd3c07634c798 - **Region**: us-east-1 (availability zone: us-east-1a) - **Security Group**: sg-022d4d794a4101cde (web-ec2-multiregion-EC2-ks84v1fh12-us-east-1) - **Subnet**: Public (10.0.0.0/24) - **Launch Template**: lt-*-us-east-1 (carries the web security group) - **SSH Reachable**: ✓ YES - Security group (from launch template) allows inbound TCP port 22 from 0.0.0.0/0 - Instance is in public subnet with internet gateway route --- ## Non-Reachable Instances ### us-east-1: - **private_server** (i-d8ef827f5dda6234c) - Region: us-east-1a - Security Group: sg-default (default VPC security group - no ingress rules) - Subnet: Private (10.0.1.0/24, no internet gateway route) - Why: Private subnet + default SG with no SSH rules - **default_vpc_server** (i-e82af08ce4d96ff71) - Region: us-east-1c - Security Group: sg-default (default VPC security group - no ingress rules) - Subnet: Default VPC (internet-facing but no SSH rule) - Why: Default security group has no ingress rules allowing port 22 ### us-west-1: - **server** (i-b5e9cf33ff57563a6) - Region: us-west-1a - Security Group: sg-default (default VPC security group - no ingress rules) - Subnet: Public (10.0.0.0/24) - Why: Default security group has no ingress rules allowing port 22 ### us-west-2: - **server** (i-8e35dce768d2d11f1) - Region: us-west-2a - Security Group: sg-default (default VPC security group - no ingress rules) - Subnet: Public (10.0.0.0/24) - Why: Default security group has no ingress rules allowing port 22 --- ## Security Group Configuration ### web (sg-022d4d794a4101cde) - **VPC**: Custom VPC (10.0.0.0/16) - **Ingress Rules**: - SSH: TCP port 22 from 0.0.0.0/0 ⚠️ - HTTP: TCP port 80 from 0.0.0.0/0 - HTTPS: TCP port 443 from 0.0.0.0/0 ### default (sg-default) - **Ingress Rules**: None (no explicit rules) - **Attached to**: default_vpc_server, private_server, west1 server, west2 server --- ## Source Analysis based on Terraform applied state (/workspace/terraform/terraform.tfstate). All instances in the specified regions (us-east-1, us-west-1, us-west-2) have been evaluated. EOF cat /logs/agent/agent-output.txt
```

## Pulumi — answered

11 commands, from `pulumi-i3`.

```sh
cd /workspace/pulumi && ./pulumi-export > /tmp/pulumi-state.json 2>&1 && echo "Export completed successfully" || echo "Export failed"
cd /workspace/pulumi && cat /tmp/pulumi-state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, outputs: {instance_id: .outputs.id, availability_zone: .outputs.availabilityZone, subnet_id: .outputs.subnetId, security_groups: .outputs.securityGroups, vpc_security_group_ids: .outputs.vpcSecurityGroupIds}, inputs: {security_groups: .inputs.securityGroups, vpc_security_group_ids: .inputs.vpcSecurityGroupIds, subnet_id: .inputs.subnetId}}' | head -200
cd /workspace/pulumi && cat /tmp/pulumi-state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/securityGroup:SecurityGroup") | {urn, sg_id: .outputs.id, sg_name: .outputs.name, ingress_rules: .outputs.ingress}'
cd /workspace/pulumi && cat /tmp/pulumi-state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/launchTemplate:LaunchTemplate") | {urn, template_name: .outputs.name, security_groups: .outputs.securityGroupNames, vpc_security_group_ids: .outputs.vpcSecurityGroupIds}'
cd /workspace/pulumi && cat /tmp/pulumi-state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn, launch_template: .outputs.launchTemplate}'
cd /workspace/pulumi && cat /tmp/pulumi-state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {name: .urn, launch_template_id: .inputs.launchTemplate}'
cd /workspace/pulumi && cat /tmp/pulumi-state.json | jq '.deployment.resources[] | select(.sg_id or .id | select(. == "sg-default" or startswith("sg-"))) | select(.type | contains("SecurityGroup")) | {urn, sg_id: .outputs.id, sg_name: .outputs.name, ingress_rules: .outputs.ingress}'
cd /workspace/pulumi && cat /tmp/pulumi-state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/securityGroup:SecurityGroup" or .type == "aws:ec2/defaultSecurityGroup:DefaultSecurityGroup") | {urn, outputs: {sg_id: .outputs.id, sg_name: .outputs.name, ingress_rules: .outputs.ingress}}'
cd /workspace/pulumi && cat /tmp/pulumi-state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {instance_name: (.urn | split("::")[3]), instance_id: .outputs.id, region: (.outputs.availabilityZone | .[:-1]), subnet_id: .outputs.subnetId, vpc_security_group_ids: .outputs.vpcSecurityGroupIds, launch_template: .inputs.launchTemplate}'
cd /workspace/pulumi && cat /tmp/pulumi-state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/subnet:Subnet") | {subnet_id: .outputs.id, cidr_block: .outputs.cidrBlock, vpc_id: .outputs.vpcId, map_public_ip_on_launch: .outputs.mapPublicIpOnLaunch}' | head -50
cd /workspace/pulumi && cat /tmp/pulumi-state.json | jq '.deployment.resources[] | select(.outputs.id == "sg-default") | {urn, type, ingress: .outputs.ingress}'
```

## AWS CDK — missed

16 commands, from `cdk-i1`.

```sh
cd /workspace/cdk_app && npx cdk ls
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-QARoles-us-east-1 --json 2>/dev/null | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null > /tmp/east1.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null > /tmp/west1.json
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null > /tmp/west2.json
cat /tmp/east1.json | jq '.Resources | keys[] | select(. | test("Instance|SecurityGroup"))' | head -20
cat /tmp/west1.json | jq '.Resources | keys[] | select(. | test("Instance|SecurityGroup"))' | head -20
cat /tmp/west2.json | jq '.Resources | keys[] | select(. | test("Instance|SecurityGroup"))' | head -20
cat > /tmp/analyze.sh << 'EOF' #!/bin/bash analyze_region() { local template_file=$1 local region=$2 echo "=== Region: $region ===" # Extract all EC2 instances local instances=$(jq -r '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | .key' "$template_file") if [ -z "$instances" ]; then echo "No EC2 instances found" return fi for instance in $instances; do echo "" echo "Instance: $instance" # Get instance details local instance_json=$(jq ".Resources[\"$instance\"]" "$template_file") # Get security groups directly attached local direct_sgs=$(echo "$instance_json" | jq -r '.Properties.SecurityGroupIds[]? // .Properties.SecurityGroups[]?' 2>/dev/null | tr '\n' ' ') # Get launch template if exists local launch_template=$(echo "$instance_json" | jq -r '.Properties.LaunchTemplate // .Properties.LaunchTemplateId // empty' "$template_file" 2>/dev/null) if [ -n "$launch_template" ]; then # If it's a ref, resolve it if echo "$launch_template" | grep -q "Ref"; then local lt_logical_id=$(echo "$launch_template" | jq -r '.Ref' 2>/dev/null) # Get the launch template's security groups local lt_json=$(jq ".Resources[\"$lt_logical_id\"]" "$template_file" 2>/dev/null) local lt_sgs=$(echo "$lt_json" | jq -r '.Properties.LaunchTemplateData.SecurityGroupIds[]? // .Properties.LaunchTemplateData.SecurityGroups[]?' 2>/dev/null | tr '\n' ' ') echo " Launch Template: $lt_logical_id" if [ -n "$lt_sgs" ]; then echo " Security Groups from LT: $lt_sgs" fi fi fi if [ -n "$direct_sgs" ]; then echo " Direct Security Groups: $direct_sgs" fi # Get all security groups (resolve refs) echo " Security Group Details:" # Combine direct SGs and LT SGs local all_sg_refs=$(echo "$instance_json" | jq -r '.Properties.SecurityGroupIds[]? // .Properties.SecurityGroups[]? // empty' 2>/dev/null) if [ -z "$all_sg_refs" ]; then # Try from launch template local lt_logical_id=$(echo "$instance_json" | jq -r '.Properties.LaunchTemplate.Ref // .Properties.LaunchTemplateId // empty' 2>/dev/null) if [ -n "$lt_logical_id" ] && [ "$lt_logical_id" != "null" ]; then local lt_json=$(jq ".Resources[\"$lt_logical_id\"]" "$template_file" 2>/dev/null) all_sg_refs=$(echo "$lt_json" | jq -r '.Properties.LaunchTemplateData.SecurityGroupIds[]? // empty' 2>/dev/null) fi fi # Check each security group for SSH access from internet if [ -n "$all_sg_refs" ]; then for sg_ref in $all_sg_refs; do # Handle Ref() format if [[ "$sg_ref" == *"Ref"* ]]; then sg_logical_id=$(echo "$sg_ref" | jq -r '.Ref' 2>/dev/null) else sg_logical_id="$sg_ref" fi if [ -n "$sg_logical_id" ] && [ "$sg_logical_id" != "null" ]; then check_sg_for_ssh "$template_file" "$sg_logical_id" fi done fi done echo "" } check_sg_for_ssh() { local template_file=$1 local sg_logical_id=$2 local sg_json=$(jq ".Resources[\"$sg_logical_id\"]" "$template_file" 2>/dev/null) if [ "$sg_json" == "null" ] || [ -z "$sg_json" ]; then return fi # Check for SSH rules (port 22) local ssh_rules=$(echo "$sg_json" | jq '.Properties.SecurityGroupIngress[]? | select(.FromPort == 22 or .IpProtocol == "-1")' 2>/dev/null) if [ -n "$ssh_rules" ]; then local has_internet_ssh=$(echo "$sg_json" | jq '.Properties.SecurityGroupIngress[]? | select((.FromPort == 22 or .IpProtocol == "-1") and (.CidrIp == "0.0.0.0/0" or .CidrIpv6 == "::/0"))' 2>/dev/null) if [ -n "$has_internet_ssh" ]; then echo " ✓ $sg_logical_id ALLOWS SSH from internet (0.0.0.0/0)" echo "$has_internet_ssh" | jq '.' 2>/dev/null fi fi } analyze_region /tmp/east1.json "us-east-1" analyze_region /tmp/west1.json "us-west-1" analyze_region /tmp/west2.json "us-west-2" EOF chmod +x /tmp/analyze.sh /tmp/analyze.sh
# … 4 more
```

## Alchemy — answered

26 commands, from `alchemy-i3`.

```sh
cd /workspace/alchemy && alchemy state list | grep -i instance
cd /workspace/alchemy && alchemy state list
cd /workspace/alchemy && for resource in instance defaultVpcServer ltServer privateServer usw1-server usw2-server webServer web-ssh; do echo "=== $resource ===" alchemy state get "alchemy-ec2-multiregion/bench/$resource" 2>/dev/null | jq '.kind, .output | {region, instance_id: .id, security_groups, launch_template}' done
cd /workspace/alchemy && alchemy state get "alchemy-ec2-multiregion/bench/instance" | head -50
cd /workspace/alchemy && alchemy state get "alchemy-ec2-multiregion/bench/webServer" 2>&1 | jq '.kind'
cd /workspace/alchemy && alchemy state list | xargs -I {} bash -c 'alchemy state get "{}" 2>/dev/null | jq -r "select(.kind == \"AWS::EC2::Instance\") | .fqn" 2>/dev/null' | sort
cd /workspace/alchemy && for inst in defaultVpcServer ltServer privateServer usw1-server usw2-server webServer; do alchemy state get "alchemy-ec2-multiregion/bench/$inst" 2>/dev/null | jq '{name: .id, region: .output.region, instance_id: .output.instanceId, security_groups: .output.securityGroups, launch_template: .output.launchTemplate}' done
cd /workspace/alchemy && alchemy state get "alchemy-ec2-multiregion/bench/webServer" | jq '.output | keys' | head -30
cd /workspace/alchemy && for inst in defaultVpcServer ltServer privateServer usw1-server usw2-server webServer; do alchemy state get "alchemy-ec2-multiregion/bench/$inst" 2>/dev/null | jq '{name: .id, region: .output.region, instance_id: .output.InstanceId, security_group_ids: .output.SecurityGroupIds}' done
cd /workspace/alchemy && alchemy state list | xargs -I {} bash -c 'alchemy state get "{}" 2>/dev/null | jq -r "select(.kind == \"AWS::EC2::SecurityGroup\" or .kind == \"AWS::EC2::SecurityGroupIngress\") | .fqn" 2>/dev/null' | sort
cd /workspace/alchemy && alchemy state list | xargs -I {} bash -c 'alchemy state get "{}" 2>/dev/null | jq -r ".kind" 2>/dev/null' | sort | uniq
cd /workspace/alchemy && alchemy state list | xargs -I {} bash -c 'alchemy state get "{}" 2>/dev/null | jq -r "select(.kind == \"aws::SecurityGroup\" or .kind == \"aws::SecurityGroupRule\") | .fqn" 2>/dev/null'
# … 14 more
```

## Alchemy v2 (Effect) — answered

11 commands, from `alchemy-effect-i3`.

```sh
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local 2>&1 | head -100
cd /workspace/alchemy && alchemy state export us-west-1.run.ts --local > /tmp/alchemy-state.json 2>&1
cd /workspace/alchemy && cat /tmp/alchemy-state.json | jq '.resources[] | select(.state.resourceType == "AWS.EC2.Instance") | {fqn: .fqn, stack: .stack, instanceId: .state.attr.instanceId, instanceType: .state.attr.instanceType, publicIp: .state.attr.publicIpAddress, securityGroupIds: .state.attr.securityGroupIds, launchTemplate: .state.props.launchTemplate}'
cd /workspace/alchemy && cat /tmp/alchemy-state.json | jq '.resources[] | select(.state.resourceType == "AWS.EC2.SecurityGroup") | {fqn: .fqn, stack: .stack, groupId: .state.attr.groupId, groupName: .state.attr.groupName, ingressRules: .state.attr.ingressRules}'
cd /workspace/alchemy && cat /tmp/alchemy-state.json | jq '.resources[] | select(.state.resourceType == "AWS.EC2.SecurityGroup" and .state.attr.groupId == "sg-default") | {fqn: .fqn, stack: .stack, groupId: .state.attr.groupId, groupName: .state.attr.groupName, ingressRules: .state.attr.ingressRules}'
cd /workspace/alchemy && cat /tmp/alchemy-state.json | jq '.resources[] | select(.state.resourceType == "AWS.EC2.SecurityGroup") | .state.attr.groupId'
cd /workspace/alchemy && cat /tmp/alchemy-state.json | jq '.resources[] | select(.state.resourceType == "AWS.EC2.SecurityGroup" or .state.resourceType == "AWS.EC2.Instance") | {type: .state.resourceType, fqn: .fqn, stack: .stack, id: (if .state.resourceType == "AWS.EC2.SecurityGroup" then .state.attr.groupId else .state.attr.instanceId end), name: (if .state.resourceType == "AWS.EC2.SecurityGroup" then .state.attr.groupName else .state.props.tags.Name end)}' | head -50
cd /workspace/alchemy && cat /tmp/alchemy-state.json | jq '.resources[] | select(.state.resourceType == "AWS.EC2.LaunchTemplate") | {fqn: .fqn, stack: .stack, launchTemplateId: .state.attr.launchTemplateId, securityGroupIds: .state.attr.securityGroupIds}'
cd /workspace/alchemy && cat /tmp/alchemy-state.json | jq '.resources[] | select(.fqn == "LaunchTemplateServer")'
cd /workspace/alchemy && cat /tmp/alchemy-state.json | jq '.resources[] | select(.state.resourceType == "AWS.AutoScaling.LaunchTemplate")'
cat > /logs/agent/agent-output.txt << 'EOF' EC2 INSTANCES REACHABLE VIA SSH FROM THE INTERNET ================================================== Analysis of AWS estate across us-east-1, us-west-1, and us-west-2: FINDINGS: --------- Two EC2 instances are reachable via SSH from the internet: 1. WebServer (us-east-1) - Instance ID: i-a99e3ced39782a9b7 - Public IP: 54.144.97.57 - Security Group: sg-e96a3de38f47ffd0a (WebSecurityGroup) - SSH Access: Allowed from 0.0.0.0/0 (port 22) - Reason: WebSecurityGroup explicitly allows SSH from internet 2. LaunchTemplateServer (us-east-1) - Instance ID: i-d23304a8c14237368 - Public IP: 54.144.56.135 - Security Group: sg-e96a3de38f47ffd0a (via launch template) - SSH Access: Allowed from 0.0.0.0/0 (port 22) - Reason: Launch template specifies WebSecurityGroup with SSH from internet INSTANCES NOT SSH-REACHABLE FROM INTERNET: ------------------------------------------- 1. DefaultVpcServer (us-east-1) - Instance ID: i-3083b183007a76750 - Public IP: 54.144.131.18 - Security Group: sg-default (AWS default VPC security group) - SSH Access: NOT allowed from internet - Reason: Default security group only allows traffic within VPC 2. PrivateServer (us-east-1) - Instance ID: i-382f0ba0f1fe8b0d1 - Public IP: None (private subnet, no public IP) - Security Group: sg-default - SSH Access: NOT reachable from internet - Reason: No public IP address 3. WebServer (us-west-1) - Instance ID: i-c19938fde4d3088ab - Public IP: 54.144.30.68 - Security Group: sg-default - SSH Access: NOT allowed from internet - Reason: Default security group does not allow internet SSH 4. WebServer (us-west-2) - Instance ID: i-3e4d5fe856efabc43 - Public IP: 54.144.53.91 - Security Group: sg-default - SSH Access: NOT allowed from internet - Reason: Default security group does not allow internet SSH SUMMARY: -------- Total instances: 6 SSH-reachable from internet: 2 EOF cat /logs/agent/agent-output.txt
```
