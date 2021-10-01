DROP TABLE IF EXISTS novidade;

CREATE TABLE IF NOT EXISTS novidade(
    id_novidade INTEGER PRIMARY KEY AUTOINCREMENT,
    novidade_resumo TEXT,
    novidade_completa TEXT,
    novidade_data INTEGER
);

INSERT INTO novidade VALUES (1,'Eum cu tantas legere complectitur, hinc utamur ea eam. Eum
patrioque mnesarchum eu, diam erant convenire et vis. Et essent evertitur sea, vis cu ubique referrentur, sed eu dicant expetendis.',
'completo1','2018-09-25'),
(2,'Eum cu tantas legere complectitur, hinc utamur ea eam. Eum patrioque mnesarchum eu, diam
erant convenire et vis. Et essent evertitur sea, vis cu ubique referrentur, sed eu dicant expetendis.',
'completo2','2018-06-15'),
(3,'Eum cu tantas legere complectitur, hinc utamur ea eam. Eum patrioque mnesarchum eu, diam
erant convenire et vis. Et essent evertitur sea, vis cu ubique referrentur, sed eu dicant expetendis.',
'completo3','2018-04-07'),
(4,'Eum cu tantas legere complectitur, hinc utamur ea eam. Eum patrioque mnesarchum eu, diam
erant convenire et vis. Et essent evertitur sea, vis cu ubique referrentur, sed eu dicant expetendis.',
'completo4','2018-03-04');

DROP TABLE IF EXISTS usuario;

CREATE TABLE usuario(
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_completo TEXT,
    cpf  VARCHAR(15) UNIQUE,
    email TEXT,
    nascimento INTEGER,
    senha TEXT,
    data_cadastro INTEGER DEFAULT CURRENT_TIMESTAMP
);
