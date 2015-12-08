# Trabalho-Redes
Repositório para trabalho de redes da UFSCar - 2015 <br><br>
Autores: <br>
André de Castro Pessoa Guimaraes <br>
Lucas Felix de Lima <br>
Rodrigo Texeira Garcia <br>

<h2> Repositório para o T1 e o T2</h2>

<h2>Informacoes necessárias para T1:</h2> <br>

1)É necessário colocar o endereco de ip dos daemons no programa webserver.py <br>
	Para isso é necessário colocar esses ips no vetor HOST[] logo no inicio do programa <br>
2)O programa é feito para funcionar com até 3 daemons <br>
3)O backend.py foi, inicialmente, feito de forma separada do webserver.py, mas está integrado com o mesmo na versão final <br>
4)A porta definida pelo grupo é a 10000 <br>
5)A página html com as informacoes recebidas das máquinas também é criada no arquivo webserver.py durante a execucao dos comandos <br>
6)Foi utilizado python2.7

<h2>Informacoes imporatantes e necessárias para T2:</h2> <br>

1) Para o congestionamento será usado a janela Go-Back-N, onde cria-se uma janela de tamanho N. É enviado um número de pacotes iguais o de janela, sendo que o emissor espera os acks para esses pacotes enviados. Caso não receba todos os ACKS da janela até o tempo limite, todos os pacotes sao enviados novamente. <br>
2) O tamanho da janela pode ser definida dentro do codigo alterando a variavel tamanhoJanela, localizada no server.py <br>
3) Para definir a chance de corrupcao de pacote e a chance de perda de pacote, é apenas altera as variaveis corruptionFactor e packetLossFactor localizadas no client.py. A chance é calculada da seguinte maneira: Chance = 1/(factor+1) <br>
4) Para separar em pacotes, o grupo resolveu utilizar uma abordagem de separar em arquivos do tamanho desejado e enviar esses pequenos pacotes para o cliente, que depois junta todos os recebidos em um arquivo só, igual ao original. Para a quebra do arquivo, foi usado como base um código já existente (https://github.com/WyomingGeezer/binfileio/blob/master/chunker.py), que apenas separa e junta os arquivos. <br>
5) Uma outra solução para a quebra de do arquivo em pacotes, seria de criar uma string com os dados do arquivo e ir separando do tamanho desejado, apenas acrescentando o cabeçalho desejado. Essa solução teria sido mais simples de implementar. <br>
6) Na nossa solução, existe um protótipo de cabecalho, formado por (NUMEROSEQUENCIA | CHECKSUM ||), sendo que o "|" é utilizado como delimitador de campo do cabeçalho e o "||" para delimitar o fim do cabeçalho. Caso precise adicionar outras informações ao cabeçalho, deve-se apenas colocar outros campos nele e escrever depois os valores adqueados. Outras informações que poderiam estar no cabeçalho seriam porta de entrada/destino e endereços. Para essa solução usada, não necessitamos desses valores. <br>
