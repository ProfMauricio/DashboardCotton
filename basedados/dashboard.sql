
-- criar o esquema dashboard
CREATE SCHEMA IF NOT EXISTS dashboard;



-- criar a tabela de fazendas
CREATE TABLE IF NOT EXISTS dashboard.fazendas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    area_hectares DECIMAL(10, 2) NOT NULL,
    qtde_talhoes INT NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- criar a tabela de talhoes
CREATE TABLE IF NOT EXISTS dashboard.talhoes (
    id SERIAL PRIMARY KEY,
    fazenda_id INT REFERENCES dashboard.fazendas(id) ON DELETE CASCADE,
    nome VARCHAR(255) NOT NULL,
    area_hectares DECIMAL(10, 2) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- criar a tabela de tipos de despesas
CREATE TABLE IF NOT EXISTS dashboard.tipos_despesas_guarda_chuva (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL UNIQUE,
    descricao TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- criar a tabela especializada de despesas
CREATE TABLE IF NOT EXISTS dashboard.detalhes_despesa_guarda_chuva (
    id SERIAL PRIMARY KEY,
    tipo_despesas_id INT REFERENCES dashboard.tipos_despesas_guarda_chuva(id) ON DELETE SET NULL,
    nome VARCHAR(255) NOT NULL UNIQUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- criar uma tabela de fases da cultura
CREATE TABLE IF NOT EXISTS dashboard.fases_cultura (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL UNIQUE,
    descricao TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- criar a tabela de tipos de custos de produção
CREATE TABLE IF NOT EXISTS dashboard.tipos_custos_producao (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL UNIQUE,
    descricao TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- criar a tabela de especificações de custos de produção
CREATE TABLE IF NOT EXISTS dashboard.detalhes_custos_producao (
    id SERIAL PRIMARY KEY,
    tipo_custo_id INT REFERENCES dashboard.tipos_custos_producao(id) ON DELETE SET NULL,
    nome VARCHAR(255) NOT NULL UNIQUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- criar a tabela de despesas da fazenda (guarda chuva)
CREATE TABLE IF NOT EXISTS dashboard.despesas_guarda_chuva_fazenda (
    id SERIAL PRIMARY KEY,
    fazenda_id INT REFERENCES dashboard.fazendas(id) ON DELETE CASCADE,
    despesa_especificacao_id INT REFERENCES dashboard.detalhes_despesa_guarda_chuva(id) ON DELETE SET NULL,
    valor DECIMAL(10, 2) NOT NULL,
    data_despesa DATE,
    fase_cultura_id INT REFERENCES dashboard.fases_cultura(id) ON DELETE SET NULL,
    descricao TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- criar a tabela de custo de producao por etapa e talhão (custo por etapa)
CREATE TABLE IF NOT EXISTS dashboard.custos_producao_talhao (
    id SERIAL PRIMARY KEY,
    talhao_id INT REFERENCES dashboard.talhoes(id) ON DELETE CASCADE,
    custo_especificacao_id INT REFERENCES dashboard.detalhes_custos_producao(id) ON DELETE SET NULL,
    valor DECIMAL(10, 2) NOT NULL,
    data_custo DATE,
    fase_cultura_id INT REFERENCES dashboard.fases_cultura(id) ON DELETE SET NULL,
    descricao TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- tabela de posição geográfica dos blocos
CREATE TABLE IF NOT EXISTS dashboard.blocos (
    id SERIAL PRIMARY KEY,
    fazenda_id INT REFERENCES dashboard.fazendas(id) ON DELETE CASCADE,
    talhao_id INT REFERENCES dashboard.talhoes(id) ON DELETE CASCADE,
    bloco INT,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- tabela de manejo agrícola por talhão
CREATE TABLE IF NOT EXISTS dashboard.manejo_agricola_talhao (
    id SERIAL PRIMARY KEY,
    talhao_id INT REFERENCES dashboard.talhoes(id) ON DELETE CASCADE,
    bloco_id INT REFERENCES dashboard.blocos(id) ON DELETE SET NULL,
    fase_cultura_id INT REFERENCES dashboard.fases_cultura(id) ON DELETE SET NULL,
    ano INT not null,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- tabela de elementos por manejo agrícola por bloco
CREATE TABLE IF NOT EXISTS dashboard.medida_elementos_horizonte (
    id SERIAL PRIMARY KEY,
    manejo_agricola_id INT REFERENCES dashboard.manejo_agricola_talhao(id) ON DELETE CASCADE,
    horizonte VARCHAR(50) NOT NULL,
    ph_h2o DECIMAL(4, 6) NOT NULL,
    ph_cacl2 DECIMAL(4, 6) NOT NULL,
    P_resina DECIMAL(5, 6) NOT NULL,
    K_trocavel DECIMAL(5, 6) NOT NULL,
    MO DECIMAL(5, 6) NOT NULL,
    Ca DECIMAL(5, 6) NOT NULL,
    Zn DECIMAL(5, 6) NOT NULL,
    B DECIMAL(5, 6) NOT NULL,
    Mn DECIMAL(5, 6) NOT NULL,
    Fe DECIMAL(5, 6) NOT NULL,
    Na DECIMAL(5, 6) NOT NULL,
    S DECIMAL(5, 6) NOT NULL,
    Mg DECIMAL(5, 6) NOT NULL,
    Elementos_baixo TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- tabela de indices calculados por manejo agrícola por bloco
CREATE TABLE IF NOT EXISTS dashboard.indices_calculados_talhao (
    id SERIAL PRIMARY KEY,
    manejo_agricola_id INT REFERENCES dashboard.manejo_agricola_talhao(id) ON DELETE CASCADE,
    ndvi DECIMAL(5, 6) NOT NULL,
    savi DECIMAL(5, 6) NOT NULL,
    gli DECIMAL(5, 6) NOT NULL,
    tx_ocupacao DECIMAL(5, 6) NOT NULL,
    status_term VARCHAR(100) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



