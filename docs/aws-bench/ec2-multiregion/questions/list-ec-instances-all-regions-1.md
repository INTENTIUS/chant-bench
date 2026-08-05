# Which EC2 instances are reachable via SSH from the internet?

`list-ec-instances-all-regions-1` · the answer aws-bench grades against: **2 — one only through its launch template**

Below is what each tool's agent actually ran. The scores say which tools
answered. This says how, and the how is where they differ most.

## chant — answered

4 commands, from `chant-h3`.

```sh
cd /workspace/chant && chant search "kind:EC2::Instance attr:region=us-east-1 attr:region=us-west-1 attr:region=us-west-2" --at latest --env floci --show PrivateIpAddress,State,SubnetId
cd /workspace/chant && chant lifecycle show floci 2>&1 | grep -E "^(EC2::Instance|EC2::SecurityGroup|EC2::SecurityGroupIngress)" | head -20
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show PrivateIpAddress,State,SubnetId,PublicIpAddress,internetFacing,effectiveIngress --explain
cd /workspace/chant && chant search "kind:EC2::Instance" --at latest --env floci --show region,PrivateIpAddress,PublicIpAddress,internetFacing,effectiveIngress
```

## No tool (AWS CLI) — missed

10 commands, from `bare-h3`.

```sh
aws ec2 describe-instances --region us-east-1 --output json | jq '.Reservations[].Instances[] | {InstanceId, State: .State.Name, PublicIpAddress, SecurityGroups: .SecurityGroups, LaunchTemplate}'
aws ec2 describe-instances --region us-west-1 --output json | jq '.Reservations[].Instances[] | {InstanceId, State: .State.Name, PublicIpAddress, SecurityGroups: .SecurityGroups, LaunchTemplate}'
aws ec2 describe-instances --region us-west-2 --output json | jq '.Reservations[].Instances[] | {InstanceId, State: .State.Name, PublicIpAddress, SecurityGroups: .SecurityGroups, LaunchTemplate}'
aws ec2 describe-security-groups --region us-east-1 --output json | jq '.SecurityGroups[] | {GroupId, GroupName, IpPermissions: .IpPermissions}'
aws ec2 describe-security-groups --region us-west-1 --output json | jq '.SecurityGroups[] | {GroupId, GroupName, IpPermissions: .IpPermissions}'
aws ec2 describe-security-groups --region us-west-2 --output json | jq '.SecurityGroups[] | {GroupId, GroupName, IpPermissions: .IpPermissions}'
aws ec2 describe-instances --region us-east-1 --output json --query 'Reservations[].Instances[].[InstanceId,State.Name,PublicIpAddress,SecurityGroups[].GroupId,LaunchTemplate]' | jq -r '.[] | "\(.InstanceId) | \(.State) | \(.PublicIpAddress) | \(.SecurityGroups) | \(.LaunchTemplate)"'
aws ec2 describe-instances --region us-east-1 --output json | jq '.Reservations[].Instances[] | {InstanceId, PublicIp: .PublicIpAddress, State: .State.Name, SecurityGroupIds: [.SecurityGroups[].GroupId], LaunchTemplate}'
aws ec2 describe-instances --region us-west-1 --output json | jq '.Reservations[].Instances[] | {InstanceId, PublicIp: .PublicIpAddress, State: .State.Name, SecurityGroupIds: [.SecurityGroups[].GroupId], LaunchTemplate}'
aws ec2 describe-instances --region us-west-2 --output json | jq '.Reservations[].Instances[] | {InstanceId, PublicIp: .PublicIpAddress, State: .State.Name, SecurityGroupIds: [.SecurityGroups[].GroupId], LaunchTemplate}'
```

## Terraform — answered

14 commands, from `terraform-h3`.

