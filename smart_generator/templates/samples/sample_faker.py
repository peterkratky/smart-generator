from faker import Faker

from smart_generator.templates.template_table import TemplateTable
from smart_generator.templates.templates_provider_faker import \
    TemplatesProviderFromFaker

provider = TemplatesProviderFromFaker()
provider.locales = [
    "az_AZ",
    "bn_BD",
    "cs_CZ",
    "da_DK",
    "de",
    "de_AT",
    "de_CH",
    "de_DE",
    "el_GR",
    "en",
    "en_AU",
    "en_BD",
    "en_CA",
    "en_GB",
    "en_IE",
    "en_IN",
    "en_NZ",
    "en_PH",
    "en_US",
    "es",
    "es_AR",
    "es_CL",
    "es_CO",
    "es_ES",
    "es_MX",
    "fa_IR",
    "fil_PH",
    "fi_FI",
    "fr_CA",
    "fr_CH",
    "fr_FR",
    "he_IL",
    "hi_IN",
    "hr_HR",
    "hu_HU",
    "hy_AM",
    "id_ID",
    "it_IT",
    "ja_JP",
    "ka_GE",
    "ko_KR",
    "ne_NP",
    "nl_BE",
    "nl_NL",
    "no_NO",
    "pl_PL",
    "pt_BR",
    "pt_PT",
    "ro_RO",
    "ru_RU",
    "sk_SK",
    "sl_SI",
    "sv_SE",
    "ta_IN",
    "th",
    "th_TH",
    "tl_PH",
    "uk_UA",
    "zh_CN",
    "zh_TW",
]
provider.add_table(TemplateTable("locale", "locale", dependency_templates=["locale"]))

fake = Faker()
for faker_method in dir(fake):
    if not faker_method.startswith("_"):
        provider.add_table(
            TemplateTable(faker_method, faker_method, dependency_templates=["locale"])
        )
