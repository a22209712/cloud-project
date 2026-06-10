# Limitações e Melhorias Futuras

## Limitações Atuais

* Apenas uma instância EC2
* Apenas uma Availability Zone
* Apenas uma fila SQS
* Sem Load Balancer
* Sem Auto Scaling
* Sem Kubernetes
* Backend e Worker executam na mesma instância

## Melhorias Futuras

### Alta Disponibilidade

* Multi-AZ
* Elastic Load Balancer
* Auto Scaling Groups

### Orquestração

* Amazon EKS
* Kubernetes

### Monitorização

* AWS CloudWatch
* Centralização de logs

### Segurança

* Subnets privadas
* AWS Secrets Manager
* Integração com WAF

### CI/CD

* Deploy automático para EC2
* Terraform Plan em Pull Requests
* Ambiente de produção
