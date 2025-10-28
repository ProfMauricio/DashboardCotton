
-- criar o esquema dashboard
CREATE SCHEMA IF NOT EXISTS dashboard;


-- criar uma tabela de fases da cultura
CREATE TABLE IF NOT EXISTS dashboard.fases_cultura (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL UNIQUE,
    descricao TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    safra varchar(10) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- tabela de posição geográfica dos blocos
CREATE TABLE IF NOT EXISTS dashboard.blocos (
    id SERIAL PRIMARY KEY,
    talhao_id INT REFERENCES dashboard.talhoes(id) ON DELETE CASCADE,
    bloco INT,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
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
CREATE TABLE IF NOT EXISTS dashboard.detalhes_tipos_despesa_guarda_chuva (
    id SERIAL PRIMARY KEY,
    tipo_despesas_id INT REFERENCES dashboard.tipos_despesas_guarda_chuva(id) ON DELETE SET NULL,
    nome VARCHAR(255) NOT NULL UNIQUE,
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
CREATE TABLE IF NOT EXISTS dashboard.detalhes_tipos_custos_producao (
    id SERIAL PRIMARY KEY,
    tipo_custo_id INT REFERENCES dashboard.tipos_custos_producao(id) ON DELETE SET NULL,
    nome VARCHAR(255) NOT NULL UNIQUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- criar a tabela de despesas da fazenda (guarda chuva)
CREATE TABLE IF NOT EXISTS dashboard.gestao_custos_despesas_guarda_chuva_fazenda (
    id SERIAL PRIMARY KEY,
    fazenda_id INT REFERENCES dashboard.fazendas(id) ON DELETE CASCADE,
    detalhes_tipo_custo_id INT REFERENCES dashboard.detalhes_tipos_despesa_guarda_chuva(id) ON DELETE SET NULL,
    valor DECIMAL(10, 2) NOT NULL,
    safra varchar(10) NOT NULL,
    descricao TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- criar a tabela de custo de producao por etapa e talhão (custo por etapa)
CREATE TABLE IF NOT EXISTS dashboard.gestao_custos_producao_por_talhao (
    id SERIAL PRIMARY KEY,
    talhao_id INT REFERENCES dashboard.talhoes(id) ON DELETE CASCADE,
    custo_especificacao_id INT REFERENCES dashboard.detalhes_tipos_custos_producao(id) ON DELETE SET NULL,
    valor DECIMAL(10, 2) NOT NULL,
    safra varchar(10) NOT NULL,
    fase_cultura_id INT REFERENCES dashboard.fases_cultura(id) ON DELETE SET NULL,
    descricao TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- tabela de manejo agrícola por talhão
CREATE TABLE IF NOT EXISTS dashboard.gestao_agricola_talhao (
    id SERIAL PRIMARY KEY,
    talhao_id INT REFERENCES dashboard.talhoes(id) ON DELETE CASCADE,
    fase_cultura_id INT REFERENCES dashboard.fases_cultura(id) ON DELETE SET NULL,
    safra varchar(10) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- tabela de elementos por manejo agrícola por bloco
CREATE TABLE IF NOT EXISTS dashboard.gestao_agricola_medidas_elementos_horizonte (
    id SERIAL PRIMARY KEY,
    bloco_id INT REFERENCES dashboard.blocos(id) ON DELETE CASCADE,
    fase_cultura_id INT REFERENCES dashboard.fases_cultura(id) ON DELETE SET NULL,
    gestao_agricola_talhao_id INT REFERENCES dashboard.gestao_agricola_talhao(id) ON DELETE SET NULL,
    horizonte VARCHAR(50) NOT NULL,
    ph_h2o double precision NOT NULL,
    ph_cacl2 double precision NOT NULL,
    P_resina double precision NOT NULL,
    K_trocavel double precision NOT NULL,
    MO double precision NOT NULL,
    Ca double precision NOT NULL,
    Zn double precision NOT NULL,
    B double precision NOT NULL,
    Mn double precision NOT NULL,
    Fe double precision NOT NULL,
    Na double precision NOT NULL,
    S double precision NOT NULL,
    Mg double precision NOT NULL,
    Elementos_baixo TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- tabela de indices calculados por manejo agrícola por bloco
CREATE TABLE IF NOT EXISTS dashboard.gestao_agricola_indices_calculados_talhao (
    id SERIAL PRIMARY KEY,
    bloco_id INT REFERENCES dashboard.blocos(id) ON DELETE CASCADE,
    fase_cultura_id INT REFERENCES dashboard.fases_cultura(id) ON DELETE SET NULL,
    gestao_agricola_talhao_id INT REFERENCES dashboard.gestao_agricola_talhao(id) ON DELETE SET NULL,
    ndvi double precision NOT NULL,
    savi double precision NOT NULL,
    gli double precision NOT NULL,
    tx_ocupacao double precision NOT NULL,
    status_term VARCHAR(100) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



