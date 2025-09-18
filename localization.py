#The idea would be that these localizations could be loaded for example from a json file. For now just a dict.

localizations_fin = {
    "new_course_header": "Uusi rata",
    "course_name_header": "Nimi:",
    "course_holes_header": "Väylien lukumäärä:",
    "course_difficulty_header": "Radan vaikeustaso:",
    "course_difficulty": "Vaikeustaso",
    "course_diff_default": "--Valitse vaikeusluokitus--",
    "course_diff_easy": "Helppo",
    "course_diff_mod": "Haastava",
    "course_diff_hard": "Vaikea",
    "course_type_header": "Radan tyyppi:",
    "course_type": "Tyyppi",
    "course_type_default": "--Valitse radan tyyppi--",
    "course_type_open": "Avoin",
    "course_type_mixed": "Vaihteleva",
    "course_type_woods": "Metsä",
    "next_button": "Seuraava",
    "str_no_courses_found": "VIRHE: ei ratoja tietokannassa. Luo rata luodaksesi kierroksen."
}

localizations = localizations_fin

def get_localization(key):
    s = str(key)
    if s in localizations:
        return localizations[s]
    else:
        print(f"Virhe: lokalisaatioavainta {s} ei löydy lokalisaatiotiedostosta.")