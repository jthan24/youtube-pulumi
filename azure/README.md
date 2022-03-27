
# Crear el proyecto
pulumi new azure-python
![](./assets/Screenshot%20from%202022-03-26%2023-03-17.png).

# Listar todas las regiones de Azure
az account list-locations --output table

# Cambiar la configuracion del proyecto en pulumi
pulumi config set azure-native:location westcentralus