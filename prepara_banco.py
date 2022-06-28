import MySQLdb
print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='123456',
                       host='127.0.0.1', port=3306, charset='utf8')

# Descomente se quiser desfazer o banco
conn.cursor().execute("DROP DATABASE IF EXISTS `tabelaperiodica`;")
conn.commit()

criar_tabelas = '''SET NAMES utf8;
    CREATE DATABASE `tabelaperiodica` DEFAULT CHARSET=utf8;
    USE `tabelaperiodica`;

CREATE TABLE IF NOT EXISTS `tabelaperiodica`.`classe` (
  `id_classe` INT NOT NULL AUTO_INCREMENT,
  `nome_classe` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_classe`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `tabelaperiodica`.`elemento` (
  `id_elemento` INT NOT NULL AUTO_INCREMENT,
  `nome_elemento` VARCHAR(45) NOT NULL,
  `num_atomico` INT NOT NULL,
  `massa_atomica` DOUBLE NOT NULL,
  `estado_fisico` VARCHAR(20) NOT NULL,
  `simbolo` VARCHAR(2) NOT NULL,
  `distribuicao_eletronica` VARCHAR(20) NOT NULL,
  `classe` INT NOT NULL,
  PRIMARY KEY (`id_elemento`),
  INDEX `fk_elemento_classe_idx` (`classe` ASC) VISIBLE,
  CONSTRAINT `fk_elemento_classe`
    FOREIGN KEY (`classe`)
    REFERENCES `tabelaperiodica`.`classe` (`id_classe`)
    ON DELETE CASCADE 
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `tabelaperiodica`.`curiosidade` (
  `id_curiosidade` INT NOT NULL AUTO_INCREMENT,
  `tipo` VARCHAR(45) NOT NULL,
  `descricao` TEXT NOT NULL,
  `elemento` INT NOT NULL,
  PRIMARY KEY (`id_curiosidade`),
  INDEX `fk_curiosidade_elemento1_idx` (`elemento` ASC) VISIBLE,
  CONSTRAINT `fk_curiosidade_elemento1`
    FOREIGN KEY (`elemento`)
    REFERENCES `tabelaperiodica`.`elemento` (`id_elemento`)
    ON DELETE CASCADE 
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `usuario` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `nome_usuario` varchar(55) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email_usuario` varchar(45) NOT NULL,
  `senha` varchar(45) NOT NULL,
  PRIMARY KEY (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE IF NOT EXISTS `tipo_usuario` (
  `id_tipo_usuario` int NOT NULL,
  `descricao_tipo_usuario` varchar(45) NOT NULL,
  KEY `FK_tipo_usuario_usuario` (`id_tipo_usuario`),
  CONSTRAINT `FK_tipo_usuario_usuario` FOREIGN KEY (`id_tipo_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


CREATE TABLE IF NOT EXISTS `tabelaperiodica`.`nivel` (
  `id_nivel` INT NOT NULL AUTO_INCREMENT,
  `nome_nivel` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_nivel`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `tabelaperiodica`.`desafio` (
  `id_desafio` INT NOT NULL AUTO_INCREMENT,
  `quantidade_perguntas` VARCHAR(45) NOT NULL,
  `nivel` INT NOT NULL,
  PRIMARY KEY (`id_desafio`),
  INDEX `fk_desafio_nivel1_idx` (`nivel` ASC) VISIBLE,
  CONSTRAINT `fk_desafio_nivel1`
    FOREIGN KEY (`nivel`)
    REFERENCES `tabelaperiodica`.`nivel` (`id_nivel`)
    ON DELETE CASCADE 
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `tabelaperiodica`.`perguntas` (
  `id_perguntas` INT NOT NULL AUTO_INCREMENT,
  `nome_pergunta` VARCHAR(20) NOT NULL,
  `descricao` TEXT NOT NULL,
  `resposta` TEXT NOT NULL,
  `desafio` INT NOT NULL,
  PRIMARY KEY (`id_perguntas`),
  INDEX `fk_perguntas_desafio1_idx` (`desafio` ASC) VISIBLE,
  CONSTRAINT `fk_perguntas_desafio1`
    FOREIGN KEY (`desafio`)
    REFERENCES `tabelaperiodica`.`desafio` (`id_desafio`)
    ON DELETE CASCADE 
    ON UPDATE CASCADE)
ENGINE = InnoDB;

'''

