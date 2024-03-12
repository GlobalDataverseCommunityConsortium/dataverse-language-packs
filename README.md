# dataverse-language-packs
Repository for language files associated with [Dataverse](https://github.com/IQSS/dataverse)

Some language packages are only available for older versions, to get the latest version view the published branches (please see notes below).

API Documentation for deploying language files is still under development.

Please Note: These transalations are provided as is. If you see any problems, please open an issue and/or contact the organization listed below as the maintainer of the translation.

Available languages:
- [English (US), latest develop branch](https://github.com/GlobalDataverseCommunityConsortium/dataverse-language-packs/tree/develop/en_US) maintained by [IQSS Harvard](https://github.com/IQSS/dataverse/tree/develop/src/main/java/propertyFiles)
- [French (Canada), latest develop branch](https://github.com/GlobalDataverseCommunityConsortium/dataverse-language-packs/tree/develop/fr_CA) maintained currently by [Institut national de la recherche scientifique INRS](https://inrs.ca/) and previously by [Bibliothèques Université de Montréal](https://bib.umontreal.ca/)
- [French (France), 4.20](https://github.com/GlobalDataverseCommunityConsortium/dataverse-language-packs/tree/develop/fr_FR) maintained by [Sciences Po](https://www.sciencespo.fr/en/)
- [German (Austria), 4.9.4](https://github.com/GlobalDataverseCommunityConsortium/dataverse-language-packs/tree/develop/de-AT/) maintained by [AUSSDA](http://aussda.at)
- [Slovenian, 4.9.4](https://github.com/GlobalDataverseCommunityConsortium/dataverse-language-packs/tree/develop/sl-SI/) maintained by [ADP, Social Science Data Archive](https://www.adp.fdv.uni-lj.si/eng/)
- [Swedish, 4.9.4](https://github.com/GlobalDataverseCommunityConsortium/dataverse-language-packs/tree/develop/se-SE/) maintained by [SND, Swedish National Data Service](https://snd.gu.se/en)
- [Ukrainian, 4.9.4](https://github.com/GlobalDataverseCommunityConsortium/dataverse-language-packs/tree/develop/ua-UA/Bundle_ua.properties) maintained by [The Center for Content Analysis](http://ukrcontent.com/en/)
- [Spanish, 4.11](https://github.com/GlobalDataverseCommunityConsortium/dataverse-language-packs/tree/develop/es_ES) maintained by [El Consorcio Madroño](http://consorciomadrono.es/en/)
- [Italian 4.9.4](https://github.com/GlobalDataverseCommunityConsortium/dataverse-language-packs/tree/develop/it-IT/) maintained by [Centro Interdipartimentale UniData](http://www.unidata.unimib.it)
- [Hungarian, 4.9.4](https://github.com/GlobalDataverseCommunityConsortium/dataverse-language-packs/tree/develop/hu-HU) maintained by [TARKI](http://tarki.hu)
- [Portuguese, 4.18.1](https://github.com/GlobalDataverseCommunityConsortium/dataverse-language-packs/tree/dataverse-v4.18.1/pt_PT) maintained by [University of Minho](https://www.uminho.pt/EN)
- [Portuguese, 4.19](https://github.com/RNP-dadosabertos/dataverse-language-packs) maintained by [Rede Nacional de Ensino e Pesquisa/Universidade Federal do Rio Grande do Sul](https://www.dadosdepesquisa.rnp.br/)
- [Portuguese (Portugal), 5.10](https://github.com/GlobalDataverseCommunityConsortium/dataverse-language-packs/tree/dataverse-v5.10/pt_PT) maintained by [Universidade de Aveiro](https://www.ua.pt/)
- [Portuguese (Portugal), 5.12](https://github.com/GlobalDataverseCommunityConsortium/dataverse-language-packs/tree/develop/pt_PT) maintained by [KEEP Solutions](https://www.keep.pt/)
- [Polish, 4.10](https://github.com/GlobalDataverseCommunityConsortium/dataverse-language-packs/tree/develop/pl_PL) maintained by [CEON](https://depot.ceon.pl)
- [Dutch 5.13](https://github.com/GlobalDataverseCommunityConsortium/dataverse-language-packs/tree/develop/nl_NL) maintained by [DANS-KNAW](https://www.dans.knaw.nl)
- [Catalan](https://github.com/GlobalDataverseCommunityConsortium/dataverse-language-packs/tree/develop/ca_CA) maintained by [CSUC](https://www.csuc.cat/ca)

## Generating tools

Bash script `generate.sh` helps to maintains up to date i18n files. It use en_US files to detect all files and keys from latest version et try to fill value for desired language from latest available version for this language.

Usage:

```bash
bash ./generate.sh fr_CA => generate fr_CA from most recent version
bash ./generate.sh fr_FR develop => generate fr_FR from develop branch
```

Process:

1. Create properties files by copying files from en_US, rename then with language code, and removing value inside.
2. Extract files from most recent version for this language (branch dataverse-vXXX) or from the specified branch
3. Fill values by searching them in extracted files, in the same filename or in all files
4. Print "not found" keys (new keys)