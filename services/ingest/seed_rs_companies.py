"""
Seed de empresas e estabelecimentos no Estado do Rio Grande do Sul.
Cobre os principais polos industriais químicos, agroindustriais, coureiro-calçadistas,
vitivinícolas e de tratamento de efluentes do RS.
"""

from sqlalchemy.orm import Session
from apps.api.models.company import Company, Establishment
from apps.api.engine.cfq_rules import classify_establishment

RS_COMPANIES_DATA = [
    # --- POLO PETROQUÍMICO DE TRIUNFO / CANOAS / PORTO ALEGRE ---
    {
        "cnpj": "92754738000180",
        "legal_name": "PETROQUÍMICA SUL BRASIL S.A.",
        "trade_name": "PETROQUÍMICA TRIUNFO",
        "size": "DEMAIS",
        "capital": 85000000.0,
        "branch": "MATRIZ",
        "primary_cnae": "2021-5/00",
        "secondary_cnaes": ["2022-3/00", "2031-2/00", "4684-2/01"],
        "city": "Triunfo",
        "district": "Distrito Industrial do Polo",
        "street": "Rodovia TF-010",
        "number": "Km 12",
        "cep": "95840-000",
        "phone": "(51) 3457-1000",
        "email": "fiscal@petroquimicasul.com.br",
        "status": "ATIVA",
        "opening": "1982-06-15",
        "crq_status": "REGISTRADA"
    },
    {
        "cnpj": "88412990000142",
        "legal_name": "TINTAS E RESINAS DO SUL LTDA",
        "trade_name": "TINTAS SUL",
        "size": "EPP",
        "capital": 1200000.0,
        "branch": "MATRIZ",
        "primary_cnae": "2071-1/00",
        "secondary_cnaes": ["2073-8/00", "4684-2/01"],
        "city": "Porto Alegre",
        "district": "Navegantes",
        "street": "Avenida Sertório",
        "number": "4520",
        "cep": "91020-001",
        "phone": "(51) 3342-9900",
        "email": "contato@tintassul.com.br",
        "status": "ATIVA",
        "opening": "1998-11-20",
        "crq_status": "NAO_CADASTRADA"
    },
    {
        "cnpj": "04123567000199",
        "legal_name": "SOLUÇÕES QUÍMICAS SANEANTES GAÚCHA LTDA",
        "trade_name": "LIMPA GAÚCHO",
        "size": "ME",
        "capital": 150000.0,
        "branch": "MATRIZ",
        "primary_cnae": "2062-2/00",
        "secondary_cnaes": ["2061-4/00", "4649-4/08"],
        "city": "Canoas",
        "district": "Bairro Rio Branco",
        "street": "Rua Boa Saúde",
        "number": "780",
        "cep": "92200-300",
        "phone": "(51) 3476-5544",
        "email": "quimica@limpagaucho.com.br",
        "status": "ATIVA",
        "opening": "2015-03-10",
        "crq_status": "NAO_CADASTRADA"
    },
    {
        "cnpj": "12987456000130",
        "legal_name": "COSMÉTICA DA SERRA INDÚSTRIA E COMÉRCIO S.A.",
        "trade_name": "BELLA SERRA COSMÉTICOS",
        "size": "EPP",
        "capital": 2500000.0,
        "branch": "MATRIZ",
        "primary_cnae": "2063-1/00",
        "secondary_cnaes": ["2062-2/00", "4644-3/01"],
        "city": "Caxias do Sul",
        "district": "São Ciro",
        "street": "Avenida Rubem Bento Alves",
        "number": "1450",
        "cep": "95050-002",
        "phone": "(54) 3218-4000",
        "email": "laboratorio@bellaserra.com.br",
        "status": "ATIVA",
        "opening": "2010-08-04",
        "crq_status": "EM_FISCALIZACAO"
    },

    # --- AGROQUÍMICA E FERTILIZANTES (PASSO FUNDO / CRUZ ALTA / RIO GRANDE) ---
    {
        "cnpj": "91234876000105",
        "legal_name": "FERTILIZANTES E NUTRIENTES DO PAMPA LTDA",
        "trade_name": "PAMPA FERTILIZANTES",
        "size": "DEMAIS",
        "capital": 18000000.0,
        "branch": "MATRIZ",
        "primary_cnae": "2013-4/00",
        "secondary_cnaes": ["2012-6/00", "4683-4/00"],
        "city": "Passo Fundo",
        "district": "Área Industrial Norte",
        "street": "Avenida Presidente Vargas",
        "number": "3200",
        "cep": "99060-000",
        "phone": "(54) 3315-7700",
        "email": "fiscalizacao@pampafertil.com.br",
        "status": "ATIVA",
        "opening": "2004-01-18",
        "crq_status": "NAO_CADASTRADA"
    },
    {
        "cnpj": "02987123000119",
        "legal_name": "DEFENSIVOS SUL-RIOGRANDENSE INDÚSTRIA LTDA",
        "trade_name": "AGROSUL DEFENSIVOS",
        "size": "DEMAIS",
        "capital": 22000000.0,
        "branch": "MATRIZ",
        "primary_cnae": "2051-7/00",
        "secondary_cnaes": ["2019-3/00", "4683-4/00"],
        "city": "Rio Grande",
        "district": "Distrito Industrial Portuário",
        "street": "Avenida Almirante Maximiano da Fonseca",
        "number": "500",
        "cep": "96204-020",
        "phone": "(53) 3233-8899",
        "email": "tecnico@agrosulquimica.com.br",
        "status": "ATIVA",
        "opening": "2007-09-12",
        "crq_status": "REGISTRADA"
    },

    # --- CURTUMES E TRATAMENTO DE COUROS (VALE DOS SINOS / NOVO HAMBURGO) ---
    {
        "cnpj": "90554332000161",
        "legal_name": "CURTUME SINOS FINISHING S.A.",
        "trade_name": "CURTUME SINOS",
        "size": "DEMAIS",
        "capital": 9500000.0,
        "branch": "MATRIZ",
        "primary_cnae": "1510-6/00",
        "secondary_cnaes": ["3701-1/00", "2091-6/00"],
        "city": "Novo Hamburgo",
        "district": "Scharlau",
        "street": "Rua Guia Lopes",
        "number": "2100",
        "cep": "93410-000",
        "phone": "(51) 3594-1122",
        "email": "meioambiente@curtumesinos.com.br",
        "status": "ATIVA",
        "opening": "1992-04-11",
        "crq_status": "NAO_CADASTRADA"
    },
    {
        "cnpj": "08123456000188",
        "legal_name": "CURTUME VALE DO PARANHANA LTDA",
        "trade_name": "PARANHANA LEATHER",
        "size": "EPP",
        "capital": 800000.0,
        "branch": "MATRIZ",
        "primary_cnae": "1510-6/00",
        "secondary_cnaes": ["3821-1/00"],
        "city": "Estância Velha",
        "district": "Rincão dos Ilhéus",
        "street": "Rua Presidente Lucena",
        "number": "120",
        "cep": "93990-000",
        "phone": "(51) 3561-3344",
        "email": "curtume@paranhana.com.br",
        "status": "ATIVA",
        "opening": "2011-10-05",
        "crq_status": "NAO_CADASTRADA"
    },

    # --- TRATAMENTO DE SUPERFÍCIES / GALVANOPLASTIA ---
    {
        "cnpj": "14567890000122",
        "legal_name": "GALVANO SUL TRATAMENTO DE METAIS LTDA",
        "trade_name": "GALVANO SUL",
        "size": "ME",
        "capital": 200000.0,
        "branch": "MATRIZ",
        "primary_cnae": "2539-0/00",
        "secondary_cnaes": ["3701-1/00", "2073-8/00"],
        "city": "Caxias do Sul",
        "district": "Pio X",
        "street": "Rua Moreira César",
        "number": "2250",
        "cep": "95034-000",
        "phone": "(54) 3225-8877",
        "email": "quimico@galvanosul.com.br",
        "status": "ATIVA",
        "opening": "2018-02-14",
        "crq_status": "NAO_CADASTRADA"
    },
    {
        "cnpj": "21987654000155",
        "legal_name": "CROMAGEM E BANHOS QUÍMICOS PORTO ALEGRE LTDA",
        "trade_name": "CROMO POA",
        "size": "ME",
        "capital": 100000.0,
        "branch": "MATRIZ",
        "primary_cnae": "2539-0/00",
        "secondary_cnaes": ["2019-3/00"],
        "city": "Porto Alegre",
        "district": "Anchieta",
        "street": "Rua Dona Teodora",
        "number": "915",
        "cep": "90240-300",
        "phone": "(51) 3374-1234",
        "email": "cromopoa@terra.com.br",
        "status": "ATIVA",
        "opening": "2016-07-22",
        "crq_status": "NAO_CADASTRADA"
    },

    # --- SANEAMENTO, TRATAMENTO DE ÁGUA E EFLUENTES (CORSAN / ETEs) ---
    {
        "cnpj": "07444333000144",
        "legal_name": "BIOEFLUENTES TRATAMENTO AMBIENTAL LTDA",
        "trade_name": "BIOEFLUENTES RS",
        "size": "EPP",
        "capital": 1500000.0,
        "branch": "MATRIZ",
        "primary_cnae": "3701-1/00",
        "secondary_cnaes": ["3821-1/00", "7120-1/00"],
        "city": "São Leopoldo",
        "district": "Distrito Industrial",
        "street": "Avenida das Indústrias",
        "number": "850",
        "cep": "93030-000",
        "phone": "(51) 3589-9090",
        "email": "operacao@bioefluentes.com.br",
        "status": "ATIVA",
        "opening": "2014-05-19",
        "crq_status": "EM_FISCALIZACAO"
    },
    {
        "cnpj": "18222333000111",
        "legal_name": "ÁGUAS DA SERRA SANEAMENTO E GESTÃO LTDA",
        "trade_name": "ÁGUAS DA SERRA",
        "size": "DEMAIS",
        "capital": 5000000.0,
        "branch": "MATRIZ",
        "primary_cnae": "3600-6/01",
        "secondary_cnaes": ["7120-1/00"],
        "city": "Gramado",
        "district": "Várzea Grande",
        "street": "Rua São Pedro",
        "number": "1120",
        "cep": "95670-000",
        "phone": "(54) 3286-4500",
        "email": "laboratorio@aguasdaserra.com.br",
        "status": "ATIVA",
        "opening": "2009-12-01",
        "crq_status": "REGISTRADA"
    },

    # --- LABORATÓRIOS DE ANÁLISES FÍSICO-QUÍMICAS ---
    {
        "cnpj": "15333444000177",
        "legal_name": "LAB-SUL ANÁLISES AMBIENTAIS E QUÍMICAS LTDA",
        "trade_name": "LABSUL ANALÍTICA",
        "size": "EPP",
        "capital": 750000.0,
        "branch": "MATRIZ",
        "primary_cnae": "7120-1/00",
        "secondary_cnaes": ["7210-0/00"],
        "city": "Porto Alegre",
        "district": "Petrópolis",
        "street": "Avenida Protásio Alves",
        "number": "2850",
        "cep": "90410-004",
        "phone": "(51) 3333-7788",
        "email": "diretoria@labsulanalitica.com.br",
        "status": "ATIVA",
        "opening": "2012-03-30",
        "crq_status": "REGISTRADA"
    },
    {
        "cnpj": "23444555000188",
        "legal_name": "QUIMI-TEST ANÁLISES INDUSTRIAIS LTDA",
        "trade_name": "QUIMITEST",
        "size": "ME",
        "capital": 120000.0,
        "branch": "MATRIZ",
        "primary_cnae": "7120-1/00",
        "secondary_cnaes": [],
        "city": "Pelotas",
        "district": "Fragata",
        "street": "Avenida Duque de Caxias",
        "number": "410",
        "cep": "96030-000",
        "phone": "(53) 3227-1199",
        "email": "laudos@quimitest.com.br",
        "status": "ATIVA",
        "opening": "2019-09-15",
        "crq_status": "NAO_CADASTRADA"
    },

    # --- VITIVINICULTURA E DESTILADOS (SERRA GAÚCHA) ---
    {
        "cnpj": "90111222000133",
        "legal_name": "VINÍCOLA VALE DOS VINHEDOS LTDA",
        "trade_name": "VINÍCOLA VALE D'OURO",
        "size": "DEMAIS",
        "capital": 14000000.0,
        "branch": "MATRIZ",
        "primary_cnae": "1112-7/00",
        "secondary_cnaes": ["1111-9/02", "7120-1/00"],
        "city": "Bento Gonçalves",
        "district": "Vale dos Vinhedos",
        "street": "Estrada RS-444",
        "number": "Km 18",
        "cep": "95700-000",
        "phone": "(54) 3459-2000",
        "email": "enologia@valedouro.com.br",
        "status": "ATIVA",
        "opening": "1995-08-20",
        "crq_status": "REGISTRADA"
    },
    {
        "cnpj": "19888777000166",
        "legal_name": "CERVEJARIA ARTESANAL MISSÕES LTDA",
        "trade_name": "MISSÕES BEER",
        "size": "ME",
        "capital": 250000.0,
        "branch": "MATRIZ",
        "primary_cnae": "1113-5/02",
        "secondary_cnaes": ["4635-4/02"],
        "city": "Santo Ângelo",
        "district": "Centro",
        "street": "Rua Marechal Floriano",
        "number": "1420",
        "cep": "98801-650",
        "phone": "(55) 3312-5500",
        "email": "mestrecervejeiro@missoesbeer.com.br",
        "status": "ATIVA",
        "opening": "2020-04-10",
        "crq_status": "NAO_CADASTRADA"
    },

    # --- COMÉRCIO ATACADISTA DE PRODUTOS QUÍMICOS ---
    {
        "cnpj": "05999888000101",
        "legal_name": "DISTRIBUIDORA GAÚCHA DE PRODUTOS QUÍMICOS S.A.",
        "trade_name": "DISQUÍMICA RS",
        "size": "DEMAIS",
        "capital": 6000000.0,
        "branch": "MATRIZ",
        "primary_cnae": "4684-2/01",
        "secondary_cnaes": ["4683-4/00", "4649-4/08"],
        "city": "Canoas",
        "district": "Industrial",
        "street": "Avenida Getúlio Vargas",
        "number": "6200",
        "cep": "92010-011",
        "phone": "(51) 3477-8000",
        "email": "atendimento@disquimicars.com.br",
        "status": "ATIVA",
        "opening": "2001-07-02",
        "crq_status": "REGISTRADA"
    },

    # --- EMPRESA BAIXADA (Para teste de filtro de situação cadastral) ---
    {
        "cnpj": "03888999000155",
        "legal_name": "QUÍMICA CANOENSE DE SOLVENTES LTDA (EXTINTA)",
        "trade_name": "SOLVECAN",
        "size": "ME",
        "capital": 50000.0,
        "branch": "MATRIZ",
        "primary_cnae": "2073-8/00",
        "secondary_cnaes": [],
        "city": "Canoas",
        "district": "Fátima",
        "street": "Rua Bartolomeu de Gusmão",
        "number": "310",
        "cep": "92200-110",
        "phone": "(51) 3466-2200",
        "email": "contato@solvecan.com.br",
        "status": "BAIXADA",
        "opening": "2005-02-15",
        "crq_status": "DISPENSADA"
    },

    # --- EMPRESA NÃO-QUÍMICA (Para teste de filtro negativo) ---
    {
        "cnpj": "25111222000199",
        "legal_name": "SUL TECH DESENVOLVIMENTO DE SOFTWARE LTDA",
        "trade_name": "SUL TECH",
        "size": "ME",
        "capital": 80000.0,
        "branch": "MATRIZ",
        "primary_cnae": "6201-5/01",
        "secondary_cnaes": ["6202-3/00"],
        "city": "Porto Alegre",
        "district": "Floresta",
        "street": "Rua Cristóvão Colombo",
        "number": "1500",
        "cep": "90560-002",
        "phone": "(51) 3311-2233",
        "email": "contato@sultech.com.br",
        "status": "ATIVA",
        "opening": "2021-01-10",
        "crq_status": "DISPENSADA"
    }
]