```sh
cd /workspace/terraform && ./terraform show -json | jq '.' > /tmp/terraform_state.json && echo "State loaded successfully"
cd /workspace/terraform && jq '.values.root_module.resources[] | select(.type == "aws_instance") | {address: .address, values: {instance_id: .values.id, availability_zone: .values.availability_zone, security_groups: .values.security_groups, vpc_security_group_ids: .values.vpc_security_group_ids, launch_template: .values.launch_template}}' /tmp/terraform_state.json
cd /workspace/terraform && ./terraform state list | grep aws_instance
cd /workspace/terraform && for instance in "module.primary.aws_instance.default_vpc_server" "module.primary.aws_instance.launch_template_server" "module.primary.aws_instance.private_server" "module.primary.aws_instance.web_server" "module.west1.aws_instance.server" "module.west2.aws_instance.server"; do echo "=== $instance ===" ./terraform state show "$instance" | grep -E "id|availability_zone|security_groups|vpc_security_group_ids|launch_template" done
cd /workspace/terraform && jq '.values.root_module | [.resources[], .child_modules[].resources[]] | map(select(.type == "aws_instance") | {name: .address, instance_id: .values.id, region: .values.availability_zone | .[0:-1], vpc_security_group_ids: .values.vpc_security_group_ids, launch_template: .values.launch_template})' /tmp/terraform_state.json
cd /workspace/terraform && jq '.values.root_module | [.resources[], .child_modules[].resources[]] | map(select(.type == "aws_security_group" or .type == "aws_security_group_rule") | {type: .type, name: .address, id: .values.id, group_id: .values.group_id, from_port: .values.from_port, to_port: .values.to_port, protocol: .values.protocol, cidr_blocks: .values.cidr_blocks, ipv6_cidr_blocks: .values.ipv6_cidr_blocks})' /tmp/terraform_state.json | jq '.'
cd /workspace/terraform && ./terraform state show module.primary.aws_security_group.web
cd /workspace/terraform && ./terraform state show module.primary.aws_security_group.unused
cd /workspace/terraform && ./terraform state list | grep -i "security_group\|sg-"
cd /workspace/terraform && grep -r "sg-default" --include="*.tf" .
cd /workspace/terraform && ./terraform state list | grep "data_source\|aws_security_group_rule\|default"
cd /workspace/terraform && ./terraform state show 'module.primary.data.aws_vpc.default'
# … 2 more
```

## Pulumi — answered

7 commands, from `pulumi-h3`.

