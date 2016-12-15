INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES
(1, 'pbkdf2_sha256$15000$ZDbgcz8xUd5x$eVFOVXKl6gG1yMp+TmkT/1MNhm6i1hNPJdVvBzV/dUw=', '2015-05-11 23:36:51', 1, 'admin', 'Gustavo', 'Santana de Oliveira', 'gustavo.sdo@gmail.com', 1, 1, '2014-12-31 01:18:00'),
(2, 'pbkdf2_sha256$12000$UjxpI6EkJXg2$GoYKHvFp9n+wGJV3ZiaDwBDqiMISOvHANHbAV27qVjE=', '2015-01-01 01:18:00', 0, 'spossato', 'Stephanie', 'Possato de Oliveira', 'spossato@unipar.br', 1, 1, '2015-01-01 01:18:00');

-- Define a data de abertura do caixa há 7 dias atrás
INSERT INTO caixa_caixa (id, status, data_abertura, data_fechamento, valor_entrada, valor_saida, valor_total, valor_inicial, valor_fechamento, diferenca) VALUES 
(1, 1, DATE_ADD(NOW(), INTERVAL -30 DAY), NULL, 0.00, 0.00, 0.00, 1000.00, 0.00, 0.00);


INSERT INTO configuracoes_parametrizacao (id, quantidade_inlines_compra, quantidade_inlines_venda, habilita_pedido_compra, habilita_pedido_venda, periodo_venc_pedido_compra, periodo_venc_pedido_venda, qtde_minima_produtos_em_estoque, perc_valor_minimo_recebimento, intervalo_dias_entrega_venda, email_abertura_caixa, evento_calendario) VALUES 
(1, 8, 4, 1, 1, 3, 7, 15, 50, 1, '', 'eventos');




INSERT INTO pessoal_cargo VALUES 
(1, 'Secretário atendente', 'Secretário atendente'),
(2, 'Assistente de vendas', 'Assistente de vendas'),
(3, 'Vendedor', 'Vendedor'),
(4, 'Gerente', 'Gerente');





--
-- Extraindo dados da tabela `pessoal_cliente`
--