conn.cursor().execute(criar_tabelas)

cursor = conn.cursor()
cursor.executemany(
    'INSERT INTO `classe` (`id_classe`, `nome_classe`) VALUES (%s, %s)',
    [
        (1, 'Metais Alcalinos'),
        (2, 'Metais Alcalinos Terrosos'),
        (3, 'Metais de Transição'),
        (4, 'Lantanídeos'),
        (5, 'Actinídeos'),
        (6, 'Gases Nobres'),
        (7, 'Semimetais'),
        (8, 'Não metais'),
        (9, 'Halogênios'),
        (10, 'Outros metais'),
    ])

cursor.execute('select * from tabelaperiodica.classe')
print(' ------------ Classes: ------------ ')
for classe in cursor.fetchall():
    print(classe[1])

cursor.executemany(
    'INSERT INTO `elemento` (`id_elemento`, `nome_elemento`, `num_atomico`, `massa_atomica`, `estado_fisico`, `simbolo`, `distribuicao_eletronica`, `classe`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
    [
        (1, 'Hidrogênio', 1, '1', 'Gasoso', 'H', '1s¹', 8),
        (2, 'Hélio', 2, '4', 'Gasoso', 'He', '1s²', 6),
        (3, 'Lítio', 3, '7', 'Sólido', 'Li', '[He]2s¹', 1),
        (4, 'Berílio', 4, '9', 'Sólido', 'Be', '[He]2s²', 2),
        (6, 'Boro', 5, '11', 'Sólido', 'B', '[He]2s²2p¹', 7),
        (7, 'Carbono', 6, '12', 'Sólido', 'C', '[He]2s²2p²', 8),
        (8, 'Nitrogênio', 7, '14', 'Gasoso', 'N', '[He]2s²2p³', 8),
        (9, 'Oxigênio', 8, '16', 'Gasoso', 'O', '[He]2s²2p⁴', 8),
        (10, 'Flúor', 9, '19', 'Gasoso', 'F', '[He]2s²2p⁵', 9),
        (11, 'Neônio', 10, '20', 'Gasoso', 'Ne', '[He]2s²2p⁶', 6),
        (12, 'Sódio', 11, '23', 'Sólido', 'Na', '[Ne]3s¹', 1),
        (13, 'Magnésio', 12, '24', 'Sólido', 'Mg', '[Ne]3s²', 2),
        (14, 'Alumínio', 13, '27', 'Sólido', 'Al', '[Ne]3s²3p¹', 10),
        (15, 'Silício', 14, '28', 'Sólido', 'Si', '[Ne]3s²3p²', 7),
        (16, 'Fósforo', 15, '31', 'Sólido', 'P', '[Ne]3s²3p³', 8),
        (17, 'Enxofre', 16, '32', 'Sólido', 'S', '[Ne]3s²3p⁴', 8),
        (18, 'Cloro', 17, '35', 'Sólido', 'Cl', '[Ne]3s²3p⁵', 9),
        (19, 'Argônio', 18, '40', 'Gasoso', 'Ar', '[Ne]3s²3p⁶', 6),
        (20, 'Potássio', 19, '39', 'Sólido', 'K', '[Ar]4s¹', 1),
        (21, 'Cálcio', 20, '40', 'Sólido', 'Ca', '[Ar]4s²', 2),
        (22, 'Escândio', 21, '45', 'Sólido', 'Sc', '[Ar]3d¹4s²', 3),
        (23, 'Titânio', 22, '48', 'Sólido', 'Ti', '[Ar]3d²4s²', 3),
        (24, 'Vanádio', 23, '51', 'Sólido', 'V', '[Ar]3d³4s²', 3),
        (25, 'Crômio', 24, '52', 'Sólido', 'Cr', '[Ar]3d⁵4s¹', 3),
        (26, 'Manganês', 25, '55', 'Sólido', 'Mn', '[Ar]3d⁵4s²', 3),
        (27, 'Ferro', 26, '56', 'Sólido', 'Fe', '[Ar]3d⁶4s²', 3),
        (28, 'Cobalto', 27, '59', 'Sólido', 'Co', '[Ar]3d⁷4s²', 3),
        (29, 'Níquel', 28, '59', 'Sólido', 'Ni', '[Ar]3d⁸4s²', 3),
        (30, 'Cobre', 29, '64', 'Sólido', 'Cu', '[Ar]3d¹º4s¹', 3),
        (31, 'Zinco', 30, '66', 'Sólido', 'Zn', '[Ar]3d¹º4s²', 3),
        (32, 'Gálio', 31, '70', 'Sólido', 'Ga', '[Ar]3d¹º4s²4p¹', 10),
        (33, 'Germânio', 32, '73', 'Sólido', 'Ge', '[Ar]3d¹º4s²4p²', 7),
        (34, 'Arsênio', 33, '75', 'Sólido', 'As', '[Ar]3d¹º4s²4p³', 7),
        (35, 'Selênio', 34, '79', 'Sólido', 'Se', '[Ar]3d¹º4s²4p⁴', 8),
        (36, 'Bromo', 35, '80', 'Líquido', 'Br', '[Ar]3d¹º4s²4p⁵', 9),
        (37, 'Criptônio', 36, '84', 'Gasoso', 'Kr', '[Ar]3d¹º4s²4p⁶', 6),
        (38, 'Rubídio', 37, '86', 'Sólido', 'Rb', '[Kr]5s¹', 1),
        (39, 'Estrôncio', 38, '88', 'Sólido', 'Sr', '[Kr]5s²', 2),
        (40, 'Ítrio', 39, '89', 'Sólido', 'Y', '[Kr]4d¹5s²', 3),
        (41, 'Zírcônio', 40, '91', 'Sólido', 'Zr', '[Kr]4d²5s²', 3),
        (42, 'Niôbio', 41, '93', 'Sólido', 'Nb', '[Kr]4d⁴5s¹', 3),
        (43, 'Molibdênio', 42, '96', 'Sólido', 'Mo', '[Kr]4d⁵5s¹', 3),
        (44, 'Tecnécio', 43, '98', 'Sólido', 'Tc', '[Kr]4d⁵5s²', 3),
        (45, 'Rutênio', 44, '101', 'Sólido', 'Ru', '[Kr]4d⁷5s¹', 3),
        (46, 'Ródio', 45, '103', 'Sólido', 'Rh', '[Kr]4d⁸5s¹', 3),
        (47, 'Paládio', 46, '107', 'Sólido', 'Pd', '[Kr]4d¹º', 3),
        (48, 'Prata', 47, '108', 'Sólido', 'Ag', '[Kr]4d¹º5s¹', 3),
        (49, 'Cádmio', 48, '113', 'Sólido', 'Cd', '[Kr]4d¹º5s²', 3),
        (50, 'Índio', 49, '115', 'Sólido', 'In', '[Kr]4d¹º5s²5p¹', 10),
        (51, 'estanho', 50, '119', 'Sólido', 'Sn', '[Kr]4d¹º5s²5p²', 10),
        (52, 'Antimônio', 51, '122', 'Sólido', 'Sb', '[Kr]4d¹º5s²5p³', 7),
        (53, 'Telúrio', 52, '128', 'Sólido', 'Te', '[Kr]4d¹º5s²5p⁴', 7),
        (54, 'Iodo', 53, '127', 'Sólido', 'I', '[Kr]4d¹º5s²5p⁵', 9),
        (55, 'Xenônio', 54, '131', 'Gasoso', 'Xe', '[Kr]4d¹º5s²5p⁶', 6),
        (56, 'Césio', 55, '133', 'Sólido', 'Cs', '[Xe]6s¹', 1),
        (57, 'Bário', 56, '137', 'Sólido', 'Ba', '[Xe]6s²', 2),
        (58, 'Lantânio', 57, '139', 'Sólido', 'La', '[Xe]5d¹6s²', 4),
        (59, 'Cério', 58, '140', 'Sólido', 'Ce', '[Xe]4f¹5d¹6s²', 4),
        (60, 'Praseodímio', 59, '141', 'Sólido', 'Pr', '[Xe]4f³6s²', 4),
        (61, 'Neodímio', 60, '144', 'Sólido', 'Nd', '[Xe]4f⁴6s²', 4),
        (62, 'Promécio', 61, '145', 'Sólido', 'Pm', '[Xe]4f⁵6s²', 4),
        (63, 'Samário', 62, '150', 'Sólido', 'Sm', '[Xe]4f⁶6s²', 4),
        (64, 'Európio', 63, '152', 'Sólido', 'Eu', '[Xe]4f⁷6s²', 4),
        (65, 'Gadolínio', 64, '157', 'Sólido', 'Gd', '[Xe]4f⁷5d¹6s²', 4),
        (66, 'Térbio', 65, '159', 'Sólido', 'Tb', '[Xe]4f⁹6s²', 4),
        (67, 'Disprósio', 66, '163', 'Sólido', 'Dy', '[Xe]4f¹º6s²', 4),
        (68, 'Hólmio', 67, '165', 'Sólido', 'Ho', '[Xe]4f¹¹6s²', 4),
        (69, 'Érbio', 68, '167', 'Sólido', 'Er', '[Xe]4f¹²6s²', 4),
        (70, 'Túlio', 69, '169', 'Sólido', 'Tm', '[Xe]4f¹³6s²', 4),
        (71, 'Itérbio', 70, '173', 'Sólido', 'Yb', '[Xe]4f¹⁴6s²', 4),
        (72, 'Lutécio', 71, '175', 'Sólido', 'Lu', '[Xe]4f¹⁴5d¹6s²', 4),
        (73, 'Háfnio', 72, '178', 'Sólido', 'Hf', '[Xe]4f¹⁴5d²6s²', 3),
        (74, 'Tântalo', 73, '181', 'Sólido', 'Ta', '[Xe]4f¹⁴5d³6s²', 3),
        (75, 'Tungstênio', 74, '184', 'Sólido', 'W', '[Xe]4f¹⁴5d⁴6s²', 3),
        (76, 'Rênio', 75, '186', 'Sólido', 'Re', '[Xe]4f¹⁴5d⁵6s²', 3),
        (77, 'Ósmio', 76, '190', 'Sólido', 'Os', '[Xe]4f¹⁴5d⁶6s²', 3),
        (78, 'Íridio', 77, '192', 'Sólido', 'Ir', '[Xe]4f¹⁴5d⁷6s²', 3),
        (79, 'Platina', 78, '195', 'Sólido', 'Pt', '[Xe]4f¹⁴5d⁹6s²', 3),
        (80, 'Ouro', 79, '197', 'Sólido', 'Au', '[Xe]4f¹⁴5d¹º6s¹', 3),
        (81, 'Mercúrio', 80, '201', 'Líquido', 'Hg', '[Xe]4f¹⁴5d¹º6s²', 3),
        (82, 'Tálio', 81, '204', 'Sólido', 'Ti', '[Xe]4f¹⁴5d¹º6s²6p¹', 10),
        (83, 'Chumbo', 82, '204', 'Sólido', 'Pb', '[Xe]4f¹⁴5d¹º6s²6p²', 10),
        (84, 'Bismuto', 83, '209', 'Sólido', 'Bi', '[Xe]4f¹⁴5d¹º6s²6p³', 10),
        (85, 'Polônio', 84, '209', 'Sólido', 'Po', '[Xe]4f¹⁴5d¹º6s²6p⁴', 7),
        (86, 'Astato', 85, '210', 'Sólido', 'At', '[Xe]4f¹⁴5d¹º6s²6p⁵', 8),
        (87, 'Radônio', 86, '222', 'Gasoso', 'Rn', '[Xe]4f¹⁴5d¹º6s²6p⁶', 6),
        (88, 'Frâncio', 87, '223', 'Sólido', 'Fr', '[Rn]7s¹', 1),
        (89, 'Rádio', 88, '226', 'Sólido', 'Ra', '[Rn]7s²', 2),
        (90, 'Actínio', 89, '227', 'Sólido', 'Ac', '[Rn]6d¹7s²', 5),
        (91, 'Tório', 90, '232', 'Sólido', 'Th', '[Rn]6d²7s²', 5),
        (92, 'Protactínio', 91, '231', 'Sólido', 'Pa', '[Rn]5f²6d¹7s²', 5),
        (93, 'Urânio', 92, '238', 'Sólido', 'U', '[Rn]5f³6d¹7s²', 5),
        (94, 'Neptúnio', 93, '237', 'Sólido', 'Np', '[Rn]5f⁴6d¹7s²', 5),
        (95, 'Plutônio', 94, '244', 'Sólido', 'Pu', '[Rn]5f⁶7s²', 5),
        (96, 'Amerício', 95, '243', 'Sólido', 'Am', '[Rn]5f⁷7s²', 5),
        (97, 'Cúrio', 96, '247', 'Sólido', 'Cm', '[Rn]5f⁷6d¹7s²', 5),
        (98, 'Berquélio', 97, '247', 'Sólido', 'Bk', '[Rn]5f⁹7s²', 5),
        (99, 'Califórnio', 98, '251', 'Sólido', 'Cf', '[Rn]5f¹º7s²', 5),
        (100, 'Einstênio', 99, '252', 'Sólido', 'Es', '[Rn]5f¹¹7s²', 5),
        (101, 'Fêrmio', 100, '257', 'Sólido', 'Fm', '[Rn]5f¹²7s²', 5),
        (102, 'Mendelévio', 101, '258', 'Sólido', 'Md', '[Rn]5f¹³7s²', 5),
        (103, 'Nobélio', 102, '259', 'Sólido', 'No', '[Rn]5f¹⁴7s²', 5),
        (104, 'Laurêncio', 103, '262', 'Sólido', 'Lr', '[Rn]5f¹⁴7s²7p¹', 5),
        (105, 'Rutherfórdio', 104, '267', 'Sólido', 'Rf', '[Rn]5f¹⁴6d²7s²', 3),
        (106, 'Dúbnio', 105, '268', 'Sólido', 'Db', '[Rn]5f¹⁴6d³7s²', 3),
        (107, 'Seabórgio', 106, '269', 'Sólido', 'Sg', '[Rn]5f¹⁴6d⁴7s²', 3),
        (108, 'Bóhrio', 107, '270', 'Sólido', 'Bh', '[Rn]5f¹⁴6d⁵7s²', 3),
        (109, 'Hássio', 108, '269', 'Sólido', 'Hs', '[Rn]5f¹⁴6d⁶7s²', 3),
        (110, 'Meitnério', 109, '278', 'Sólido', 'Mt', '[Rn]5f¹⁴6d⁷7s²', 3),
        (111, 'Darmstádtio', 110, '281', 'Sólido', 'Ds', '[Rn]5f¹⁴6d⁹7s¹', 3),
        (112, 'Roentgênio', 111, '280', 'Sólido', 'Rg', '[Rn]5f¹⁴6d¹º7s¹', 3),
        (113, 'Copernício', 112, '285', 'Líquido', 'Cn', '[Rn]5f¹⁴6d¹º7s²', 3),
        (114, 'Nihônio', 113, '286', 'Sólido', 'Nh', '[Rn]5f¹⁴6d¹º7s²7p¹', 10),
        (115, 'Fleróvio', 114, '289', 'Sólido', 'Fl', '[Rn]5f¹⁴6d¹º7s²7p²', 10),
        (116, 'Moscóvio', 115, '289', 'Sólido', 'Mc', '[Rn]5f¹⁴6d¹º7s²7p³', 10),
        (117, 'Livermório', 116, '293', 'Gasoso', 'Lv', '[Rn]5f¹⁴6d¹º7s²7p⁴', 10),
        (118, 'Tennesso', 117, '294', 'Sólido', 'Ts', '[Rn]5f¹⁴6d¹º7s²7p⁵', 9),
        (119, 'Oganessônio', 118, '294', 'Sólido', 'Og', '[Rn]5f¹⁴6d¹º7s²7p⁶', 6)
    ])

