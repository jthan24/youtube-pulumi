# youtube-pulumi
Deploy with pulumi some stacks!! over #aws #gpc and #azure


# Instalar Pulumi en Windows
choco install pulumi

# Instalar Pulumi con bash (Mac/Linux)
curl -fsSL https://get.pulumi.com | sh

# Instalar Python en Linux
https://docs.python-guide.org/starting/install3/linux/


# Instalar Pulumi con asdf
asdf plugin list all |grep pulumi
asdf plugin add plugin pulumi https://github.com/canha/asdf-pulumi.git 
asdf install pulumi latest
asdf local pulumi latest


# Iniciar sesion en Pulumi
https://app.pulumi.com/account/tokens


# Crear token en la consola de Pulumi
export PULUMI_ACCESS_TOKEN=pul-999999999999999999aaaaaaaaaaaaaaaaaaaaa


# Aprovisionar la infraestructura
pulumi up

# Eliminar la infraestructura
pulumi destroy

# Eliminar el stack de la pagina de pulumi
pulumi stack rm dev