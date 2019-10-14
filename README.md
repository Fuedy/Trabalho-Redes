# Trabalho-Redes
Repositório para trabalho de redes da UFSCar - 2015

Autores:
- André de Castro Pessoa Guimaraes
- Lucas Felix de Lima
- Rodrigo Texeira Garcia

## Repositório para o T1 e o T2

### Informações necessárias para T1

1. É necessário colocar o endereco de ip dos daemons no programa _webserver.py_
    - Para isso é necessário colocar esses ips no vetor `HOST[]` logo no inicio do programa
2. O programa é feito para funcionar com até 3 daemons
3. O _backend.py_ foi, inicialmente, feito de forma separada do _webserver.py_, mas está integrado com o mesmo na versão final
4. A porta definida pelo grupo é a 10000
5. A página html com as informacoes recebidas das máquinas também é criada no arquivo _webserver.py_ durante a execução dos comandos
6. Foi utilizado python2.7

### Informações importantes e necessárias para T2

1. Para o congestionamento será usado a janela _Go-Back-N_, onde cria-se uma janela de tamanho N. É enviado um número de pacotes iguais o de janela, sendo que o emissor espera os ACKS para esses pacotes enviados. Caso não receba todos os ACKS da janela até o tempo limite, todos os pacotes são enviados novamente.
2. O tamanho da janela pode ser definida dentro do código alterando a variável `tamanhoJanela`, localizada no _server.py_
3. Para definir a chance de corrupcao de pacote e a chance de perda de pacote, é apenas altera as variaveis `corruptionFactor` e `packetLossFactor` localizadas no _client.py_. A chance é calculada da seguinte maneira: `Chance = 1/(factor+1)`
4. Para separar em pacotes, o grupo resolveu utilizar uma abordagem de separar em arquivos do tamanho desejado e enviar esses pequenos pacotes para o cliente, que depois junta todos os recebidos em um arquivo só, igual ao original. Para a quebra do arquivo, foi usado como base um código [já existente](https://github.com/WyomingGeezer/binfileio/blob/master/chunker.py), que apenas separa e junta os arquivos.
5. Uma outra solução para a quebra de do arquivo em pacotes, seria de criar uma string com os dados do arquivo e ir separando do tamanho desejado, apenas acrescentando o cabeçalho desejado. Essa solução teria sido mais simples de implementar.
6. Na nossa solução, existe um protótipo de cabecalho, formado por (NUMEROSEQUENCIA | CHECKSUM ||), sendo que o "|" é utilizado como delimitador de campo do cabeçalho e o "||" para delimitar o fim do cabeçalho. Caso precise adicionar outras informações ao cabeçalho, deve-se apenas colocar outros campos nele e escrever depois os valores adequados. Outras informações que poderiam estar no cabeçalho seriam porta de entrada/destino e endereços. Para essa solução usada, não necessitamos desses valores.