```sh
cd /workspace/pulumi && ./pulumi-export > /tmp/state.json && cat /tmp/state.json | jq '.' | head -100
cd /workspace/pulumi && cat /tmp/state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance" or .type == "aws:ec2/securityGroup:SecurityGroup" or .type == "aws:ec2/launchTemplate:LaunchTemplate") | {type, urn, outputs}' 2>/dev/null | head -300
cd /workspace/pulumi && cat /tmp/state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/instance:Instance") | {urn, region: (.outputs.availabilityZone | split("-")[0:-1] | join("-")), id: .outputs.id, publicIp: .outputs.publicIp, securityGroups: .outputs.vpcSecurityGroupIds, launchTemplate: .outputs.launchTemplate, tags: .outputs.tags}' 2>/dev/null
cd /workspace/pulumi && cat /tmp/state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/securityGroup:SecurityGroup") | {urn, id: .outputs.id, ingress: .outputs.ingress}' 2>/dev/null
cd /workspace/pulumi && cat /tmp/state.json | jq '.deployment.resources[] | select(.type == "aws:ec2/launchTemplate:LaunchTemplate") | {urn, id: .outputs.id, vpcSecurityGroupIds: .outputs.vpcSecurityGroupIds}' 2>/dev/null
cd /workspace/pulumi && cat /tmp/state.json | jq '.deployment.resources[] | select(.outputs.id == "sg-default") | {id: .outputs.id, ingress: .outputs.ingress, description: .outputs.description}' 2>/dev/null
cat > /logs/agent/agent-output.txt << 'EOF' # EC2 Instances Reachable via SSH from the Internet ## Summary Based on analysis of the Pulumi state, **2 EC2 instances** in your account are reachable via SSH from the internet: 1. **webServer** (i-89c4532190f0f7108) - Region: us-east-1 - Public IP: 54.144.180.174 - Security Group: sg-7661567701a7a8e78 (web) - Subnet: Public (10.0.0.0/24) - SSH Access: Allowed from 0.0.0.0/0 on port 22 2. **ltServer** (i-c54ab5b597f3a4356) - Region: us-east-1 - Public IP: 54.144.237.47 - Security Group: sg-7661567701a7a8e78 (web, via launch template) - Subnet: Public (10.0.0.0/24) - SSH Access: Allowed from 0.0.0.0/0 on port 22 ## Analysis Details ### Instances NOT Reachable via SSH from Internet: - **defaultVpcServer** (i-438371dd30873e1f7) - us-east-1 - Uses default VPC security group (sg-default) - Default SG does not allow SSH from 0.0.0.0/0 - Public IP: 54.144.156.159 - **privateServer** (i-4da5ba4e99a496207) - us-east-1 - In private subnet (10.0.1.0/24, no IGW route) - No public IP assigned - Uses default security group - **usw1-server** (i-9c5b7c544a8bb8588) - us-west-1 - Uses default VPC security group - Public IP: 54.144.2.138, but SSH not allowed from internet - Code comment: "internet-facing but not SSH-reachable" - **usw2-server** (i-ecdd069aef7173854) - us-west-2 - Uses default VPC security group - Public IP: 54.144.208.253, but SSH not allowed from internet - Code comment: "internet-facing but not SSH-reachable" ### Key Finding: The "web" security group (sg-7661567701a7a8e78) is the only managed security group that explicitly allows SSH (port 22) from 0.0.0.0/0. Only two instances use this group: - webServer (directly) - ltServer (via launch template) Both have public IPs and are in the public subnet of us-east-1. EOF cat /logs/agent/agent-output.txt
```

## AWS CDK — answered

25 commands, from `cdk-h3`.