def seed_companies(db: Session):
    est_count = 0
    for item in RS_COMPANIES_DATA:
        cnpj_clean = "".join(c for c in item["cnpj"] if c.isdigit())
        cnpj_base = cnpj_clean[:8]

        # 1. Company
        company = db.query(Company).filter(Company.cnpj_base == cnpj_base).first()
        if not company:
            company = Company(
                cnpj_base=cnpj_base,
                legal_name=item["legal_name"],
                company_size=item["size"],
                capital_social=item["capital"]
            )
            db.add(company)
            db.flush()

        # 2. Establishment
        est = db.query(Establishment).filter(Establishment.cnpj == cnpj_clean).first()
        if not est:
            # Roda o motor de classificação da Resolução CFQ 339/2025
            classification = classify_establishment(
                primary_cnae=item["primary_cnae"],
                secondary_cnaes=item["secondary_cnaes"]
            )

            # Define RT e AFT realistas com base na situação de registro no CRQ-V
            is_reg = item["crq_status"] == "REGISTRADA"
            c_prefix = cnpj_clean[:6]
            tech_man = f"Dra. Mariana Dornelles (CRQ 0520{c_prefix[:4]})" if is_reg else None
            tech_crq = f"0520{c_prefix[:4]}-V" if is_reg else None
            aft_num = f"AFT-2026-{c_prefix[:5]}" if is_reg else None
            aft_val = "2026-12-31" if is_reg else None
            ie_num = f"096/{cnpj_clean[3:11]}"

            est = Establishment(
                company_id=company.id,
                cnpj=cnpj_clean,
                branch_type=item["branch"],
                trade_name=item["trade_name"],
                registration_status=item["status"],
                opening_date=item["opening"],
                primary_cnae=item["primary_cnae"],
                secondary_cnaes=item["secondary_cnaes"],
                street=item["street"],
                number=item["number"],
                district=item["district"],
                postal_code=item["cep"],
                city=item["city"],
                state="RS",
                phone=item["phone"],
                email=item["email"],
                chemical_score=classification["score"],
                cfq_tier=classification["tier"],
                cfq_rationale=classification["rationale"],
                regulatory_status=classification.get("regulatory_status", "MANDATORY_REGISTRATION"),
                crq_status=item["crq_status"],
                technical_manager=tech_man,
                technical_manager_crq=tech_crq,
                aft_number=aft_num,
                aft_valid_until=aft_val,
                state_registration=ie_num
            )
            db.add(est)
            est_count += 1

    db.commit()
    print(f"[Seed] {est_count} estabelecimentos do Rio Grande do Sul cadastrados e classificados.")

