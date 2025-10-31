drop materialized view dashboard.v_talhoes;
drop materialized view dashboard.v_indices_calculados;
drop materialized view dashboard.v_indices_solo;
drop materialized view dashboard.v_gestao_guarda_chuva_por_talhao;
drop materialized view dashboard.v_gestao_guarda_chuva_fazenda;


-- View dos talhoes
create materialized view dashboard.v_talhoes as select t.id as "IdTalhao", t.nome as "NomeTalhao", t.area_hectares as "Area" , t.latitude as "Latitude", t.longitude as "Longitude"
from dashboard.talhoes t where t.fazenda_id in (select id from dashboard.fazendas f where f.nome like 'São José') and t.safra = '2025';

-- View dos indices calculados da gestao agricola
create materialized view dashboard.v_indices_calculados as
select gaict.id as "Id",
gaict.bloco_id  as "bloco_id",
b.bloco as "FID",
b.bloco as "bloco",
b.latitude as "latitude",
b.longitude as "longitude",
gaict.ndvi as "ndvi",
gaict.gli  as "gli",
gaict.savi as "savi",
gaict.tx_ocupacao as "taxa_ocupacao",
gaict.status_term as "status_termal",
fc.nome as "fase_cultura"
from dashboard.gestao_agricola_indices_calculados_talhao gaict
inner join dashboard.blocos b on b.id = gaict.bloco_id
inner join dashboard.fases_cultura fc on fc.id = gaict.fase_cultura_id
where gaict.gestao_agricola_talhao_id in
(select gat.id from dashboard.gestao_agricola_talhao gat where gat.safra like '2025' and gat.talhao_id = 1) order by gaict.Id ;


-- view dos indices medidos do solo da gestão agricola
create materialized view dashboard.v_indices_solo as
    select gameh.id as "Id",
gameh.bloco_id  as "bloco_id",
b.bloco as "FID",
b.latitude as "latitude",
b.longitude as "longitude",
gameh.fe as "ferro",
gameh.ca as "cálcio",
gameh.k_trocavel as "k_trocavel",
gameh.horizonte as "horizonte",
gameh.mg as "magnésio",
gameh.mn as "manganês",
gameh.mo as "materia_organica",
gameh.na as "na",
gameh.p_resina as "p_resina",
gameh.ph_cacl2 as "ph_cacl2",
gameh.ph_h2o as "ph_h2o",
gameh.s as "enxofre",
gameh.zn as "zinco",
gameh.elementos_baixo as "elementos_baixo",
fc.nome as "fase_cultura"
from dashboard.gestao_agricola_medidas_elementos_horizonte gameh
inner join dashboard.blocos b on b.id = gameh.bloco_id
inner join dashboard.fases_cultura fc on fc.id = gameh.fase_cultura_id
where gameh.gestao_agricola_talhao_id in
(select gat.id from dashboard.gestao_agricola_talhao gat where gat.safra like '2025' and gat.talhao_id = 1) order by gameh.Id  ;

-- view de dados de gestão guarda-chuva por talhao
create materialized view dashboard.v_gestao_guarda_chuva_por_talhao as
select gcppt.id as "id",
gcppt.valor as "valor",
tcp.nome as "tipo_despesa",
dtcp.nome as "detalhe_tipo_despesa",
t.latitude as "latitude",
t.longitude as "longitude",
t.nome as "nome_talhao"
from dashboard.gestao_custos_producao_por_talhao gcppt
inner join dashboard.talhoes t on t.id = gcppt.talhao_id
inner join dashboard.detalhes_tipos_custos_producao dtcp on  dtcp.id = gcppt.custo_especificacao_id
inner join dashboard.tipos_custos_producao tcp on tcp.id = dtcp.tipo_custo_id
where gcppt.safra like '2025' order by gcppt.talhao_id ;

--
create materialized view dashboard.v_gestao_guarda_chuva_fazenda as
select gcdgcf.id as "Id",
gcdgcf.valor as "valor",
dtcp.nome as "Detalhe_Custo",
tdgc.nome as "Tipo_Custo"
from dashboard.gestao_custos_despesas_guarda_chuva_fazenda gcdgcf
inner join dashboard.detalhes_tipos_custos_producao dtcp on dtcp.id = gcdgcf.detalhes_tipo_custo_id
inner join dashboard.tipos_despesas_guarda_chuva tdgc on tdgc.id = dtcp.tipo_custo_id
where gcdgcf.fazenda_id in ( select id from dashboard.fazendas f where f.nome like '%São José%') and gcdgcf.safra like '2025' ;

