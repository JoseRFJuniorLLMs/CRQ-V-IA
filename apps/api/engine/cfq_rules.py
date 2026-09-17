"""
Motor Regulatório CRQ-V baseado na Resolução Normativa CFQ nº 339/2025.
Classifica CNAEs e estabelecimentos por probabilidade e obrigatoriedade de registro no CRQ-V.
"""

from typing import List, Dict, Tuple

# Mapeamento de CNAEs com base na Resolução CFQ 339/2025 e Lei 2.800/1956
CFQ_CNAE_RULES = {
    # TIER 1: OBRIGATORIEDADE / ALTA RELEVÂNCIA (Score 80 - 100)
    # Fabricação de produtos químicos, tintas, fertilizantes, defensivos, saneantes, cosméticos, refino
    "2011-8": {"tier": "HIGH", "weight": 95, "desc": "Fabricação de cloro e álcalis", "rationale": "Atividade química básica essencial, registro obrigatório no CRQ-V."},
    "2012-6": {"tier": "HIGH", "weight": 95, "desc": "Fabricação de intermediários para fertilizantes", "rationale": "Síntese e transformação química, registro e responsável técnico obrigatórios."},
    "2013-4": {"tier": "HIGH", "weight": 95, "desc": "Fabricação de adubos e fertilizantes", "rationale": "Formulação química de fertilizantes, fiscalização direta do CRQ-V."},
    "2014-2": {"tier": "HIGH", "weight": 95, "desc": "Fabricação de gases industriais", "rationale": "Processamento e envase de gases químicos, enquadramento pleno no CRQ-V."},
    "2019-3": {"tier": "HIGH", "weight": 95, "desc": "Fabricação de outros produtos químicos inorgânicos", "rationale": "Indústria química pesada inorgânica, controle técnico estrito."},
    "2021-5": {"tier": "HIGH", "weight": 95, "desc": "Fabricação de produtos petroquímicos básicos", "rationale": "Refino e craqueamento petroquímico, polo petroquímico (ex: Triunfo/RS)."},
    "2022-3": {"tier": "HIGH", "weight": 95, "desc": "Fabricação de intermediários para plastificantes e resinas", "rationale": "Síntese de polímeros e resinas, atividade química privativa."},
    "2029-1": {"tier": "HIGH", "weight": 95, "desc": "Fabricação de outros produtos químicos orgânicos", "rationale": "Indústria química orgânica, responsabilidade técnica indelegável."},
    "2031-2": {"tier": "HIGH", "weight": 90, "desc": "Fabricação de resinas termoplásticas", "rationale": "Polimerização e transformação industrial química."},
    "2032-1": {"tier": "HIGH", "weight": 90, "desc": "Fabricação de resinas termofixas", "rationale": "Química de polímeros avançados, registro obrigatório."},
    "2033-9": {"tier": "HIGH", "weight": 90, "desc": "Fabricação de elastômeros", "rationale": "Borracha sintética e elastômeros, processo químico controlado."},
    "2040-1": {"tier": "HIGH", "weight": 90, "desc": "Fabricação de fibras artificiais e sintéticas", "rationale": "Fiação química e extrusão de filamentos poliméricos."},
    "2051-7": {"tier": "HIGH", "weight": 95, "desc": "Fabricação de defensivos agrícolas", "rationale": "Agrotóxicos e biocidas, alto risco toxicológico e controle técnico rigoroso."},
    "2052-5": {"tier": "HIGH", "weight": 95, "desc": "Fabricação de desinfestantes domissanitários", "rationale": "Saneantes e praguicidas urbanos, enquadramento prioritário no CRQ-V."},
    "2061-4": {"tier": "HIGH", "weight": 90, "desc": "Fabricação de sabões e detergentes sintéticos", "rationale": "Indústria de tensoativos e domissanitários, responsável técnico químico exigido."},
    "2062-2": {"tier": "HIGH", "weight": 90, "desc": "Fabricação de produtos de limpeza e polimento", "rationale": "Formulação de saneantes e limpadores industriais."},
    "2063-1": {"tier": "HIGH", "weight": 90, "desc": "Fabricação de cosméticos, produtos de perfumaria e de higiene pessoal", "rationale": "Química cosmética, registro de empresa e responsável técnico habilitado."},
    "2071-1": {"tier": "HIGH", "weight": 95, "desc": "Fabricação de tintas, vernizes, esmaltes e lacas", "rationale": "Formulação e dispersão de tintas e solventes, foco fiscalizatório clássico."},
    "2072-0": {"tier": "HIGH", "weight": 90, "desc": "Fabricação de tintas de impressão", "rationale": "Tintas gráficas e solventes industriais."},
    "2073-8": {"tier": "HIGH", "weight": 90, "desc": "Fabricação de impermeabilizantes, solventes e produtos afins", "rationale": "Misturas químicas complexas, inflamáveis e solventes."},
    "2091-6": {"tier": "HIGH", "weight": 95, "desc": "Fabricação de adesivos e selantes", "rationale": "Adesivos industriais e colas sintéticas."},
    "2092-4": {"tier": "HIGH", "weight": 95, "desc": "Fabricação de pólvoras, explosivos e detonantes", "rationale": "Materiais energéticos e explosivos, controle químico e militar estrito."},
    "2093-2": {"tier": "HIGH", "weight": 90, "desc": "Fabricação de aditivos de uso industrial", "rationale": "Aditivos para combustíveis, plásticos e lubrificantes."},
    "2094-1": {"tier": "HIGH", "weight": 90, "desc": "Fabricação de catalisadores", "rationale": "Química fina e processos catalíticos industriais."},
    "2099-1": {"tier": "HIGH", "weight": 85, "desc": "Fabricação de outros produtos químicos não especificados", "rationale": "Especialidades químicas e produtos formulados diversos."},
    "2110-6": {"tier": "HIGH", "weight": 90, "desc": "Fabricação de produtos farmoquímicos", "rationale": "Síntese de insumos farmacêuticos ativos (IFAs), controle químico direto."},

    # TIER 2: MÉDIA RELEVÂNCIA / ATIVIDADES INDUSTRIAIS E SERVIÇOS TÉCNICOS (Score 55 - 79)
    # Tratamento de efluentes, galvanoplastia, laboratórios, alimentos com aditivos, celulose, curtume
    "1510-6": {"tier": "MEDIUM", "weight": 70, "desc": "Curtimento e outras preparações de couro", "rationale": "Processo químico intensivo de curtimento (cromo/tanino) e tratamento de efluentes."},
    "1710-9": {"tier": "MEDIUM", "weight": 75, "desc": "Fabricação de celulose e pastas químicas", "rationale": "Digestão química de madeira, branqueamento com cloro/dióxido e recuperação de licores."},
    "1721-4": {"tier": "MEDIUM", "weight": 65, "desc": "Fabricação de papel e papelão", "rationale": "Colagem, cargas minerais, aditivação química e controle de pH e retenção."},
    "1921-7": {"tier": "MEDIUM", "weight": 75, "desc": "Fabricação de produtos do refino de petróleo", "rationale": "Processamento e controle de combustíveis e óleos."},
    "1922-5": {"tier": "MEDIUM", "weight": 75, "desc": "Rerrefino de óleos lubrificantes", "rationale": "Reciclagem e reprocessamento químico de lubrificantes usados."},
    "2211-1": {"tier": "MEDIUM", "weight": 70, "desc": "Fabricação de pneumáticos e câmaras-de-ar", "rationale": "Vulcanização e aditivação de elastômeros e negro de fumo."},
    "2219-6": {"tier": "MEDIUM", "weight": 65, "desc": "Fabricação de artefatos de borracha", "rationale": "Formulação elastomérica e processos térmicos de cura."},
    "2221-8": {"tier": "MEDIUM", "weight": 70, "desc": "Fabricação de laminados plásticos", "rationale": "Extrusão e termomoldagem de resinas poliméricas."},
    "2222-6": {"tier": "MEDIUM", "weight": 65, "desc": "Fabricação de embalagens de material plástico", "rationale": "Transformação plástica e uso de masterbatches colorantes."},
    "2229-3": {"tier": "MEDIUM", "weight": 65, "desc": "Fabricação de artefatos plásticos diversos", "rationale": "Injeção, extrusão e reciclagem de resinas sintéticas."},
    "2311-7": {"tier": "MEDIUM", "weight": 65, "desc": "Fabricação de vidro plano e de segurança", "rationale": "Fusão de silicatos, têmpera química e tratamento superficial."},
    "2312-5": {"tier": "MEDIUM", "weight": 65, "desc": "Fabricação de embalagens de vidro", "rationale": "Fusão vítrea e controle de composição química de matérias-primas."},
    "2320-6": {"tier": "MEDIUM", "weight": 75, "desc": "Fabricação de cimento", "rationale": "Calcinação e clinquerização de calcário e argila, controle de óxidos."},
    "2341-9": {"tier": "MEDIUM", "weight": 65, "desc": "Fabricação de produtos cerâmicos refratários", "rationale": "Formulações cerâmicas refratárias submetidas a alta temperatura."},
    "2411-3": {"tier": "MEDIUM", "weight": 70, "desc": "Siderurgia e refino de ferro-gusa", "rationale": "Redução e oxidação em alto-forno, controle de ligas e escórias."},
    "2441-5": {"tier": "MEDIUM", "weight": 70, "desc": "Metalurgia de metais não-ferrosos", "rationale": "Eletro-obtenção, lixiviação e refino químico de cobre, alumínio e chumbo."},
    "2539-0": {"tier": "MEDIUM", "weight": 70, "desc": "Serviços de usinagem, solda e tratamento de metais (Galvanoplastia)", "rationale": "Banhos galvânicos, anodização e desengraxe exigem controle químico de soluções."},
    "3600-6": {"tier": "MEDIUM", "weight": 75, "desc": "Captação, tratamento e distribuição de água", "rationale": "Controle físico-químico da potabilidade e dosagem de reagentes (coagulantes/cloro)."},
    "3701-1": {"tier": "MEDIUM", "weight": 75, "desc": "Gestão de redes de esgoto e tratamento de efluentes", "rationale": "Operação de ETEs industriais e municipais com controle de DBO/DQO e metais."},
    "3811-4": {"tier": "MEDIUM", "weight": 60, "desc": "Coleta e tratamento de resíduos perigosos", "rationale": "Manipulação e destinação de resíduos químicos industriais."},
    "3821-1": {"tier": "MEDIUM", "weight": 65, "desc": "Tratamento e disposição de resíduos perigosos", "rationale": "Incineração, coprocessamento e neutralização química de passivos."},
    "3832-7": {"tier": "MEDIUM", "weight": 65, "desc": "Recuperação de materiais plásticos (Reciclagem)", "rationale": "Descontaminação, extrusão e pelotização de polímeros pós-consumo."},
    "7120-1": {"tier": "MEDIUM", "weight": 75, "desc": "Testes e análises técnicas (Laboratórios)", "rationale": "Laboratórios de ensaios físico-químicos e cromatografia devem possuir registro no CRQ."},
    "7210-0": {"tier": "MEDIUM", "weight": 70, "desc": "Pesquisa e desenvolvimento experimental em ciências físicas e naturais", "rationale": "P&D com bancada química, síntese e testes moleculares."},
    "1031-7": {"tier": "MEDIUM", "weight": 60, "desc": "Fabricação de conservas de frutas e legumes", "rationale": "Controle de acidez, conservantes químicos e pasteurização."},
    "1041-4": {"tier": "MEDIUM", "weight": 65, "desc": "Fabricação de óleos vegetais em bruto", "rationale": "Extração por solventes químicos (hexano) e degomagem."},
    "1042-2": {"tier": "MEDIUM", "weight": 65, "desc": "Fabricação de óleos vegetais refinados", "rationale": "Neutralização química, clarificação e desodorização de óleos."},
    "1051-2": {"tier": "MEDIUM", "weight": 60, "desc": "Preparação do leite e fabricação de laticínios", "rationale": "Fermentação lática, coagulação enzimática e controle analítico de acidez/gordura."},
    "1062-7": {"tier": "MEDIUM", "weight": 65, "desc": "Fabricação de amidos e féculas de vegetais", "rationale": "Modificação química de amidos para uso alimentício e industrial."},
    "1066-0": {"tier": "MEDIUM", "weight": 60, "desc": "Fabricação de alimentos para animais (rações)", "rationale": "Aditivação mineral, premixes químicos e controle de micotoxinas."},
    "1099-6": {"tier": "MEDIUM", "weight": 65, "desc": "Fabricação de vinagres e fermentos químicos/biológicos", "rationale": "Fermentação acética e formulação de fermentos e aditivos."},
    "1111-9": {"tier": "MEDIUM", "weight": 65, "desc": "Fabricação de aguardentes e outras bebidas destiladas", "rationale": "Fermentação e destilação com análises físico-químicas de graduação e congêneres."},
    "1112-7": {"tier": "MEDIUM", "weight": 65, "desc": "Fabricação de vinho", "rationale": "Enologia e controle analítico de mostos, sulfitação e fermentação (Polo Serra Gaúcha/RS)."},
    "1113-5": {"tier": "MEDIUM", "weight": 65, "desc": "Fabricação de cervejas e chopes", "rationale": "Bioquímica de malteação, mosturação e controle microbiológico/físico-químico."},
    "1610-2": {"tier": "MEDIUM", "weight": 60, "desc": "Desdobramento e tratamento químico de madeira", "rationale": "Impregnação com sais hidrossolúveis (CCA/CCB) em autoclave contra xilófagos."},
    "2121-1": {"tier": "MEDIUM", "weight": 75, "desc": "Fabricação de medicamentos alopáticos para uso humano", "rationale": "Controle físico-químico de formulações e ensaios analíticos de teor e dissolução."},

    # TIER 3: BAIXA RELEVÂNCIA / COMÉRCIO E APOIO (Score 30 - 54)
    # Comércio atacadista de químicos, defensivos, embalagens, equipamentos de laboratório
    "4684-2": {"tier": "LOW", "weight": 45, "desc": "Comércio atacadista de produtos químicos e petroquímicos", "rationale": "Armazenagem, fracionamento e distribuição de matérias-primas químicas."},
    "4683-4": {"tier": "LOW", "weight": 45, "desc": "Comércio atacadista de defensivos agrícolas, adubos e fertilizantes", "rationale": "Comércio e estocagem de agroquímicos, com potencial fiscalizatório."},
    "4644-3": {"tier": "LOW", "weight": 40, "desc": "Comércio atacadista de produtos farmacêuticos e cosméticos", "rationale": "Distribuição de produtos formulados, fiscalização em casos de fracionamento."},
    "4649-4": {"tier": "LOW", "weight": 35, "desc": "Comércio atacadista de produtos de higiene, limpeza e conservação domiciliar", "rationale": "Distribuição atacadista de saneantes."},
    "4669-9": {"tier": "LOW", "weight": 30, "desc": "Comércio atacadista de máquinas e equipamentos para uso industrial e laboratórios", "rationale": "Fornecimento de instrumentos analíticos e insumos."}
}