cursor.execute('select * from tabelaperiodica.elemento')
print(' ------------ Elementos: ------------ ')
for elemento in cursor.fetchall():
    print(elemento[1])

cursor.executemany(
    'INSERT INTO `curiosidade` (`id_curiosidade`, `tipo`, `descricao`, `elemento`) VALUES (%s, %s, %s, %s)',
    [
        (1, 'Propriedades', 'Ocorre como um gás incolor, inodoro e altamente inflamável. É o elemento de menor densidade da Tabela Periódica e por este motivo era utilizado no enchimento de dirigíveis, mas teve seu uso abolido devido à elevada inflamabilidade.', 1),
        (2, 'Abundância', 'O hidrogênio é o elemento mais abundante do universo. Sendo encontrado no sol, na maioria das estrelas e o principal constituinte do planeta Júpiter.', 1),
        (3, 'Usos', 'O gás hidrogênio (H2) é considerado\no combustível limpo do futuro, uma vez que sua combustão produz água. A eletrólise da água constitui um dos principais métodos de obtenção do gás hidrogênio.', 1),
        (4, 'Propriedades', 'O hélio é o segundo elemento menos denso da Tabela Periódica, e por este motivo é comumente usado no enchimento de balões decorativos, bem como de balões meteorológicos ou dirigíveis.', 2),
        (5, 'Origem do nome', 'O nome hélio vem da palavra grega “helios” que significa “SOL”. O hélio é o principal componente do sol, onde é formado pela fusão nuclear de átomos de hidrogênio, processo que libera uma quantidade altíssima de energia.', 2),
        (6, 'Usos', 'Devido ao seu baixíssimo ponto de congelamento, o hélio é usado em\r\ncrioscopia como meio de resfriamento de equipamentos diversos como os espectrômetros de RMN e para resfriar o combustível de veículos espaciais.', 2),
    ])

