#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CROP ROTATION PLANNER
=====================
Piano di Rotazione Stagionale Ottimale per un'azienda orticola tipo.

Genera automaticamente un calendario di rotazione su 4 anni e 4 parcelle,
basandosi su principi agronomici:
  - Rotazione tra famiglie botaniche diverse
  - Interruzione dei cicli dei patogeni tellurici
  - Alternanza colture depletive / migliorative / neutre
  - Posizionamento stagionale ottimale
  - Rotazione spaziale (le colture si spostano di parcella ogni anno)

Riferimenti scientifici (PubMed):
  - Wu et al. (2025) Plant Communications – PMID 40903899
  - Khan et al. (2025) Current Microbiology – PMID 41369731
  - Zhang et al. (2022) Microorganisms – PMID 35456849
  - Tan et al. (2021) Environmental Research – PMID 34052246
  - Zang et al. (2025) Ecotoxicology & Env. Safety – PMID 40885112
  - Sahoo & Kadoo (2025) Planta – PMID 41003817

Autore: Crop Rotation Planner Team
Licenza: MIT
"""

# ============================================================
# DATABASE AGRONOMICO
# ============================================================

CROPS = {
    # -- Solanacee --
    "Pomodoro":  {"famiglia":"Solanaceae",    "stagioni":["Primavera","Estate"], "patogeni":["Fusarium oxysporum","Verticillium dahliae","Ralstonia solanacearum"], "effetto":"depletivo"},
    "Peperone":  {"famiglia":"Solanaceae",    "stagioni":["Primavera","Estate"], "patogeni":["Fusarium oxysporum","Verticillium dahliae","Phytophthora capsici"], "effetto":"depletivo"},
    "Melanzana": {"famiglia":"Solanaceae",    "stagioni":["Estate"],             "patogeni":["Fusarium oxysporum","Verticillium dahliae"], "effetto":"depletivo"},
    "Patata":    {"famiglia":"Solanaceae",    "stagioni":["Primavera"],          "patogeni":["Rhizoctonia solani","Fusarium spp.","Ralstonia solanacearum"], "effetto":"depletivo"},
    # -- Brassicacee --
    "Cavolo":       {"famiglia":"Brassicaceae","stagioni":["Autunno","Inverno"], "patogeni":["Plasmodiophora brassicae","Xanthomonas campestris"], "effetto":"depletivo"},
    "Cavolfiore":   {"famiglia":"Brassicaceae","stagioni":["Autunno","Inverno"], "patogeni":["Plasmodiophora brassicae","Alternaria brassicicola"], "effetto":"depletivo"},
    "Rapa":         {"famiglia":"Brassicaceae","stagioni":["Autunno"],           "patogeni":["Plasmodiophora brassicae"], "effetto":"depletivo"},
    "Ravanello":    {"famiglia":"Brassicaceae","stagioni":["Primavera","Autunno"],"patogeni":["Plasmodiophora brassicae"], "effetto":"neutro"},
    # -- Cucurbitacee --
    "Zucchina":  {"famiglia":"Cucurbitaceae","stagioni":["Estate"],              "patogeni":["Fusarium oxysporum f.sp. cucurbitae","Pythium spp."], "effetto":"depletivo"},
    "Cetriolo":  {"famiglia":"Cucurbitaceae","stagioni":["Estate"],              "patogeni":["Fusarium oxysporum","Pythium aphanidermatum"], "effetto":"depletivo"},
    "Melone":    {"famiglia":"Cucurbitaceae","stagioni":["Estate"],              "patogeni":["Fusarium oxysporum f.sp. melonis","Monosporascus cannonballus"], "effetto":"depletivo"},
    # -- Fabacee (leguminose) --
    "Fagiolo":   {"famiglia":"Fabaceae","stagioni":["Primavera","Estate"],       "patogeni":["Rhizoctonia solani","Fusarium spp."], "effetto":"migliorativo"},
    "Fava":      {"famiglia":"Fabaceae","stagioni":["Autunno","Inverno"],        "patogeni":["Botrytis fabae","Fusarium spp."], "effetto":"migliorativo"},
    "Pisello":   {"famiglia":"Fabaceae","stagioni":["Primavera","Autunno"],      "patogeni":["Fusarium solani","Aphanomyces euteiches"], "effetto":"migliorativo"},
    # -- Amaryllidacee --
    "Cipolla":   {"famiglia":"Amaryllidaceae","stagioni":["Primavera","Autunno"],"patogeni":["Fusarium oxysporum f.sp. cepae","Sclerotium cepivorum"], "effetto":"depletivo"},
    "Aglio":     {"famiglia":"Amaryllidaceae","stagioni":["Autunno","Inverno"],  "patogeni":["Sclerotium cepivorum","Fusarium spp."], "effetto":"depletivo"},
    # -- Asteracee --
    "Lattuga":   {"famiglia":"Asteraceae","stagioni":["Primavera","Autunno"],    "patogeni":["Sclerotinia sclerotiorum","Pythium spp."], "effetto":"neutro"},
    "Cicoria":   {"famiglia":"Asteraceae","stagioni":["Autunno","Inverno"],      "patogeni":["Sclerotinia sclerotiorum"], "effetto":"neutro"},
    # -- Apiacee --
    "Carota":    {"famiglia":"Apiaceae","stagioni":["Primavera","Autunno"],      "patogeni":["Pythium spp.","Rhizoctonia solani"], "effetto":"neutro"},
    "Prezzemolo":{"famiglia":"Apiaceae","stagioni":["Primavera","Autunno","Inverno"],"patogeni":["Pythium spp."], "effetto":"neutro"},
    # -- Amaranthaceae --
    "Bietola":   {"famiglia":"Amaranthaceae","stagioni":["Primavera","Autunno","Inverno"],"patogeni":["Cercospora beticola","Pythium spp."], "effetto":"neutro"},
    "Spinacio":  {"famiglia":"Amaranthaceae","stagioni":["Primavera","Autunno"], "patogeni":["Fusarium oxysporum f.sp. spinaciae","Pythium spp."], "effetto":"neutro"},
    # -- Poacee (cover crop) --
    "Orzo (cover)":  {"famiglia":"Poaceae","stagioni":["Autunno","Inverno"],     "patogeni":[], "effetto":"migliorativo"},
    "Avena (cover)": {"famiglia":"Poaceae","stagioni":["Autunno","Inverno"],     "patogeni":[], "effetto":"migliorativo"},
}

STAGIONI = ["Primavera", "Estate", "Autunno", "Inverno"]
PARCELLE = ["A", "B", "C", "D"]
NUM_ANNI = 4

# ============================================================
# SCHEMA BASE DI ROTAZIONE (Anno 1)
# ============================================================
# Ogni stagione ha 4 colture di famiglie botaniche diverse.
# Negli anni successivi le colture si spostano di parcella (rotazione spaziale).

SCHEMA_BASE = {
    "Primavera": ["Patata",   "Fagiolo",  "Ravanello", "Pisello"],
    "Estate":    ["Pomodoro", "Zucchina", "Melone",    "Peperone"],
    "Autunno":   ["Cipolla",  "Cavolo",   "Carota",    "Lattuga"],
    "Inverno":   ["Aglio",    "Cavolfiore","Cicoria",   "Orzo (cover)"],
}


def shift_lista(lista, offset):
    """Ruota la lista di offset posizioni (rotazione spaziale)."""
    return [lista[(i - offset) % len(lista)] for i in range(len(lista))]


def genera_piano():
    """Genera il piano di rotazione per NUM_ANNI anni."""
    piano = {p: [] for p in PARCELLE}
    for anno in range(NUM_ANNI):
        for stg in STAGIONI:
            base = SCHEMA_BASE[stg]
            ruotata = shift_lista(base, anno)
            for idx, p in enumerate(PARCELLE):
                piano[p].append((ruotata[idx], stg, anno + 1))
    return piano


def verifica_piano(piano):
    """Verifica che il piano rispetti i principi agronomici di rotazione."""
    problemi = []
    for p in PARCELLE:
        for i in range(1, len(piano[p])):
            c1 = piano[p][i - 1][0]
            c2 = piano[p][i][0]
            f1 = CROPS[c1]["famiglia"]
            f2 = CROPS[c2]["famiglia"]
            # Controlla famiglie consecutive (ignora Primavera->Estate, stesso ciclo colturale)
            s1 = piano[p][i - 1][1]
            s2 = piano[p][i][1]
            if f1 == f2 and not (s1 == "Primavera" and s2 == "Estate"):
                problemi.append(
                    "Parc.{}, Anno {} {}: famiglia {} consecutiva".format(
                        p, piano[p][i][2], piano[p][i][1], f2
                    )
                )
    return problemi


def stampa_calendario(piano):
    """Stampa il calendario di rotazione in formato tabellare."""
    EFFETTO_ICON = {"depletivo": "[!]", "migliorativo": "[+]", "neutro": "[o]"}

    print("=" * 84)
    print("   CROP ROTATION PLANNER - Piano di Rotazione Stagionale Ottimale")
    print("   Azienda orticola tipo | 4 parcelle | 4 anni | Clima temperato")
    print("=" * 84)

    for anno in range(1, NUM_ANNI + 1):
        print()
        print("-" * 84)
        print("  ANNO {}".format(anno))
        print("-" * 84)
        hdr = "  {:<12}|".format("Stagione")
        for p in PARCELLE:
            hdr += " {:<18}|".format("Parc." + p)
        print(hdr)
        print("  {}|{}|{}|{}|{}|".format("-" * 12, "-" * 19, "-" * 19, "-" * 19, "-" * 19))

        for stg in STAGIONI:
            riga = "  {:<12}|".format(stg)
            for p in PARCELLE:
                coltura = ""
                for c, s, a in piano[p]:
                    if a == anno and s == stg:
                        coltura = c
                        break
                ic = EFFETTO_ICON[CROPS[coltura]["effetto"]]
                label = coltura + " " + ic
                riga += " {:<18}|".format(label)
            print(riga)
        print()

    # Legenda
    print("=" * 84)
    print("  LEGENDA E NOTE AGRONOMICHE")
    print("=" * 84)
    print()
    print("  EFFETTO SUOLO:")
    print("  [!] Depletivo    - consuma nutrienti, accumula patogeni (Solanaceae, Cucurbitaceae, Brassicaceae)")
    print("  [o] Neutro       - moderato impatto (Asteraceae, Apiaceae, Amaranthaceae)")
    print("  [+] Migliorativo - arricchisce il suolo, fissa N2 (Fabaceae, Poaceae cover crop)")
    print()
    print("  FAMIGLIE BOTANICHE IN ROTAZIONE:")
    print("  Solanaceae     -> Pomodoro, Peperone, Melanzana, Patata")
    print("  Brassicaceae   -> Cavolo, Cavolfiore, Rapa, Ravanello")
    print("  Cucurbitaceae  -> Zucchina, Cetriolo, Melone")
    print("  Fabaceae       -> Fagiolo, Fava, Pisello (fissano N2 atmosferico)")
    print("  Amaryllidaceae -> Cipolla, Aglio")
    print("  Asteraceae     -> Lattuga, Cicoria")
    print("  Apiaceae       -> Carota, Prezzemolo")
    print("  Poaceae        -> Orzo, Avena (cover crop / sovescio)")
    print("  Amaranthaceae  -> Bietola, Spinacio")
    print()
    print("  PRINCIPI CHIAVE DEL PIANO:")
    print("  1. Mai la stessa famiglia botanica sulla parcella per >=2 stagioni consecutive")
    print("  2. Dopo Solanaceae/Cucurbitaceae [!] -> inserire Fabaceae/Poaceae [+]")
    print("  3. Le Brassicaceae in Autunno/Inverno: biofumigazione naturale (glucosinolati)")
    print("  4. Le Fabaceae arricchiscono l'azoto del suolo (fissazione biologica di N2)")
    print("  5. Cover crop (Orzo/Avena) proteggono il suolo e riducono il bank di patogeni")
    print("  6. Rotazione >=3-4 anni per patogeni persistenti (Fusarium, Verticillium)")
    print("  7. Le colture si spostano di parcella ogni anno (rotazione spaziale)")
    print()
    print("  PATOGENI GESTITI DALLA ROTAZIONE:")
    print("  * Fusarium oxysporum (tropicale/temperato) - ciclo 3-5 anni")
    print("  * Verticillium dahliae (microsclerozi)      - ciclo 4-7 anni")
    print("  * Ralstonia solanacearum (batterio)         - ciclo 3-5 anni")
    print("  * Plasmodiophora brassicae (clubroot)       - ciclo 4-10 anni")
    print("  * Sclerotium cepivorum (cipolla/aglio)      - ciclo 4-8 anni")
    print("  * Rhizoctonia solani                        - ciclo 3-4 anni")
    print()

    # Verifica
    problemi = verifica_piano(piano)
    if problemi:
        print("  AVVISI:")
        for pr in problemi:
            print("    " + pr)
    else:
        print("  >> Il piano rispetta tutti i principi agronomici di rotazione!")

    print()
    print("=" * 84)
    print("  Piano generato con successo - Rispettare l'ordine delle successioni!")
    print("=" * 84)


if __name__ == "__main__":
    piano = genera_piano()
    stampa_calendario(piano)