```sh
cd /workspace/cdk_app && npx cdk ls 2>/dev/null
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-QARoles-us-east-1 --json 2>/dev/null | jq -r '.Resources | keys[]' | head -20
cd /workspace/cdk_app && for stack in ec2-multiregion-EC2-ks84v1fh12-us-east-1 ec2-multiregion-EC2-ls9fuhb522-us-west-1 ec2-multiregion-EC2-ls9fuhb522-us-west-2; do echo "=== Stack: $stack ==="; npx cdk synth "$stack" --json 2>/dev/null | jq '.Resources | to_entries[] | select(.value.Type | test("EC2::Instance|EC2::SecurityGroup|EC2::LaunchTemplate")) | .key'; done
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null | jq ' .Resources | to_entries[] | select(.value.Type == "AWS::EC2::SecurityGroupIngress" or .value.Type == "AWS::EC2::SecurityGroup") | { LogicalId: .key, Type: .value.Type, GroupId: .value.Properties.GroupId // .value.Properties.GroupId, SecurityGroupIngress: .value.Properties.SecurityGroupIngress, SourceSecurityGroupId: (.value.Properties.SecurityGroupIngress[]?.SourceSecurityGroupId // "N/A"), IpProtocol: (.value.Properties.SecurityGroupIngress[]?.IpProtocol // "N/A"), FromPort: (.value.Properties.SecurityGroupIngress[]?.FromPort // "N/A"), ToPort: (.value.Properties.SecurityGroupIngress[]?.ToPort // "N/A"), CidrIp: (.value.Properties.SecurityGroupIngress[]?.CidrIp // "N/A") } ' | head -100
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ks84v1fh12-us-east-1 --json 2>/dev/null > /tmp/us_east_1_template.json
cat > /tmp/analyze_ssh.py << 'EOF' import json import sys def analyze_stack(template_file, stack_name, region): with open(template_file) as f: template = json.load(f) resources = template.get('Resources', {}) # Find all security groups and check for SSH ingress from internet ssh_accessible_sgs = {} for logical_id, resource in resources.items(): if resource.get('Type') == 'AWS::EC2::SecurityGroup': ingress_rules = resource.get('Properties', {}).get('SecurityGroupIngress', []) for rule in ingress_rules: from_port = rule.get('FromPort') to_port = rule.get('ToPort') cidr_ip = rule.get('CidrIp', '') ip_protocol = rule.get('IpProtocol', '') # Check if SSH (port 22) from internet (0.0.0.0/0) if cidr_ip == '0.0.0.0/0' and (from_port == 22 or (from_port is None and to_port is None and ip_protocol == '-1')): ssh_accessible_sgs[logical_id] = { 'FromPort': from_port, 'ToPort': to_port, 'Rule': rule } # Find instances and their security groups instances_by_sg = {} instances_by_template = {} for logical_id, resource in resources.items(): if resource.get('Type') == 'AWS::EC2::Instance': props = resource.get('Properties', {}) # Direct security groups security_groups = props.get('SecurityGroupIds', []) or props.get('SecurityGroups', []) # Security groups from launch template lt_id = props.get('LaunchTemplate', {}).get('LaunchTemplateId') lt_name = props.get('LaunchTemplate', {}).get('LaunchTemplateName') instances_by_sg[logical_id] = { 'SecurityGroups': security_groups, 'LaunchTemplate': lt_id or lt_name, 'InstanceType': props.get('InstanceType'), 'ImageId': props.get('ImageId') } # Check launch templates for security groups for logical_id, resource in resources.items(): if resource.get('Type') == 'AWS::EC2::LaunchTemplate': props = resource.get('Properties', {}).get('LaunchTemplateData', {}) sgs = props.get('SecurityGroupIds', []) or props.get('SecurityGroups', []) instances_by_template[logical_id] = sgs # Find instances reachable via SSH ssh_reachable_instances = [] for inst_logical_id, inst_props in instances_by_sg.items(): all_sgs = inst_props.get('SecurityGroups', []).copy() # Add SGs from launch template if referenced lt_ref = inst_props.get('LaunchTemplate') if lt_ref: # Try to find the launch template for lt_logical_id, lt_sgs in instances_by_template.items(): if lt_logical_id == lt_ref or lt_logical_id.startswith(lt_ref): all_sgs.extend(lt_sgs) # Check if any of the instance's SGs allow SSH from internet for sg in all_sgs: if sg in ssh_accessible_sgs: ssh_reachable_instances.append({ 'InstanceLogicalId': inst_logical_id, 'SecurityGroups': all_sgs, 'LaunchTemplate': inst_props.get('LaunchTemplate'), 'SSHAccessibleVia': sg }) break return { 'StackName': stack_name, 'Region': region, 'SSHAccessibleSGs': ssh_accessible_sgs, 'SSHReachableInstances': ssh_reachable_instances, 'AllInstances': instances_by_sg } result = analyze_stack(sys.argv[1], sys.argv[2], sys.argv[3]) print(json.dumps(result, indent=2)) EOF python3 /tmp/analyze_ssh.py /tmp/us_east_1_template.json "ec2-multiregion-EC2-ks84v1fh12-us-east-1" "us-east-1"
cat /tmp/us_east_1_template.json | jq '.Resources | to_entries[] | select(.value.Type == "AWS::EC2::Instance") | {LogicalId: .key, Props: .value.Properties | {SecurityGroupIds, SecurityGroups, LaunchTemplate}} | .[0:2]'
cat /tmp/us_east_1_template.json | jq '.Resources.WebServerInstance8A1D687E.Properties | {SecurityGroupIds, LaunchTemplate}'
cat > /tmp/analyze_ssh2.py << 'EOF' import json import sys def resolve_reference(ref, resources): """Resolve CloudFormation references to get logical IDs""" if isinstance(ref, dict): if 'Fn::GetAtt' in ref: # Returns the logical ID being referenced return ref['Fn::GetAtt'][0] elif 'Ref' in ref: return ref['Ref'] return ref def analyze_stack(template_file, stack_name, region): with open(template_file) as f: template = json.load(f) resources = template.get('Resources', {}) # Map logical IDs to security group info sg_info = {} for logical_id, resource in resources.items(): if resource.get('Type') == 'AWS::EC2::SecurityGroup': ingress_rules = resource.get('Properties', {}).get('SecurityGroupIngress', []) sg_info[logical_id] = { 'Ingress': ingress_rules, 'HasSSHFromInternet': False } # Check for SSH from internet for rule in ingress_rules: cidr_ip = rule.get('CidrIp', '') from_port = rule.get('FromPort') to_port = rule.get('ToPort') if cidr_ip == '0.0.0.0/0' and from_port == 22: sg_info[logical_id]['HasSSHFromInternet'] = True # Find instances and check if they can be reached via SSH ssh_reachable = [] for logical_id, resource in resources.items(): if resource.get('Type') == 'AWS::EC2::Instance': props = resource.get('Properties', {}) # Get security groups (resolve references) sg_ids = props.get('SecurityGroupIds', []) sg_logical_ids = [resolve_reference(sg, resources) for sg in sg_ids] # Check launch template for additional security groups lt_ref = props.get('LaunchTemplate', {}) if lt_ref: lt_name = lt_ref.get('LaunchTemplateName', '') # Find launch template by name for lt_logical_id, lt_resource in resources.items(): if lt_resource.get('Type') == 'AWS::EC2::LaunchTemplate': if lt_logical_id.startswith(lt_name): lt_data = lt_resource.get('Properties', {}).get('LaunchTemplateData', {}) lt_sg_ids = lt_data.get('SecurityGroupIds', []) or lt_data.get('SecurityGroups', []) lt_sg_logical_ids = [resolve_reference(sg, resources) for sg in lt_sg_ids] sg_logical_ids.extend(lt_sg_logical_ids) # Check if any of these SGs allow SSH from internet for sg_logical_id in sg_logical_ids: if sg_logical_id in sg_info and sg_info[sg_logical_id].get('HasSSHFromInternet'): ssh_reachable.append({ 'InstanceLogicalId': logical_id, 'SSHAccessibleVia_SG': sg_logical_id }) break return { 'StackName': stack_name, 'Region': region, 'SSHAccessibleSGs': {k: v for k, v in sg_info.items() if v['HasSSHFromInternet']}, 'SSHReachableInstances': ssh_reachable } result = analyze_stack(sys.argv[1], sys.argv[2], sys.argv[3]) print(json.dumps(result, indent=2)) EOF python3 /tmp/analyze_ssh2.py /tmp/us_east_1_template.json "ec2-multiregion-EC2-ks84v1fh12-us-east-1" "us-east-1"
cd /workspace/cdk_app && npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-1 --json 2>/dev/null > /tmp/us_west_1_template.json && \ npx cdk synth ec2-multiregion-EC2-ls9fuhb522-us-west-2 --json 2>/dev/null > /tmp/us_west_2_template.json
cat > /tmp/analyze_all.py << 'EOF' import json def resolve_reference(ref, resources): """Resolve CloudFormation references to get logical IDs""" if isinstance(ref, dict): if 'Fn::GetAtt' in ref: return ref['Fn::GetAtt'][0] elif 'Ref' in ref: return ref['Ref'] return ref def analyze_stack(template_file, stack_name, region): with open(template_file) as f: template = json.load(f) resources = template.get('Resources', {}) # Map logical IDs to security group info sg_info = {} for logical_id, resource in resources.items(): if resource.get('Type') == 'AWS::EC2::SecurityGroup': ingress_rules = resource.get('Properties', {}).get('SecurityGroupIngress', []) sg_info[logical_id] = { 'Ingress': ingress_rules, 'HasSSHFromInternet': False } # Check for SSH from internet for rule in ingress_rules: cidr_ip = rule.get('CidrIp', '') from_port = rule.get('FromPort') to_port = rule.get('ToPort') if cidr_ip == '0.0.0.0/0' and from_port == 22: sg_info[logical_id]['HasSSHFromInternet'] = True # Find instances and check if they can be reached via SSH ssh_reachable = [] all_instances = {} for logical_id, resource in resources.items(): if resource.get('Type') == 'AWS::EC2::Instance': props = resource.get('Properties', {}) # Get security groups (resolve references) sg_ids = props.get('SecurityGroupIds', []) sg_logical_ids = [resolve_reference(sg, resources) for sg in sg_ids] all_instances[logical_id] = { 'SecurityGroups': sg_logical_ids, 'ImageId': props.get('ImageId'), 'InstanceType': props.get('InstanceType'), 'SSHAccessible': False } # Check launch template for additional security groups lt_ref = props.get('LaunchTemplate', {}) if lt_ref: lt_name = lt_ref.get('LaunchTemplateName', '') for lt_logical_id, lt_resource in resources.items(): if lt_resource.get('Type') == 'AWS::EC2::LaunchTemplate': if lt_logical_id.startswith(lt_name): lt_data = lt_resource.get('Properties', {}).get('LaunchTemplateData', {}) lt_sg_ids = lt_data.get('SecurityGroupIds', []) or lt_data.get('SecurityGroups', []) lt_sg_logical_ids = [resolve_reference(sg, resources) for sg in lt_sg_ids] sg_logical_ids.extend(lt_sg_logical_ids) # Check if any of these SGs allow SSH from internet for sg_logical_id in sg_logical_ids: if sg_logical_id in sg_info and sg_info[sg_logical_id].get('HasSSHFromInternet'): ssh_reachable.append({ 'InstanceLogicalId': logical_id, 'SSHAccessibleVia_SG': sg_logical_id }) all_instances[logical_id]['SSHAccessible'] = True break return { 'StackName': stack_name, 'Region': region, 'SSHAccessibleSGs': {k: v for k, v in sg_info.items() if v['HasSSHFromInternet']}, 'SSHReachableInstances': ssh_reachable, 'AllInstances': all_instances } # Analyze all stacks results = [] results.append(analyze_stack('/tmp/us_east_1_template.json', 'ec2-multiregion-EC2-ks84v1fh12-us-east-1', 'us-east-1')) results.append(analyze_stack('/tmp/us_west_1_template.json', 'ec2-multiregion-EC2-ls9fuhb522-us-west-1', 'us-west-1')) results.append(analyze_stack('/tmp/us_west_2_template.json', 'ec2-multiregion-EC2-ls9fuhb522-us-west-2', 'us-west-2')) print(json.dumps(results, indent=2)) EOF python3 /tmp/analyze_all.py
for region in us-east-1; do echo "=== Stack: ec2-multiregion-EC2-ks84v1fh12-us-east-1 (Region: $region) ===" aws cloudformation describe-stack-resources \ --stack-name ec2-multiregion-EC2-ks84v1fh12-us-east-1 \ --region $region \ --query 'StackResources[?LogicalResourceId==`WebServerInstance8A1D687E` || LogicalResourceId==`LaunchTemplateInstance`].[LogicalResourceId,PhysicalResourceId,ResourceType]' \ --output table done
# … 13 more
```

