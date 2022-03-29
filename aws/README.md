
# Configurar las credenciales para el proyecto
export AWS_ACCESS_KEY_ID=9999999999AAAAAAAAAAAA
export AWS_SECRET_ACCESS_KEY=777777777777777+aaaaaaAAAAA
export AWS_DEFAULT_REGION=eu-west-1

# Crear el proyecto base con AWS
pulumi new aws-python
![](./assets/Screenshot%20from%202022-03-28%2020-30-32.png).

# Aplicar la infraestructura
pulumi up --stack dev

# Eliminar la infraestructura
pulumi destroy --stack dev --yes