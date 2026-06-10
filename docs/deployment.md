# Deployment

1. Terraform creates infrastructure

```bash
terraform init
terraform apply
```

2. Ansible installs Docker

```bash
ansible-playbook -i inventory.ini install-docker.yml
```

3. GitHub Actions builds image

4. Image is pushed to Docker Hub

5. EC2 runs Docker container
```