## Alchemy — answered

19 commands, from `alchemy-h3`.

```sh
cd /workspace/alchemy && alchemy state list | head -20
cd /workspace/alchemy && alchemy state list | grep -i instance
cd /workspace/alchemy && alchemy state list | grep -i security
cd /workspace/alchemy && alchemy state get "alchemy-ec2-multiregion/bench/instance" 2>/dev/null | jq '.'
cd /workspace/alchemy && alchemy state list | grep -E "(exp-InstanceId|exp-LaunchTemplateInstanceId|exp-PrivateInstanceId|exp-DefaultVPCInstanceId|usw1-exp-InstanceId|usw2-exp-InstanceId)" | head -20
find /workspace/alchemy/.alchemy -name "*.json" -type f | head -20
find /workspace/alchemy/.alchemy -name "*.json" -type f | xargs grep -l '"kind".*Instance' | head -20
cd /workspace/alchemy && for file in webServer privateServer usw2-server usw1-server defaultVpcServer ltServer; do echo "=== $file ==="; cat .alchemy/alchemy-ec2-multiregion/bench/$file.json | jq '{kind, id, output: {instanceId: .output.instanceId, region: .output.region, publicIp: .output.publicIp, securityGroupIds: .output.securityGroupIds, launchTemplate: .output.launchTemplate}}'; done
find /workspace/alchemy/.alchemy -name "*.json" -type f | xargs grep -l '"kind".*SecurityGroup' | head -20
find /workspace/alchemy/.alchemy -name "*.json" -type f | xargs grep -l '"kind".*SecurityGroupIngress\|SecurityGroupRule' | head -20
find /workspace/alchemy/.alchemy -name "*.json" -type f | xargs grep -l '"kind".*Address\|ElasticIp' | head -20
find /workspace/alchemy/.alchemy -name "*.json" -type f | xargs grep -l '"kind".*Subnet' | head -20
# … 7 more
```

