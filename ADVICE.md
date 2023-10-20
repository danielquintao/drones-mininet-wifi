1. `staX.pos` e `staX.position` (para o nó `staX` qualquer) não são coerentes:
    ```
    mininet-wifi> py sta1.pos
    (0, 0, 0)
    mininet-wifi> py sta1.position
    (40.0, 40.0, 0.0)
    ```