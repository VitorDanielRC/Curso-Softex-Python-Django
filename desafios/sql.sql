DROP DATABASE IF EXISTS loja_ecommerce;
CREATE DATABASE loja_ecommerce;
USE loja_ecommerce;

DROP TABLE IF EXISTS Itens_Pedido;
DROP TABLE IF EXISTS Pedidos;
DROP TABLE IF EXISTS Produtos;
DROP TABLE IF EXISTS Clientes;

CREATE TABLE Clientes (
id INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(100) NOT NULL,
email VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE Produtos (
id INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(100) NOT NULL,
preco DECIMAL(10,2) NOT NULL,
estoque INT NOT NULL DEFAULT 0
);

CREATE TABLE Pedidos (
id INT AUTO_INCREMENT PRIMARY KEY,
data_compra DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
total DECIMAL(10,2) NOT NULL,
id_cliente INT NOT NULL,
CONSTRAINT fk_pedidos_clientes
FOREIGN KEY (id_cliente) REFERENCES Clientes(id)
);

CREATE TABLE Itens_Pedido (
id INT AUTO_INCREMENT PRIMARY KEY,
id_pedido INT NOT NULL,
id_produto INT NOT NULL,
quantidade INT NOT NULL,
CONSTRAINT fk_itens_pedido_pedidos
FOREIGN KEY (id_pedido) REFERENCES Pedidos(id),
CONSTRAINT fk_itens_pedido_produtos
FOREIGN KEY (id_produto) REFERENCES Produtos(id)
);


INSERT INTO Clientes (nome, email) VALUES
('João',  'joao@exemplo.com'),
('Maria', 'maria@exemplo.com'),
('Ana',   'ana@exemplo.com');

INSERT INTO Produtos (nome, preco, estoque) VALUES
('Teclado', 150.00, 50),
('Mouse',    80.00, 100),
('Monitor', 850.90, 20);

INSERT INTO Pedidos (data_compra, total, id_cliente)
SELECT NOW(), 0.00, id
FROM Clientes
WHERE nome = 'Maria';

INSERT INTO Itens_Pedido (id_pedido, id_produto, quantidade) VALUES
(
LAST_INSERT_ID(),
(SELECT id FROM Produtos WHERE nome = 'Teclado'),
1
),
(
LAST_INSERT_ID(),
(SELECT id FROM Produtos WHERE nome = 'Mouse'),
2
);

UPDATE Pedidos p
JOIN (
SELECT ip.id_pedido,
SUM(ip.quantidade * pr.preco) AS total_calculado
FROM Itens_Pedido ip
JOIN Produtos pr ON ip.id_produto = pr.id
GROUP BY ip.id_pedido
) t ON p.id = t.id_pedido
SET p.total = t.total_calculado;

SELECT nome, preco
FROM Produtos
WHERE preco > 100.00;

SELECT
c.nome       AS nome_cliente,
p.id         AS id_pedido,
p.data_compra
FROM Pedidos p
JOIN Clientes c ON p.id_cliente = c.id
WHERE c.nome = 'Maria';




UPDATE Produtos
SET preco = preco * 1.10
WHERE nome = 'Mouse';


UPDATE Produtos
SET estoque = estoque - 2
WHERE nome = 'Mouse';




DELETE FROM Clientes
WHERE nome = 'João';


DELETE ip
FROM Itens_Pedido ip
JOIN Pedidos p   ON ip.id_pedido = p.id
JOIN Clientes c  ON p.id_cliente = c.id
JOIN Produtos pr ON ip.id_produto = pr.id
WHERE c.nome = 'Maria'
AND pr.nome = 'Teclado'
LIMIT 1;
