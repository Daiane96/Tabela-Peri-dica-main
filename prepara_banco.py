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
        (3, 'Metais de Transi????o'),
        (4, 'Lantan??deos'),
        (5, 'Actin??deos'),
        (6, 'Gases Nobres'),
        (7, 'Semimetais'),
        (8, 'N??o metais'),
        (9, 'Halog??nios'),
        (10, 'Outros metais'),
    ])

cursor.execute('select * from tabelaperiodica.classe')
print(' ------------ Classes: ------------ ')
for classe in cursor.fetchall():
    print(classe[1])

cursor.executemany(
    'INSERT INTO `elemento` (`id_elemento`, `nome_elemento`, `num_atomico`, `massa_atomica`, `estado_fisico`, `simbolo`, `distribuicao_eletronica`, `classe`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
    [
        (1, 'Hidrog??nio', 1, '1', 'Gasoso', 'H', '1s??', 8),
        (2, 'H??lio', 2, '4', 'Gasoso', 'He', '1s??', 6),
        (3, 'L??tio', 3, '7', 'S??lido', 'Li', '[He]2s??', 1),
        (4, 'Ber??lio', 4, '9', 'S??lido', 'Be', '[He]2s??', 2),
        (6, 'Boro', 5, '11', 'S??lido', 'B', '[He]2s??2p??', 7),
        (7, 'Carbono', 6, '12', 'S??lido', 'C', '[He]2s??2p??', 8),
        (8, 'Nitrog??nio', 7, '14', 'Gasoso', 'N', '[He]2s??2p??', 8),
        (9, 'Oxig??nio', 8, '16', 'Gasoso', 'O', '[He]2s??2p???', 8),
        (10, 'Fl??or', 9, '19', 'Gasoso', 'F', '[He]2s??2p???', 9),
        (11, 'Ne??nio', 10, '20', 'Gasoso', 'Ne', '[He]2s??2p???', 6),
        (12, 'S??dio', 11, '23', 'S??lido', 'Na', '[Ne]3s??', 1),
        (13, 'Magn??sio', 12, '24', 'S??lido', 'Mg', '[Ne]3s??', 2),
        (14, 'Alum??nio', 13, '27', 'S??lido', 'Al', '[Ne]3s??3p??', 10),
        (15, 'Sil??cio', 14, '28', 'S??lido', 'Si', '[Ne]3s??3p??', 7),
        (16, 'F??sforo', 15, '31', 'S??lido', 'P', '[Ne]3s??3p??', 8),
        (17, 'Enxofre', 16, '32', 'S??lido', 'S', '[Ne]3s??3p???', 8),
        (18, 'Cloro', 17, '35', 'S??lido', 'Cl', '[Ne]3s??3p???', 9),
        (19, 'Arg??nio', 18, '40', 'Gasoso', 'Ar', '[Ne]3s??3p???', 6),
        (20, 'Pot??ssio', 19, '39', 'S??lido', 'K', '[Ar]4s??', 1),
        (21, 'C??lcio', 20, '40', 'S??lido', 'Ca', '[Ar]4s??', 2),
        (22, 'Esc??ndio', 21, '45', 'S??lido', 'Sc', '[Ar]3d??4s??', 3),
        (23, 'Tit??nio', 22, '48', 'S??lido', 'Ti', '[Ar]3d??4s??', 3),
        (24, 'Van??dio', 23, '51', 'S??lido', 'V', '[Ar]3d??4s??', 3),
        (25, 'Cr??mio', 24, '52', 'S??lido', 'Cr', '[Ar]3d???4s??', 3),
        (26, 'Mangan??s', 25, '55', 'S??lido', 'Mn', '[Ar]3d???4s??', 3),
        (27, 'Ferro', 26, '56', 'S??lido', 'Fe', '[Ar]3d???4s??', 3),
        (28, 'Cobalto', 27, '59', 'S??lido', 'Co', '[Ar]3d???4s??', 3),
        (29, 'N??quel', 28, '59', 'S??lido', 'Ni', '[Ar]3d???4s??', 3),
        (30, 'Cobre', 29, '64', 'S??lido', 'Cu', '[Ar]3d????4s??', 3),
        (31, 'Zinco', 30, '66', 'S??lido', 'Zn', '[Ar]3d????4s??', 3),
        (32, 'G??lio', 31, '70', 'S??lido', 'Ga', '[Ar]3d????4s??4p??', 10),
        (33, 'Germ??nio', 32, '73', 'S??lido', 'Ge', '[Ar]3d????4s??4p??', 7),
        (34, 'Ars??nio', 33, '75', 'S??lido', 'As', '[Ar]3d????4s??4p??', 7),
        (35, 'Sel??nio', 34, '79', 'S??lido', 'Se', '[Ar]3d????4s??4p???', 8),
        (36, 'Bromo', 35, '80', 'L??quido', 'Br', '[Ar]3d????4s??4p???', 9),
        (37, 'Cript??nio', 36, '84', 'Gasoso', 'Kr', '[Ar]3d????4s??4p???', 6),
        (38, 'Rub??dio', 37, '86', 'S??lido', 'Rb', '[Kr]5s??', 1),
        (39, 'Estr??ncio', 38, '88', 'S??lido', 'Sr', '[Kr]5s??', 2),
        (40, '??trio', 39, '89', 'S??lido', 'Y', '[Kr]4d??5s??', 3),
        (41, 'Z??rc??nio', 40, '91', 'S??lido', 'Zr', '[Kr]4d??5s??', 3),
        (42, 'Ni??bio', 41, '93', 'S??lido', 'Nb', '[Kr]4d???5s??', 3),
        (43, 'Molibd??nio', 42, '96', 'S??lido', 'Mo', '[Kr]4d???5s??', 3),
        (44, 'Tecn??cio', 43, '98', 'S??lido', 'Tc', '[Kr]4d???5s??', 3),
        (45, 'Rut??nio', 44, '101', 'S??lido', 'Ru', '[Kr]4d???5s??', 3),
        (46, 'R??dio', 45, '103', 'S??lido', 'Rh', '[Kr]4d???5s??', 3),
        (47, 'Pal??dio', 46, '107', 'S??lido', 'Pd', '[Kr]4d????', 3),
        (48, 'Prata', 47, '108', 'S??lido', 'Ag', '[Kr]4d????5s??', 3),
        (49, 'C??dmio', 48, '113', 'S??lido', 'Cd', '[Kr]4d????5s??', 3),
        (50, '??ndio', 49, '115', 'S??lido', 'In', '[Kr]4d????5s??5p??', 10),
        (51, 'estanho', 50, '119', 'S??lido', 'Sn', '[Kr]4d????5s??5p??', 10),
        (52, 'Antim??nio', 51, '122', 'S??lido', 'Sb', '[Kr]4d????5s??5p??', 7),
        (53, 'Tel??rio', 52, '128', 'S??lido', 'Te', '[Kr]4d????5s??5p???', 7),
        (54, 'Iodo', 53, '127', 'S??lido', 'I', '[Kr]4d????5s??5p???', 9),
        (55, 'Xen??nio', 54, '131', 'Gasoso', 'Xe', '[Kr]4d????5s??5p???', 6),
        (56, 'C??sio', 55, '133', 'S??lido', 'Cs', '[Xe]6s??', 1),
        (57, 'B??rio', 56, '137', 'S??lido', 'Ba', '[Xe]6s??', 2),
        (58, 'Lant??nio', 57, '139', 'S??lido', 'La', '[Xe]5d??6s??', 4),
        (59, 'C??rio', 58, '140', 'S??lido', 'Ce', '[Xe]4f??5d??6s??', 4),
        (60, 'Praseod??mio', 59, '141', 'S??lido', 'Pr', '[Xe]4f??6s??', 4),
        (61, 'Neod??mio', 60, '144', 'S??lido', 'Nd', '[Xe]4f???6s??', 4),
        (62, 'Prom??cio', 61, '145', 'S??lido', 'Pm', '[Xe]4f???6s??', 4),
        (63, 'Sam??rio', 62, '150', 'S??lido', 'Sm', '[Xe]4f???6s??', 4),
        (64, 'Eur??pio', 63, '152', 'S??lido', 'Eu', '[Xe]4f???6s??', 4),
        (65, 'Gadol??nio', 64, '157', 'S??lido', 'Gd', '[Xe]4f???5d??6s??', 4),
        (66, 'T??rbio', 65, '159', 'S??lido', 'Tb', '[Xe]4f???6s??', 4),
        (67, 'Dispr??sio', 66, '163', 'S??lido', 'Dy', '[Xe]4f????6s??', 4),
        (68, 'H??lmio', 67, '165', 'S??lido', 'Ho', '[Xe]4f????6s??', 4),
        (69, '??rbio', 68, '167', 'S??lido', 'Er', '[Xe]4f????6s??', 4),
        (70, 'T??lio', 69, '169', 'S??lido', 'Tm', '[Xe]4f????6s??', 4),
        (71, 'It??rbio', 70, '173', 'S??lido', 'Yb', '[Xe]4f?????6s??', 4),
        (72, 'Lut??cio', 71, '175', 'S??lido', 'Lu', '[Xe]4f?????5d??6s??', 4),
        (73, 'H??fnio', 72, '178', 'S??lido', 'Hf', '[Xe]4f?????5d??6s??', 3),
        (74, 'T??ntalo', 73, '181', 'S??lido', 'Ta', '[Xe]4f?????5d??6s??', 3),
        (75, 'Tungst??nio', 74, '184', 'S??lido', 'W', '[Xe]4f?????5d???6s??', 3),
        (76, 'R??nio', 75, '186', 'S??lido', 'Re', '[Xe]4f?????5d???6s??', 3),
        (77, '??smio', 76, '190', 'S??lido', 'Os', '[Xe]4f?????5d???6s??', 3),
        (78, '??ridio', 77, '192', 'S??lido', 'Ir', '[Xe]4f?????5d???6s??', 3),
        (79, 'Platina', 78, '195', 'S??lido', 'Pt', '[Xe]4f?????5d???6s??', 3),
        (80, 'Ouro', 79, '197', 'S??lido', 'Au', '[Xe]4f?????5d????6s??', 3),
        (81, 'Merc??rio', 80, '201', 'L??quido', 'Hg', '[Xe]4f?????5d????6s??', 3),
        (82, 'T??lio', 81, '204', 'S??lido', 'Ti', '[Xe]4f?????5d????6s??6p??', 10),
        (83, 'Chumbo', 82, '204', 'S??lido', 'Pb', '[Xe]4f?????5d????6s??6p??', 10),
        (84, 'Bismuto', 83, '209', 'S??lido', 'Bi', '[Xe]4f?????5d????6s??6p??', 10),
        (85, 'Pol??nio', 84, '209', 'S??lido', 'Po', '[Xe]4f?????5d????6s??6p???', 7),
        (86, 'Astato', 85, '210', 'S??lido', 'At', '[Xe]4f?????5d????6s??6p???', 8),
        (87, 'Rad??nio', 86, '222', 'Gasoso', 'Rn', '[Xe]4f?????5d????6s??6p???', 6),
        (88, 'Fr??ncio', 87, '223', 'S??lido', 'Fr', '[Rn]7s??', 1),
        (89, 'R??dio', 88, '226', 'S??lido', 'Ra', '[Rn]7s??', 2),
        (90, 'Act??nio', 89, '227', 'S??lido', 'Ac', '[Rn]6d??7s??', 5),
        (91, 'T??rio', 90, '232', 'S??lido', 'Th', '[Rn]6d??7s??', 5),
        (92, 'Protact??nio', 91, '231', 'S??lido', 'Pa', '[Rn]5f??6d??7s??', 5),
        (93, 'Ur??nio', 92, '238', 'S??lido', 'U', '[Rn]5f??6d??7s??', 5),
        (94, 'Nept??nio', 93, '237', 'S??lido', 'Np', '[Rn]5f???6d??7s??', 5),
        (95, 'Plut??nio', 94, '244', 'S??lido', 'Pu', '[Rn]5f???7s??', 5),
        (96, 'Amer??cio', 95, '243', 'S??lido', 'Am', '[Rn]5f???7s??', 5),
        (97, 'C??rio', 96, '247', 'S??lido', 'Cm', '[Rn]5f???6d??7s??', 5),
        (98, 'Berqu??lio', 97, '247', 'S??lido', 'Bk', '[Rn]5f???7s??', 5),
        (99, 'Calif??rnio', 98, '251', 'S??lido', 'Cf', '[Rn]5f????7s??', 5),
        (100, 'Einst??nio', 99, '252', 'S??lido', 'Es', '[Rn]5f????7s??', 5),
        (101, 'F??rmio', 100, '257', 'S??lido', 'Fm', '[Rn]5f????7s??', 5),
        (102, 'Mendel??vio', 101, '258', 'S??lido', 'Md', '[Rn]5f????7s??', 5),
        (103, 'Nob??lio', 102, '259', 'S??lido', 'No', '[Rn]5f?????7s??', 5),
        (104, 'Laur??ncio', 103, '262', 'S??lido', 'Lr', '[Rn]5f?????7s??7p??', 5),
        (105, 'Rutherf??rdio', 104, '267', 'S??lido', 'Rf', '[Rn]5f?????6d??7s??', 3),
        (106, 'D??bnio', 105, '268', 'S??lido', 'Db', '[Rn]5f?????6d??7s??', 3),
        (107, 'Seab??rgio', 106, '269', 'S??lido', 'Sg', '[Rn]5f?????6d???7s??', 3),
        (108, 'B??hrio', 107, '270', 'S??lido', 'Bh', '[Rn]5f?????6d???7s??', 3),
        (109, 'H??ssio', 108, '269', 'S??lido', 'Hs', '[Rn]5f?????6d???7s??', 3),
        (110, 'Meitn??rio', 109, '278', 'S??lido', 'Mt', '[Rn]5f?????6d???7s??', 3),
        (111, 'Darmst??dtio', 110, '281', 'S??lido', 'Ds', '[Rn]5f?????6d???7s??', 3),
        (112, 'Roentg??nio', 111, '280', 'S??lido', 'Rg', '[Rn]5f?????6d????7s??', 3),
        (113, 'Copern??cio', 112, '285', 'L??quido', 'Cn', '[Rn]5f?????6d????7s??', 3),
        (114, 'Nih??nio', 113, '286', 'S??lido', 'Nh', '[Rn]5f?????6d????7s??7p??', 10),
        (115, 'Fler??vio', 114, '289', 'S??lido', 'Fl', '[Rn]5f?????6d????7s??7p??', 10),
        (116, 'Mosc??vio', 115, '289', 'S??lido', 'Mc', '[Rn]5f?????6d????7s??7p??', 10),
        (117, 'Liverm??rio', 116, '293', 'Gasoso', 'Lv', '[Rn]5f?????6d????7s??7p???', 10),
        (118, 'Tennesso', 117, '294', 'S??lido', 'Ts', '[Rn]5f?????6d????7s??7p???', 9),
        (119, 'Oganess??nio', 118, '294', 'S??lido', 'Og', '[Rn]5f?????6d????7s??7p???', 6)
    ])

