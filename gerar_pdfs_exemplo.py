"""
Gera PDFs de exemplo de uma empresa fictícia — "Brisa Tecnologia Ltda." —
para testar o sistema. Execute:  python gerar_pdfs_exemplo.py
Os arquivos são criados na pasta ./exemplos
"""

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
)

OUT = Path(__file__).parent / "exemplos"
OUT.mkdir(exist_ok=True)

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Heading1"], textColor=colors.HexColor("#0E5A6B"))
H2 = ParagraphStyle("H2", parent=styles["Heading2"], textColor=colors.HexColor("#0E5A6B"))
P = ParagraphStyle("P", parent=styles["BodyText"], fontSize=10.5, leading=15, spaceAfter=6)


def table(rows):
    t = Table(rows, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCEFF2")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def build(filename, title, sections):
    doc = SimpleDocTemplate(str(OUT / filename), pagesize=A4,
                            leftMargin=2.2 * cm, rightMargin=2.2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm, title=title)
    story = [Paragraph(title, H1), Paragraph("Brisa Tecnologia Ltda. — documento fictício para demonstração", P), Spacer(1, 12)]
    for item in sections:
        if item == "PAGE":
            story.append(PageBreak())
        elif isinstance(item, tuple) and item[0] == "h":
            story.append(Paragraph(item[1], H2))
        elif isinstance(item, tuple) and item[0] == "t":
            story += [table(item[1]), Spacer(1, 8)]
        else:
            story.append(Paragraph(item, P))
    doc.build(story)
    print("gerado:", OUT / filename)


# ---------------------------------------------------------------------------
# 1. Manual do Colaborador
# ---------------------------------------------------------------------------
build("manual_do_colaborador.pdf", "Manual do Colaborador — versão 2026", [
    ("h", "1. Sobre a Brisa"),
    "A Brisa Tecnologia Ltda. foi fundada em 2014 em Campinas (SP) e desenvolve purificadores de ar "
    "inteligentes para residências e escritórios. Hoje a empresa tem 340 colaboradores distribuídos "
    "entre a sede em Campinas, o centro de distribuição em Jundiaí e o escritório comercial em Recife. "
    "Nossa missão é \"ar limpo acessível para todo mundo\". Os valores da empresa são: transparência, "
    "cuidado com o cliente, aprendizado contínuo e responsabilidade ambiental.",
    ("h", "2. Jornada de trabalho e ponto"),
    "A jornada padrão é de 40 horas semanais, de segunda a sexta-feira. O horário núcleo, em que todos "
    "devem estar disponíveis, é das 10h às 16h; fora desse período cada pessoa organiza seu horário com "
    "o gestor. O registro de ponto é feito pelo aplicativo BrisaPonto. Horas extras precisam de aprovação "
    "prévia do gestor no próprio aplicativo e são compensadas em banco de horas com validade de 6 meses. "
    "Saldo não compensado após 6 meses é pago em folha com adicional de 50%.",
    ("h", "3. Trabalho híbrido e remoto"),
    "O modelo padrão é híbrido: 2 dias presenciais por semana (terças e quintas são os dias de encontro "
    "do time) e 3 dias remotos. Funções de laboratório, produção e logística são 100% presenciais. "
    "Colaboradores em regime híbrido ou remoto recebem auxílio home office de R$ 150,00 por mês, pago "
    "junto com o salário, para despesas de internet e energia. Na admissão, a empresa também fornece "
    "notebook, monitor de 24 polegadas, teclado e mouse; cadeira ergonômica pode ser solicitada ao "
    "setor de Facilities mediante laudo ou indicação do SESMT.",
    ("h", "4. Férias"),
    "Todo colaborador CLT tem direito a 30 dias de férias após 12 meses de trabalho (período aquisitivo). "
    "As férias podem ser divididas em até três períodos, sendo que um deles deve ter no mínimo 14 dias "
    "corridos e os demais no mínimo 5 dias corridos cada. A solicitação deve ser feita no portal de RH "
    "com pelo menos 45 dias de antecedência. Não é permitido iniciar férias nos dois dias que antecedem "
    "feriado ou dia de descanso semanal remunerado. É possível vender até 10 dias (abono pecuniário), "
    "desde que solicitado até 15 dias antes do fim do período aquisitivo.",
    "Estagiários têm direito a 30 dias de recesso remunerado a cada 12 meses de contrato, ou proporcional "
    "para contratos menores, preferencialmente coincidindo com as férias escolares.",
    "PAGE",
    ("h", "5. Benefícios"),
    ("t", [
        ["Benefício", "Valor / Regra", "Quem tem direito"],
        ["Vale-refeição/alimentação", "R$ 45,00 por dia útil (cartão flexível)", "CLT e estagiários"],
        ["Plano de saúde", "Coparticipação de 20%, sem mensalidade para o titular", "CLT + dependentes"],
        ["Plano odontológico", "Gratuito para titular; R$ 18/mês por dependente", "CLT"],
        ["Auxílio home office", "R$ 150,00/mês", "Regime híbrido ou remoto"],
        ["Gympass/Wellhub", "Plano básico subsidiado", "CLT e estagiários"],
        ["Auxílio educação", "Até R$ 600,00/mês, 50% da mensalidade", "CLT com 6+ meses de casa"],
        ["Auxílio creche", "R$ 500,00/mês por filho até 6 anos", "CLT"],
        ["PLR", "Até 1,5 salário, conforme metas anuais", "CLT"],
    ]),
    "O auxílio educação vale para graduação, pós-graduação e cursos de idiomas relacionados à função. "
    "É necessário apresentar comprovante de matrícula e nota mínima 7,0 (ou aprovação) a cada semestre; "
    "em caso de desligamento voluntário em até 12 meses após o último reembolso, o valor deve ser devolvido.",
    ("h", "6. Reembolso de despesas"),
    "Despesas de viagem a trabalho (transporte, hospedagem e alimentação) são reembolsadas pelo sistema "
    "Despesas+ em até 10 dias úteis após a aprovação do gestor. Os comprovantes devem ser enviados em até "
    "30 dias da data da despesa; após esse prazo o reembolso não é garantido. Limites diários de "
    "alimentação em viagem: R$ 120,00 em capitais e R$ 90,00 nas demais cidades. Bebidas alcoólicas não "
    "são reembolsáveis. Corridas de aplicativo são permitidas na categoria padrão; categorias premium "
    "exigem justificativa.",
    ("h", "7. Avaliação de desempenho e carreira"),
    "O ciclo de avaliação é semestral (março e setembro) e combina autoavaliação, avaliação do gestor e "
    "feedback de dois pares. Promoções e méritos são discutidos no comitê de calibração de setembro e "
    "aplicados na folha de outubro. Cada colaborador tem um PDI (Plano de Desenvolvimento Individual) "
    "revisado a cada ciclo.",
    ("h", "8. Canais de contato"),
    "Dúvidas sobre folha e benefícios: rh@brisa.example ou ramal 2200. Suporte de TI: chamado no portal "
    "BrisaDesk ou ramal 2300. Canal de ética e denúncias (anônimo): etica.brisa.example, disponível 24 horas.",
])

# ---------------------------------------------------------------------------
# 2. Manual do produto
# ---------------------------------------------------------------------------
build("manual_purificador_brisa_air_pro.pdf", "Manual do Usuário — Purificador Brisa Air Pro", [
    ("h", "1. Especificações técnicas"),
    ("t", [
        ["Item", "Especificação"],
        ["Modelo", "BAP-300"],
        ["Área de cobertura", "Até 45 m²"],
        ["CADR (taxa de ar limpo)", "300 m³/h"],
        ["Filtros", "Pré-filtro lavável + HEPA H13 + carvão ativado"],
        ["Potência", "38 W (máx.) / 2 W (standby)"],
        ["Tensão", "Bivolt automático 100–240 V"],
        ["Ruído", "22 dB (modo noturno) a 52 dB (turbo)"],
        ["Conectividade", "Wi-Fi 2,4 GHz, app Brisa Home"],
        ["Peso", "5,2 kg"],
    ]),
    ("h", "2. Instalação"),
    "Retire o purificador da embalagem e remova o plástico protetor do filtro HEPA antes de ligar — "
    "o aparelho não funciona corretamente com o plástico. Posicione o equipamento a pelo menos 30 cm de "
    "paredes e móveis, em local plano, longe de umidificadores e de fontes de calor. Conecte o cabo na "
    "tomada; o anel de luz acenderá em branco indicando que o aparelho está pronto.",
    ("h", "3. Conectando ao aplicativo Brisa Home"),
    "1) Baixe o app Brisa Home na loja do seu celular e crie uma conta. 2) Mantenha pressionado o botão "
    "Wi-Fi por 5 segundos até o anel piscar em azul. 3) No app, toque em \"Adicionar dispositivo\" e "
    "selecione Brisa Air Pro. 4) Informe a rede Wi-Fi de 2,4 GHz — redes de 5 GHz não são suportadas. "
    "A conexão leva até 2 minutos. Se falhar, aproxime o roteador e repita o processo.",
    ("h", "4. Modos de operação"),
    "Automático: ajusta a velocidade conforme a qualidade do ar medida pelo sensor de partículas PM2.5. "
    "Noturno: velocidade mínima, luzes apagadas, 22 dB. Turbo: velocidade máxima por 30 minutos, depois "
    "volta ao modo anterior. Manual: 4 velocidades fixas. A cor do anel indica a qualidade do ar: azul "
    "(boa, PM2.5 até 12 µg/m³), verde (moderada, 13–35), amarelo (ruim, 36–55) e vermelho (muito ruim, "
    "acima de 55).",
    "PAGE",
    ("h", "5. Manutenção e troca de filtros"),
    "O pré-filtro deve ser limpo a cada 2 semanas com aspirador ou água corrente; deixe secar "
    "completamente antes de recolocar. O filtro HEPA H13 com carvão ativado (refil BAP-F1) deve ser "
    "trocado a cada 6 a 8 meses, dependendo do uso — o aparelho avisa com o ícone de filtro aceso em "
    "laranja. O filtro HEPA NÃO pode ser lavado. Após a troca, mantenha o botão de filtro pressionado "
    "por 3 segundos para zerar o contador. O refil BAP-F1 custa R$ 189,90 na loja oficial.",
    ("h", "6. Códigos de erro"),
    ("t", [
        ["Código", "Significado", "O que fazer"],
        ["E1", "Filtro ausente ou mal encaixado", "Reposicione o filtro e feche bem a tampa traseira"],
        ["E2", "Falha no sensor de partículas", "Limpe a entrada do sensor com cotonete seco; se persistir, acione a assistência"],
        ["E3", "Motor travado ou superaquecido", "Desligue da tomada por 30 minutos; verifique obstruções"],
        ["E4", "Falha de comunicação Wi-Fi", "Reinicie o roteador e refaça o pareamento (seção 3)"],
        ["E5", "Filtro vencido há mais de 30 dias", "Troque o filtro HEPA e zere o contador"],
    ]),
    ("h", "7. Garantia"),
    "A garantia legal é de 90 dias, acrescida de garantia contratual de 21 meses, totalizando 2 anos a "
    "partir da data da nota fiscal. Registrando o produto no app Brisa Home em até 30 dias após a compra, "
    "a garantia é estendida para 3 anos. A garantia não cobre filtros (itens de consumo), danos por queda, "
    "uso em ambientes externos ou reparos feitos por terceiros não autorizados. Para acionar a garantia, "
    "abra um chamado em suporte.brisa.example ou ligue 0800 000 2026 (segunda a sábado, 8h às 20h).",
    ("h", "8. Segurança"),
    "Não use o aparelho em banheiros ou locais com umidade acima de 85%. Não cubra a saída de ar. Não "
    "utilize aromatizantes ou óleos essenciais no aparelho, pois danificam o filtro de carvão. Mantenha "
    "fora do alcance de crianças pequenas e animais que possam morder o cabo.",
])

# ---------------------------------------------------------------------------
# 3. Política de segurança da informação (curta)
# ---------------------------------------------------------------------------
build("politica_seguranca_informacao.pdf", "Política de Segurança da Informação", [
    ("h", "1. Senhas e autenticação"),
    "Senhas devem ter no mínimo 12 caracteres e são trocadas apenas quando houver suspeita de "
    "vazamento (não há troca periódica obrigatória). A autenticação em dois fatores (2FA) pelo app "
    "Authenticator é obrigatória para e-mail, VPN e sistemas financeiros. É proibido compartilhar senhas, "
    "inclusive com colegas e gestores; use o cofre de senhas corporativo para credenciais de equipe.",
    ("h", "2. Dispositivos"),
    "Notebooks corporativos têm disco criptografado e bloqueio de tela automático após 5 minutos. "
    "O uso de pen drives está bloqueado; para transferir arquivos use o Drive corporativo. Celulares "
    "pessoais podem acessar e-mail corporativo somente com o app de gerenciamento (MDM) instalado.",
    ("h", "3. Classificação de informações"),
    "Pública: pode ser divulgada (site, materiais de marketing). Interna: uso dos colaboradores (este "
    "manual, comunicados). Confidencial: dados de clientes, financeiros e projetos em desenvolvimento — "
    "só podem ser compartilhados com quem precisa saber. Restrita: dados pessoais sensíveis e segredos "
    "industriais — acesso registrado e aprovado pela diretoria.",
    ("h", "4. Incidentes"),
    "Qualquer suspeita de incidente (e-mail de phishing, perda de equipamento, acesso indevido) deve ser "
    "comunicada em até 1 hora para seguranca@brisa.example ou pelo ramal 2399. Em caso de perda ou roubo "
    "de notebook, também é necessário registrar boletim de ocorrência em até 48 horas.",
])