## Alchemy v2 (Effect) — answered

18 commands, from `alchemy-effect-h3`.

```sh
cd /workspace/alchemy && alchemy state stacks us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-east-1" "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== $stack ==="; alchemy state stages us-west-1.run.ts --local --stack "$stack" 2>&1; done
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-east-1" "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== $stack ==="; alchemy state resources --stack "$stack" --stage bench us-west-1.run.ts --local 2>&1 | grep -i instance; done
cd /workspace/alchemy && for stack in "alchemy-effect-ec2-multiregion-us-east-1" "alchemy-effect-ec2-multiregion-us-west-1" "alchemy-effect-ec2-multiregion-us-west-2"; do echo "=== $stack ==="; alchemy state resources --stack "$stack" --stage bench us-west-1.run.ts --local 2>&1; done
cd /workspace/alchemy && alchemy state get --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage bench --fqn "WebServer" us-west-1.run.ts --local 2>&1 | head -100
cd /workspace/alchemy && alchemy state get --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage bench --fqn "WebSecurityGroup" us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && for instance in "DefaultVpcServer" "LaunchTemplateServer" "PrivateServer"; do echo "=== $instance ==="; alchemy state get --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage bench --fqn "$instance" us-west-1.run.ts --local 2>&1 | grep -E '"(instanceId|state|publicIpAddress|securityGroupIds|launchTemplate)"'; done
cd /workspace/alchemy && alchemy state get --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage bench --fqn "DefaultVpcServer" us-west-1.run.ts --local 2>&1 | jq '{instanceId: .attr.instanceId, state: .attr.state, publicIpAddress: .attr.publicIpAddress, securityGroupIds: .attr.securityGroupIds, subnetId: .attr.subnetId}'
cd /workspace/alchemy && alchemy state get --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage bench --fqn "LaunchTemplateServer" us-west-1.run.ts --local 2>&1 | jq '{instanceId: .attr.instanceId, state: .attr.state, publicIpAddress: .attr.publicIpAddress, securityGroupIds: .attr.securityGroupIds, launchTemplate: .props.launchTemplate}'
cd /workspace/alchemy && alchemy state get --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage bench --fqn "LaunchTemplateServer" us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state get --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage bench --fqn "WebLaunchTemplate" us-west-1.run.ts --local 2>&1
cd /workspace/alchemy && alchemy state get --stack "alchemy-effect-ec2-multiregion-us-east-1" --stage bench --fqn "PrivateServer" us-west-1.run.ts --local 2>&1 | jq '{instanceId: .attr.instanceId, state: .attr.state, publicIpAddress: .attr.publicIpAddress, securityGroupIds: .attr.securityGroupIds}'
# … 6 more
```