cursor.execute('select * from tabelaperiodica.curiosidade')
print(' ------------ Curiosidades: ------------ ')
for curiosidade in cursor.fetchall():
    print(curiosidade[1])

cursor.executemany(
    'INSERT INTO `usuario` (`id_usuario`, `usuario`,`nome_usuario`, `email_usuario`, `senha`) VALUES (%s, %s, %s, %s, %s)',
    [
        (1,'amanda', 'Amanda Eleutério', 'amanda2@gmail.com', '54321'),
        (2,'daiane', 'Daiane Cristina', 'daiane@gmail.com', '54321'),
        (3,'tiago', 'Tiago Carlos', 'tiago@gmail.com', '54321'),
    ])

cursor.execute('select * from tabelaperiodica.usuario')
print(' ------------ Usuário: ------------ ')
for usuario in cursor.fetchall():
    print(usuario[1])

cursor.executemany(
    'INSERT INTO `tipo_usuario` (`id_tipo_usuario`, `descricao_tipo_usuario`) VALUES (%s, %s)',
    [
        (1, 'Professor'),
        (2, 'Aluno'),
        (3, 'Professor'),
    ])

cursor.execute('select * from tabelaperiodica.tipo_usuario')
print(' ------------ Tipo de Usuário: ------------ ')
for tipo_usuario in cursor.fetchall():
    print(tipo_usuario[1])


cursor.executemany(
    'INSERT INTO `nivel` (`id_nivel`, `nome_nivel`) VALUES(%s, %s)',
    [
        (1, 'Fácil'),
        (2, 'Médio'),
        (3, 'Difícil'),
    ])

cursor.execute('select * from tabelaperiodica.nivel')
print(' ------------ Nível: ------------ ')
for nivel in cursor.fetchall():
    print(nivel[1])
conn.commit()
cursor.close()