cursor.execute('select * from tabelaperiodica.elemento')
print(' ------------ Elementos: ------------ ')
for elemento in cursor.fetchall():
    print(elemento[1])

cursor.executemany(
    'INSERT INTO `curiosidade` (`id_curiosidade`, `tipo`, `descricao`, `elemento`) VALUES (%s, %s, %s, %s)',
    [
        (1, 'Propriedades', 'Ocorre como um g??s incolor, inodoro e altamente inflam??vel. ?? o elemento de menor densidade da Tabela Peri??dica e por este motivo era utilizado no enchimento de dirig??veis, mas teve seu uso abolido devido ?? elevada inflamabilidade.', 1),
        (2, 'Abund??ncia', 'O hidrog??nio ?? o elemento mais abundante do universo. Sendo encontrado no sol, na maioria das estrelas e o principal constituinte do planeta J??piter.', 1),
        (3, 'Usos', 'O g??s hidrog??nio (H2) ?? considerado\no combust??vel limpo do futuro, uma vez que sua combust??o produz ??gua. A eletr??lise da ??gua constitui um dos principais m??todos de obten????o do g??s hidrog??nio.', 1),
        (4, 'Propriedades', 'O h??lio ?? o segundo elemento menos denso da Tabela Peri??dica, e por este motivo ?? comumente usado no enchimento de bal??es decorativos, bem como de bal??es meteorol??gicos ou dirig??veis.', 2),
        (5, 'Origem do nome', 'O nome h??lio vem da palavra grega ???helios??? que significa ???SOL???. O h??lio ?? o principal componente do sol, onde ?? formado pela fus??o nuclear de ??tomos de hidrog??nio, processo que libera uma quantidade alt??ssima de energia.', 2),
        (6, 'Usos', 'Devido ao seu baix??ssimo ponto de congelamento, o h??lio ?? usado em\r\ncrioscopia como meio de resfriamento de equipamentos diversos como os espectr??metros de RMN e para resfriar o combust??vel de ve??culos espaciais.', 2),
    ])

