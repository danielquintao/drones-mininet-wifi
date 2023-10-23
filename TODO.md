[x] Aprender a fazer drone mudar de direção sozinho \
    Ideia: tentar fazer um script changedir.py tal que, abrindo um terminal pro drone (`xterm`)
    e chamando `python3 changedir.py <latitude> <longitude>`, o drone mude de direção na hora. \
    Pode ser também um servidor HTTP que espera comandos, por ex., `GET /changedir?lat=...&lon=...`

[ ] Pensar no caso em que a simulação já "acabou" (staX.p = []) e a gente quer fazer o drone se mover.
    Qual a melhor forma dew resolver?
- append no staX.p ao invés de manter seu tamanho o mesmo?
- acrescentar várias posicões paradas no fim da simulacao para evitar que staX.p seja vazio (i.e., fazer o movimento durar mais)?
 
[x] Adaptar o código do flexão para o cenário no exame:
- 9 drones em formação 3x3
- ponto de destino fixo
- ...

[ ] Implementar o protocolo
- dentro do protocolo, o drone pode fazer requests ao servidor de jeito parecido ao `change_my_dir.py` 
(só q o `change_my_dir.py` é uma CLI q a gente chama na mãe, o q n é o caso pra implementa~ção do protocolo
em q temos basicamente um while true, como no lab 2)
- precisaremos implementar um GET no `server.py` para que os drones perguntem sua posição atual ao servidor.
Isso pode ser visto como uma consulta simulada a um sistema de GPS.