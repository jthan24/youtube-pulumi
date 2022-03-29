# Agregar el cliente de gcloud

asdf plugin list all |grep gcloud
asdf plugin add gcloud https://github.com/jthegedus/asdf-gcloud.git
asdf install gcloud latest
asdf local gcloud latest


# Configurar las credenciales para el proyecto

gcloud config set project pulumi-28324
gcloud auth application-default login

# Crear el proyecto base con GCP
pulumi new gcp-python
![](./assets/Screenshot%20from%202022-03-28%2015-39-32.png).

# Aplicar la infraestructura
pulumi up --stack dev

# Eliminar la infraestructura
pulumi destroy --stack dev --yes