INSERT INTO `pessoal_cliente` (`id`, `nome`, `data_nasc`, `cpf`, `rg`, `sexo`, `estado_civil`, `endereco`, `numero`, `bairro`, `complemento`, `estado`, `cep`, `telefone`, `celular`, `email`, `data`, `status`, `observacao`, `foto`, `tipo_pessoa`, `cnpj`, `razao_social`, `cidade_id`) VALUES
(1, 'Bryan Danilo Julio Barbosa', '1993-07-02', '72746759829', '206185133', 'M', 'solteiro', 'Travessa do Poço', '386', 'Arenoso', '', 'BA', '41211-440', '44-3021-8921', '44-2025-8082', 'bryan@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 616),
(2, 'Caio Felipe Moura', '1997-05-02', '85198464678', '324444618', 'M', 'viuvo', 'Raimundo Andrade de Lima', '946', 'Presidente Costa e Silva', '', 'RN', '59625-578', '11-3056-3350', '11-98738-0341', 'caio@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 3769),
(3, 'Iago Lucca Lima', '1996-12-12', '36355164227', '112074716', 'M', 'separado_judicialmente', 'Vila do Apertar da Hora', '319', 'Zona Rural', '', 'PE', '56140-973', '', '', 'iago@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 3342),
(4, 'Murilo Erick Dias', '1990-12-21', '36732214268', '509581274', 'M', 'solteiro', 'Rua do Himaláia', '622', 'Vila Marcos Roberto', '', 'MS', '79080-490', '40-2943-5082', '', 'murilo@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 1506),
(5, 'Caio Thales Iago Araújo', '1991-02-12', '60258932333', '472976813', 'M', 'marital', 'Viola de Cocho', '564', 'Capão do Pequi', '', 'MT', '78134-314', '44-8053-2553', '', 'caio@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 1483),
(6, 'Lorena Fernanda Rodrigues', '1985-01-18', '78636719305', '340919668', 'F', 'separado_judicialmente', 'Cinqüenta e Seis', '682', 'João de Deus', '', 'PE', '56316-566', '11-20354-2410', '11-80358-5100', '', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 3309),
(7, 'Betina Gabrielly Cavalcanti', '1985-11-02', '72278459821', '492242082', 'F', 'viuvo', 'Chororó', '436', 'Padre Ulrico', '', 'PR', '85604-538', '11-21844-4281', '', 'betina@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 2907),
(8, 'Letícia Julia Caroline Araújo', '1985-07-26', '63079802306', '372385035', 'F', 'solteiro', 'Travessa Boa Esperança', '788', 'Santa Amélia', '', 'AL', '57063-883', '', '44-9252-3541', 'leticia@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 147),
(9, 'Laís Isabella Amanda Gomes', '1985-05-01', '54332683145', '290232119', 'F', 'viuvo', 'Roberto Scarpa', '850', 'Jardim Caieira', '', 'SP', '13483-214', '44-3621-2486', '', 'lais@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 5011),
(10, 'Julia Milena Cardoso', '1985-05-12', '20711053200', '352385431', 'F', 'casado', 'Piedade', '175', 'São Francisco', '', 'MS', '79118-250', '', '', 'julia@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 1506),
(11, 'Natasha Romanoff', NULL, NULL, '', 'F', '', 'Avenida Caiano', '422', 'Fazenda Grande do Retiro', '', 'BA', '40355-540', '', '', 'natasha@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 616);

-- --------------------------------------------------------



--
-- Extraindo dados da tabela `pessoal_fornecedor`
--

INSERT INTO `pessoal_fornecedor` (`id`, `nome`, `data_nasc`, `cpf`, `rg`, `sexo`, `estado_civil`, `endereco`, `numero`, `bairro`, `complemento`, `estado`, `cep`, `telefone`, `celular`, `email`, `data`, `status`, `observacao`, `foto`, `tipo_pessoa`, `cnpj`, `razao_social`, `cidade_id`) VALUES
(1, 'Daenerys Targaryen', '1985-08-24', '78905880380', '402801751', 'F', 'uniao_estavel', 'Avenida Atlântica', '807', 'Morada do Vale', '', 'MG', '', '', '', 'daenerys@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 1778),
(2, 'Violet Crowley', '1985-08-17', '62556153083', '450067142', 'F', 'viuvo', 'Rua Catorze', '307', 'Três Barras', '', 'MT', '', '', '44-5031-6441', 'volet@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 1383),
(3, 'Amy Farrah Fowler', '1996-10-14', '81799502988', '462538746', 'F', 'uniao_estavel', 'Travessa Cristalina', '126', 'Paciência', '', 'RJ', '', '', '11-3056-3166', 'amy@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 3658),
(4, 'Katniss Everdeen', '1991-02-03', '31136580638', '268445369', 'F', 'solteiro', 'Travessa Ivone Franca', '925', 'Centro', '', 'RJ', '26525-230', '', '44-2025-3125', 'katniss@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 3637),
(5, 'Hermione Granger', '1993-12-15', '17303391584', '181593579', 'F', 'separado', 'Rua Carlos Menotti', '450', 'Parque Residencial Servantes II', '', 'SP', '', '', '', 'hermione@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 5172),
(6, 'Lara Croft', '1988-11-14', '76627722763', '360369388', 'F', 'divorciado', 'Avenida Barão de Nazaré', '911', 'São José', '', 'PE', '55295-135', '21-4622-8222', '', 'lara@estagio.com', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 3249),
(7, 'Hua Mulan', '1988-11-08', '39458489385', '422834658', 'F', 'marital', 'Travessa Wilson', '535', 'Fazenda Grande do Retiro', '', 'BA', '40350-400', '21-3363-9883', '', 'mulan@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 290),
(8, 'Shmi Skywalker', '1994-11-06', '56636906979', '185890672', 'M', 'solteiro', 'Manoel João Machado', '509', 'Metropol', '', 'SC', '88819-000', '21-4455-8785', '', 'skywalker@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 4487),
(9, 'Lily Potter', '1985-06-14', '79344554293', '362135691', 'F', 'marital', 'Rua Olinda', '913', 'Artur Lundgren II', '', 'PE', '53416-570', '', '', 'potter@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 3305),
(10, 'Martha Kent', '1982-12-12', '65870247934', '264739711', 'F', 'casado', 'Doutor João Costa', '550', 'Bongi', '', 'PE', '50760-510', '11-30323-2526', '', 'martha@estagio.com.br', '2015-10-27 01:03:05.450810', 1, '', '', 'PF', NULL, NULL, 3315),
(11, 'Sarah Connor', NULL, NULL, '303786061', 'F', '', 'Rua dos Cravinhos', '314', 'Serra Dourada', '', 'MT', '78056-243', '44-4044-3021', '', 'sarah@estagio.com.br', '2015-10-27 01:03:05.450810', 1, 'http://www.4devs.com.br/gerador_de_pessoas', '', 'PF', NULL, NULL, 1383),
(12, 'Julio e Lavínia Materiais ME', '1970-02-12', NULL, '', NULL, '', 'Avenida das Nações Unidas', '709', 'Centro', '', 'SP', '09726-110', '44-2035-8085', '', 'jlmateriais@estagio.com.br', '2015-10-27 01:03:05.450810', 1, 'Inscrição estadual: 455561772582.\r\n\r\nhttp://www.4devs.com.br/gerador_de_empresas', '', 'PJ', '98840109000131', '', 5252);

-- --------------------------------------------------------



--
-- Extraindo dados da tabela `pessoal_funcionario`
--

INSERT INTO `pessoal_funcionario` (`id`, `nome`, `data_nasc`, `cpf`, `rg`, `sexo`, `estado_civil`, `endereco`, `numero`, `bairro`, `complemento`, `estado`, `cep`, `telefone`, `celular`, `email`, `data`, `status`, `observacao`, `foto`, `salario`, `cargo_id`, `cidade_id`, `usuario_id`) VALUES
(1, 'Padmé Amidala', NULL, NULL, '', 'F', 'solteiro', 'Rua Mogi das Cruzes', '680', 'Vila Santo Antônio', '', 'PR', '87502-120', '11-26234-0400', '', 'padme@gmail.com', '2015-10-27 01:03:05.450810', 1, '', '', NULL, 2, 3172, NULL);

--


INSERT INTO parametros_financeiros_formapagamento (id, nome, descricao, quant_parcelas, prazo_entre_parcelas, tipo_prazo, carencia, tipo_carencia, status) VALUES 
(1, 'À vista','Pagamento efetuado à vista.', 1, 0, 'M', 0, 'M', 1),
(2, 'À prazo (Mensal, Entrada + 2x)', 'Pagamento parcelado em 3 vezes, com acerto da primeira parcela no ato da compra.', 3, 1, 'M', 0, 'M', 1),
(3, 'À prazo (Mensal, em 6x - Prazo: 1M - Carência: 2S)', 'Pagamento parcelado em 6 vezes, com primeiro pagamento para duas semanas.', 6, 1, 'M', 2, 'S', 1),
(4, 'À prazo (Semanal, em 3x - Prazo: 2S - Carência: 1D) ', 'Pagamento parcelado em 3 vezes, com prazo entre parcelas de 2 semanas e carência de 1 dia.', 3, 2, 'S', 1, 'D', 1),
(5, 'À prazo (Diário, em 5x - Prazo: 3D - Carência: 1M) ', 'Pagamento parcelado em 5 vezes, com prazo entre parcelas de 3 dias e carência de 1 mês.', 5, 3, 'D', 1, 'M', 1);


INSERT INTO parametros_financeiros_grupoencargo (id, nome, multa, juros, tipo_juros, status, padrao) VALUES 
(1, 'Grupo de encargos Padrão', 2, 0.0333, 'S', 1, 1);


INSERT INTO schedule_calendar (id, name, slug) VALUES
(1, 'Eventos', 'eventos');


INSERT INTO schedule_rule (id, name, description, frequency, params) VALUES
(1, 'Aniversário', 'Evento realizado anualmente.', 'YEARLY', ''),
(2, 'Feriado', 'Evento realizado anualmente', 'YEARLY', '');


INSERT INTO schedule_event (id, start, end, title, description, created_on, updated_on, end_recurring_period, color_event, calendar_id, creator_id, rule_id) VALUES
(1, '1993-11-06 02:00:00.000000', '1993-11-07 01:59:59.000000', 'Aniversário do Gustavo', 'Comprar presentes para o chefe!!', '2015-08-24 02:07:35.684113', '2015-08-24 02:28:23.939942', NULL, '#f1c232', 1, NULL, 1),
(2, '2000-01-01 02:00:00.000000', '2000-01-01 02:00:00.000000', 'Feriado “Confraternização Universal”', 'Recesso Administrativo', '2015-08-24 02:48:39.352469', '2015-08-24 02:50:06.415693', NULL, '', 1, NULL, 2),
(3, '2000-02-16 02:00:00.000000', '2000-02-18 02:00:00.000000', 'Feriado “Carnaval”', 'Recesso Administrativo', '2015-08-24 02:50:13.508466', '2015-08-24 02:50:13.508466', NULL, '', 1, NULL, 2),
(4, '2000-04-21 03:00:00.000000', '2000-04-21 03:00:00.000000', 'Feriado “Tiradentes” ', 'Recesso Administrativo', '2015-08-24 02:52:26.440734', '2015-08-24 02:52:26.440734', NULL, '', 1, NULL, 2),
(5, '2000-04-02 03:00:00.000000', '2000-04-04 03:00:00.000000', 'Feriado “Paixão de Cristo” ', 'Recesso Administrativo', '2015-08-24 02:53:12.523636', '2015-08-24 02:53:12.523636', NULL, '', 1, NULL, 2),
(6, '2000-10-04 03:00:00.000000', '2000-10-04 03:00:00.000000', 'Feriado Municipal de Umuarama', 'Recesso Administrativo', '2015-08-24 02:59:59.028659', '2015-08-24 02:59:59.028659', NULL, '', 1, NULL, 2);


UPDATE  django_site 
SET     domain = 'localhost:8000', name = 'summum.com'
WHERE   id = 1;