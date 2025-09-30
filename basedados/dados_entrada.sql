-- incluindo as fases do cultivo
insert into dashboard.fases_cultura (nome, descricao, data_criacao) values ('Etapa1', 'Etapa 1 - Vegetativo', now());
insert into dashboard.fases_cultura (nome, descricao, data_criacao) values ('Etapa2', 'Etapa 2 - Início da fase reprodutiva', now());
insert into dashboard.fases_cultura (nome, descricao, data_criacao) values ('Etapa3', 'Etapa 3 - Final fase reprodutiva, maturação e colheita', now());


--  incluindo os tipos de despesas guarda-chuva
insert into dashboard.tipos_despesas_guarda_chuva (nome, descricao, data_criacao) values ('MÃO DE OBRA', 'A. MÃO DE OBRA (CEPEA/AMPA CONAB)', now()),
                                                                                         ('MANUTENÇÃO', 'B. MANUTENÇÃO', now()),
                                                                                         ('IMPOSTOS E TAXAS', 'C. IMPOSTOS E TAXAS', now()),
                                                                                         ('FINANCEIRAS', 'D. FINANCEIRAS', now()),
                                                                                         ('OUTROS CUSTOS', 'E. OUTROS CUSTOS', now());


-- incluindo as especialiddes dos tipos de despesas guarda-chuva
insert into dashboard.detalhes_tipos_despesa_guarda_chuva(tipo_despesas_id, nome, data_criacao) values (1,'Permanente', now()),
                                                                                                    (1, 'Temporária', now()),
                                                                                                    (2,'Manutenção Máquinas Equipamentos Utilit.', now()),
                                                                                                    (2, 'Manutenção Benfeitorias',now() ),
                                                                                                    (3, 'Funrural',now()),
                                                                                                    (3, 'Fethab I',now()),
                                                                                                    (3, 'Fethab II',now()),
                                                                                                    (3, 'ITR',now()),
                                                                                                    (3, 'IMA - MT',now()),
                                                                                                    (3, 'Outros Impostos e Taxas 1',now()),
                                                                                                    (3, 'Outros Impostos e Taxas 2',now()),
                                                                                                    (3, 'Outros Impostos e Taxas 3',now()),
                                                                                                    (3, 'Outros Impostos e Taxas 4',now()),
                                                                                                    (4, 'Financiamentos (taxas, IOF, juros)',now()),
                                                                                                    (4, 'Seguro da Produção',now()),
                                                                                                    (4, 'Seguro Maquinário Equipamentos Utilit.',now()),
                                                                                                    (5,'Assistência Técnica', now()),
                                                                                                    (5,'Combustível Utilitários', now() ),
                                                                                                    (5, 'Despesas Gerais', now()),
                                                                                                    (5, 'Análise de Solo (A)', now()),
                                                                                                    (5, 'Custo c/ Alimentação', now());


-- incluidos dados de tipos de custos de produção
insert into dashboard.tipos_custos_producao(nome, descricao, data_criacao) values ('SEMENTES', '1 - SEMENTES', now()),
                                                                                  ('FERTILIZANTES','2 - FERTILIZANTES', now()),
                                                                                  ('OPERAÇÕES COM MÁQUINAS', '3 - OPERAÇÕES COM MÁQUINAS', now()),
                                                                                  ('AGROTÓXICOS', '4 - AGROTÓXICOS', now());



-- incluindo dados de detalhes
insert into dashboard.detalhes_tipos_custos_producao(tipo_custo_id, nome, data_criacao) values (1,'Sementes de Algodão', now()),
                                                                                      (1,'Royalteis sementes algodão', now()),
                                                                                      (1,'Sementes de cobertura (pré-plantio de algodão)', now()),
                                                                                      (2,'Corretivos de solo - Calcário / Fósforo / Potássio / Gesso Agrícola', now()),
                                                                                      (2, 'Macronutriente - NPK - Base e Cobertura', now()),
                                                                                      (2,'Micronutriente - Solo e Cobertura', now()),
                                                                                      (3,'Manejo Pré Plantio', now()),
                                                                                      (3,'Adubação e Plantio', now()),
                                                                                      (3,'Aplicações de agrotóxicos e cobertura com máquinas terrestres',now()),
                                                                                      (3, 'Aplicações de agrotóxicos e cobertura com avião agrícola', now()),
                                                                                      (3, 'Colheita', now()),
                                                                                      (3,'Embalagens Colheita (filme plástico) / Utensílios',now()),
                                                                                      (3,'Serviço terceirizado - Aluguel de máquinas e outro', now()),
                                                                                      (3,'Serviço terceirizado - Aluguel de máquinas e outro 1', now()),
                                                                                      (3,'Serviço terceirizado - Aluguel de máquinas e outro 2', now()),
                                                                                      (3,'Serviço terceirizado - Aluguel de máquinas e outro 3', now()),
                                                                                      (3,'Serviço terceirizado - Aluguel de máquinas e outro 4', now()),
                                                                                      (3,'Serviço terceirizado - Aluguel de máquinas e outro 5', now()),
                                                                                      (3,'Irrigação (A)', now()),
                                                                                      (3,'Coleta de imagens multiespectrais com drones (VANTs)', now()),
                                                                                      (4, 'Fungicida', now()),
                                                                                      (4,'Herbicida', now()),
                                                                                      (4,'Inseticida', now()),
                                                                                      (4,'Adjuvantes / Outros (fitohormônios, estimulantes, etc.)', now()),
                                                                                      (4,'Adjuvante / Outros 1', now()),
                                                                                      (4,'Adjuvante / Outros 2', now()),
                                                                                      (4,'Adjuvante / Outros 3', now()),
                                                                                      (4,'Adjuvante / Outros 4', now()),
                                                                                      (4,'Adjuvante / Outros 5', now());



--- simulando dados de fazenda para São Jose
insert into dashboard.fazendas(nome, area_hectares, qtde_talhoes, data_criacao) values ('São José', 350, 4, now() );

-- inserindo talhoes
insert into dashboard.talhoes(fazenda_id, nome, area_hectares, latitude, longitude, data_criacao) values (1,'Talho 1', 50,1.353535,3.3533535,now());
insert into dashboard.talhoes(fazenda_id, nome, area_hectares, latitude, longitude, data_criacao) values (1,'Talho 2', 30,2.353535,5.656565, now());
insert into dashboard.talhoes(fazenda_id, nome, area_hectares, latitude, longitude, data_criacao) values (1,'Talho 3', 10,2.353535,5.656565, now());
insert into dashboard.talhoes(fazenda_id, nome, area_hectares, latitude, longitude, data_criacao) values (1,'Talho 4', 25,2.353535,5.656565, now());


