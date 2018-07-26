# sharingan
apt-get update && apt-get upgrade -y

export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list sudo apt-get update && sudo apt-get install google-cloud-sdk gcloud init gcloud auth application-default login

No Console do GCP, navegue até a página Criar chave da conta de serviço. No menu suspenso Conta de serviço, selecione Nova conta de serviço. Insira um nome no campo do formulário Nome da conta de serviço. No menu suspenso Papel, selecione Projeto > Proprietário.

cole o json em: /root/.config/gcloud/application_default_credentials.json

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py python get-pip.py

apt install python-pip pip install beautifulsoup4 pip install requests pip install --upgrade google-cloud-vision pip install pika pip install json pip install ast

echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list curl http://www.rabbitmq.com/rabbitmq-signing-key-public.asc | sudo apt-key add - apt-get update sudo apt-get install rabbitmq-server rabbitmq-plugins enable rabbitmq_management

rabbitmqctl add_user user pass rabbitmqctl set_user_tags user administrator rabbitmqctl set_permissions -p / user "." "." ".*"

criar as filas:domain, imageurls, phisher criar user gerente deletar guest

start as daemons