cursor.execute('select * from tabelaperiodica.curiosidade')
print(' ------------ Curiosidades: ------------ ')
for curiosidade in cursor.fetchall():
    print(curiosidade[1])

cursor.executemany(
    'INSERT INTO `usuario` (`id_usuario`, `usuario`,`nome_usuario`, `email_usuario`, `senha`) VALUES (%s, %s, %s, %s, %s)',
    [
        (1,'amanda', 'Amanda Eleut??rio', 'amanda2@gmail.com', '54321'),
        (2,'daiane', 'Daiane Cristina', 'daiane@gmail.com', '54321'),
        (3,'tiago', 'Tiago Carlos', 'tiago@gmail.com', '54321'),
    ])

cursor.execute('select * from tabelaperiodica.usuario')
print(' ------------ Usu??rio: ------------ ')
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
print(' ------------ Tipo de Usu??rio: ------------ ')
for tipo_usuario in cursor.fetchall():
    print(tipo_usuario[1])


cursor.executemany(
    'INSERT INTO `nivel` (`id_nivel`, `nome_nivel`) VALUES(%s, %s)',
    [
        (1, 'F??cil'),
        (2, 'M??dio'),
        (3, 'Dif??cil'),
    ])

cursor.execute('select * from tabelaperiodica.nivel')
print(' ------------ N??vel: ------------ ')
for nivel in cursor.fetchall():
    print(nivel[1])
conn.commit()
cursor.close()