def normalize_cnae(code: str) -> str:
    """Remove caracteres especiais e normaliza para formato de classe ex: '2029-1' ou '2029-1/00'."""
    if not code:
        return ""
    clean = "".join(c for c in code if c.isdigit())
    if len(clean) == 7:
        return f"{clean[:4]}-{clean[4]}/{clean[5:]}"
    elif len(clean) >= 5:
        return f"{clean[:4]}-{clean[4]}"
    return code

def match_cnae_prefix(cnae_clean: str) -> Tuple[str, dict]:
    """Busca correspondência por prefixo de classe (ex: 2029-1)."""
    clean_digits = "".join(c for c in cnae_clean if c.isdigit())
    if len(clean_digits) >= 5:
        prefix_class = f"{clean_digits[:4]}-{clean_digits[4]}"
        if prefix_class in CFQ_CNAE_RULES:
            return prefix_class, CFQ_CNAE_RULES[prefix_class]
    return "", {}

def classify_establishment(primary_cnae: str, secondary_cnaes: List[str] = None) -> Dict:
    """
    Analisa o CNAE primário e secundários conforme a Resolução Normativa CFQ 339/2025.
    Retorna score (0-100), prioridade fiscal (HIGH/MEDIUM/LOW), status regulatório 
    (MANDATORY_REGISTRATION, CHEMICAL_SUPPORT_ACTIVITY, SERVICE_TO_THIRD_PARTIES) e justificativa explicável.
    """
    if secondary_cnaes is None:
        secondary_cnaes = []

    matched_factors = []
    max_score = 0
    highest_tier = "NONE"
    primary_rationale = ""
    primary_matched = False
    is_service = False

    # Avalia CNAE Primário
    cnae_norm = normalize_cnae(primary_cnae)
    matched_key, rule = match_cnae_prefix(cnae_norm)
    
    if rule:
        primary_matched = True
        max_score = rule["weight"]
        highest_tier = rule["tier"]
        primary_rationale = f"CNAE Primário ({cnae_norm} - {rule['desc']}): {rule['rationale']}"
        if "7120" in cnae_norm or "7210" in cnae_norm or "2539" in cnae_norm:
            is_service = True
        matched_factors.append({
            "cnae": cnae_norm,
            "type": "PRIMARY",
            "desc": rule["desc"],
            "tier": rule["tier"],
            "weight": rule["weight"],
            "rationale": rule["rationale"]
        })
    else:
        primary_rationale = f"CNAE Primário ({primary_cnae}) não classificado como privativo da Química."

    # Avalia CNAEs Secundários
    for sec in secondary_cnaes:
        sec_norm = normalize_cnae(sec)
        sec_key, sec_rule = match_cnae_prefix(sec_norm)
        if sec_rule:
            # Ponderação para secundários: 85% do peso original
            sec_weight = int(sec_rule["weight"] * 0.85)
            if sec_weight > max_score:
                max_score = sec_weight
                if highest_tier in ("NONE", "LOW") and sec_rule["tier"] in ("HIGH", "MEDIUM"):
                    highest_tier = sec_rule["tier"]
            matched_factors.append({
                "cnae": sec_norm,
                "type": "SECONDARY",
                "desc": sec_rule["desc"],
                "tier": sec_rule["tier"],
                "weight": sec_weight,
                "rationale": f"Atividade Secundária: {sec_rule['rationale']}"
            })

    if not matched_factors:
        return {
            "score": 5.0,
            "tier": "NONE",
            "fiscal_priority": "LOW",
            "regulatory_status": "OUT_OF_SCOPE",
            "rationale": "Empresa sem atividade econômica com indícios diretos de Química pela Resolução CFQ 339/2025.",
            "factors": []
        }

    # Determina o status regulatório segundo Art. 3º e 4º da RN CFQ 339/2025
    if is_service:
        reg_status = "SERVICE_TO_THIRD_PARTIES"
    elif primary_matched and highest_tier in ("HIGH", "MEDIUM"):
        reg_status = "MANDATORY_REGISTRATION"
    elif not primary_matched and matched_factors:
        reg_status = "CHEMICAL_SUPPORT_ACTIVITY"
    else:
        reg_status = "MANDATORY_REGISTRATION" if highest_tier == "HIGH" else "CHEMICAL_SUPPORT_ACTIVITY"

    # Gera justificativa consolidada
    consolidated_rationale = primary_rationale
    if len(matched_factors) > 1:
        extra_cnaes = [f["cnae"] for f in matched_factors if f["type"] == "SECONDARY"]
        consolidated_rationale += f" Apresenta também {len(extra_cnaes)} atividade(s) secundária(s) com potencial químico ({', '.join(extra_cnaes[:3])})."

    return {
        "score": float(max_score),
        "tier": highest_tier,
        "fiscal_priority": highest_tier,
        "regulatory_status": reg_status,
        "rationale": consolidated_rationale,
        "factors": matched_factors
    }

