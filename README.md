# Crop Rotation Planner

A Python tool that generates **optimal seasonal crop rotation plans** for horticultural farms, based on agronomic principles and supported by peer-reviewed scientific literature.

## Features

- **4-year rotation plan** across 4 parcels (A, B, C, D)
- **24 crops** from 9 botanical families
- **Seasonal optimization**: each crop is placed in its optimal growing season
- **Pathogen cycle management**: rotation gaps respect the survival time of major soil-borne pathogens
- **Soil health balance**: alternation of depletive / neutral / soil-improving crops
- **Spatial rotation**: crops shift across parcels each year to break pathogen cycles
- **Automatic validation**: the tool checks that no agronomic rule is violated

## Quick Start

```bash
python crop_rotation_planner.py
```

## Sample Output

```
====================================================================================
   CROP ROTATION PLANNER - Piano di Rotazione Stagionale Ottimale
   Azienda orticola tipo | 4 parcelle | 4 anni | Clima temperato
====================================================================================

------------------------------------------------------------------------------------
  ANNO 1
------------------------------------------------------------------------------------
  Stagione    | Parc.A            | Parc.B            | Parc.C            | Parc.D            |
  ------------|-------------------|-------------------|-------------------|-------------------|
  Primavera   | Patata [!]        | Fagiolo [+]       | Ravanello [o]     | Pisello [+]       |
  Estate      | Pomodoro [!]      | Zucchina [!]      | Melone [!]        | Peperone [!]      |
  Autunno     | Cipolla [!]       | Cavolo [!]        | Carota [o]        | Lattuga [o]       |
  Inverno     | Aglio [!]         | Cavolfiore [!]    | Cicoria [o]       | Orzo (cover) [+]  |
```

### Effect on Soil
| Icon | Effect | Description |
|------|--------|-------------|
| `[!]` | Depletive | Consumes nutrients, accumulates pathogens (Solanaceae, Cucurbitaceae, Brassicaceae) |
| `[o]` | Neutral | Moderate impact (Asteraceae, Apiaceae, Amaranthaceae) |
| `[+]` | Soil-improving | Enriches soil, fixes N₂ (Fabaceae, Poaceae cover crops) |

## Agronomic Principles

1. **Family rotation**: Never plant the same botanical family on the same parcel for ≥2 consecutive seasons
2. **Depletive → Improving succession**: After Solanaceae/Cucurbitaceae, insert Fabaceae or Poaceae (N-fixing / cover crops)
3. **Brassicaceae in Autumn/Winter**: natural biofumigation via glucosinolate release
4. **Biological N fixation**: Fabaceae (beans, fava, peas) enrich soil nitrogen
5. **Cover crops**: Barley/Oat protect soil and reduce pathogen banks during fallow periods
6. **Pathogen cycle management**: rotation ≥3-4 years for persistent pathogens (Fusarium, Verticillium)
7. **Spatial rotation**: crops shift across parcels each year

## Managed Soil-Borne Pathogens

| Pathogen | Survival in soil |
|----------|-----------------|
| *Fusarium oxysporum* | 3-5 years |
| *Verticillium dahliae* (microsclerotia) | 4-7 years |
| *Ralstonia solanacearum* (bacterium) | 3-5 years |
| *Plasmodiophora brassicae* (clubroot) | 4-10 years |
| *Sclerotium cepivorum* (onion/garlic) | 4-8 years |
| *Rhizoctonia solani* | 3-4 years |

## Scientific References (PubMed)

The rotation principles implemented in this tool are grounded in the following peer-reviewed studies:

1. **Wu, Liu, Yu, Fan, He, Zhu, Dong, Yang, Zhu** (2025). *An altruistic rhizo-microbiome strategy in crop-rotation systems for sustainable management of soil-borne diseases.* **Plant Communications**. PMID: [40903899](https://pubmed.ncbi.nlm.nih.gov/40903899/)

2. **Khan, Ullah, Maqbool, Khan, Khan, Khalid, Arshad, Paker, Naz, Akmal, Munis, Chaudhary** (2025). *Unravelling the Mechanistic Role of Soil Microbial Interactions in the Suppression of Phytopathogens in Vegetable Agroecosystems of Pakistan.* **Current Microbiology**. PMID: [41369731](https://pubmed.ncbi.nlm.nih.gov/41369731/)

3. **Zhang, Li, Lu, Xu, Pan** (2022). *Three Preceding Crops Increased the Yield of and Inhibited Clubroot Disease in Continuously Monocropped Chinese Cabbage by Regulating the Soil Properties and Rhizosphere Microbial Community.* **Microorganisms**. PMID: [35456849](https://pubmed.ncbi.nlm.nih.gov/35456849/)

4. **Tan, Liu, Peng, Yin, Meng, Tao, Gu, Li, Yang, Xiao, Liu, Xiang, Zhou** (2021). *Soil potentials to resist continuous cropping obstacle: Three field cases.* **Environmental Research**. PMID: [34052246](https://pubmed.ncbi.nlm.nih.gov/34052246/)

5. **Zang, Guo, Li, Chen, Ma** (2025). *Using Russian dandelion allelochemicals to elevate disease resistance and improve sugar beet growth.* **Ecotoxicology and Environmental Safety**. PMID: [40885112](https://pubmed.ncbi.nlm.nih.gov/40885112/)

6. **Sahoo, Kadoo** (2025). *Integrative multi-omics and computer-aided biofungicide design approach to combat fusarium wilt of chickpea.* **Planta**. PMID: [41003817](https://pubmed.ncbi.nlm.nih.gov/41003817/)

7. **Zhang, Tang, Guo, Yang, Wang, Wei, Su, He, Li, Ouyang, Zhou** (2022). *Correlation analysis between continuous cropping obstacle of Gastrodia elata and Ilyonectria fungi and relieving strategy.* **China Journal of Chinese Materia Medica**. PMID: [35531675](https://pubmed.ncbi.nlm.nih.gov/35531675/)

8. **Ma, Gao, Li, Wang, Li, Hu, Huang, Lin, Tang, Liu** (2023). *Identification and characterization of biocontrol agent Lysinibacillus boronitolerans P42 against Cerrena unicolor that causes root rot of arecanut palm.* **Archives of Microbiology**. PMID: [37004578](https://pubmed.ncbi.nlm.nih.gov/37004578/)

## Botanical Families in Rotation

| Family | Crops | Soil Effect |
|--------|-------|-------------|
| Solanaceae | Tomato, Pepper, Eggplant, Potato | Depletive |
| Brassicaceae | Cabbage, Cauliflower, Turnip, Radish | Depletive / Neutral |
| Cucurbitaceae | Zucchini, Cucumber, Melon | Depletive |
| Fabaceae | Bean, Fava, Pea | Soil-improving (N₂ fixation) |
| Amaryllidaceae | Onion, Garlic | Depletive |
| Asteraceae | Lettuce, Chicory | Neutral |
| Apiaceae | Carrot, Parsley | Neutral |
| Amaranthaceae | Swiss Chard, Spinach | Neutral |
| Poaceae | Barley, Oat (cover crop) | Soil-improving |

## License

MIT License
