import regex as re

pos_map = {'N': 'N-', 'V': 'V-', 'J': 'A-', 'D': 'RA', 'B': 'D-',
           'C': 'C-', 'T': 'X-', 'I': 'I-', 'P': 'P-'}

def get_degree_map():
    degree_map = {'O': '-', 'C': 'C', 'S': 'S'}
    return degree_map

def get_case_map():
    case_map = {'G': 'G', 'N': 'N', 'A': 'A', 'D': 'D', 'V': 'V'}
    return case_map

def get_tense_map():
    # this is icky, but I can only really map Past to Aorist.
    tense_map = {'A': 'A', 'P': 'P', 'F': 'F', 'L': 'Y', 'R': 'X', 'I': 'I'}
    return tense_map


def get_mood_map():
    mood_map = {'I': 'I', 'S': 'S', 'M': 'D', 'O': 'O', 'N': 'N', 'P': 'P'}
    return mood_map


def get_number_map():
    number_map = {'S': 'S', 'P': 'P'}
    return number_map


def get_voice_map():
    # where 'U' == middle/passive
    voice_map = {'A': 'A', 'M': 'M', 'P': 'P', 'U': 'U'}
    return voice_map


def get_gender_map():
    gender_map = {'M': 'M', 'F': 'F', 'N': 'N'}
    return gender_map


def get_pron_type_map():
    pron_type_map = {'P': 'P', 'R': 'R', 'I': 'I', 'D': 'D'}
    return pron_type_map

# greek
tense_map = get_tense_map()
mood_map = get_mood_map()
number_map = get_number_map()
voice_map = get_voice_map()
case_map = get_case_map()
gender_map = get_gender_map()
pron_type_map = get_pron_type_map()
degree_map = get_degree_map()


def format_return_codes(return_codes):
    codes = []
    for key in return_codes:
        codes.append(return_codes[key])
    return "".join(codes)


def map_case_number_gender(morph, return_codes):
    if morph[1] in case_map:
        return_codes["case"] = case_map[morph[1]]
    else:
        print(f"Unknown case: {morph[1]} from {morph}")
    if morph[2] in number_map:
        return_codes["number"] = number_map[morph[2]]
    else:
        print(f"Unknown number: {morph[2]} from {morph}")
    if morph[3] in gender_map:
        return_codes["gender"] = gender_map[morph[3]]
    else:
        print(f"Unknown gender: {morph[3]} from {morph}")

    return format_return_codes(return_codes)


def get_pos(morph_text):
    if morph_text[0] in pos_map:
        return pos_map[morph_text[0]]
    elif morph_text[:2] == "RP":
        return "RP"
    elif morph_text[:2] == "RD":
        return "RD"
    elif morph_text[:2] == "RR":
        return "RR"
    elif morph_text[:2] == "RI":
        return "RI"
    elif morph_text[:2] == "RX":
        return "RI"
    elif re.match(r"R[SCKF]", morph_text):
        return morph_text[:2] # Tauber isn't this specific
    elif morph_text == "XP":
        return "NP"
    elif morph_text == "XN":
        return "NU"
    elif morph_text == "XF":
        return "TL"
    else:
        print(f"Unknown POS: {morph_text[0]} from {morph_text}")
        return morph_text[0]


def map_logos_morph(morph):
    logos_pos = morph[0]
    return_codes = {"person": "-", "tense": "-", "voice": "-", "mood": "-", "case": "-", "number": "-",
                    "gender": "-", "degree": "-"}

    one_codes = ['P', 'C', 'B', 'T', 'I', 'X']

    if logos_pos in one_codes:
        return format_return_codes(return_codes)
    elif len(morph) == 1:
        return format_return_codes(return_codes)
    elif logos_pos == "N":
        return map_case_number_gender(morph, return_codes)
    elif logos_pos == "J":
        if len(morph) == 4:
            return map_case_number_gender(morph, return_codes)
    elif logos_pos == "D":
        return map_case_number_gender(morph, return_codes)
    elif logos_pos == "R":
        return_codes["person"] = morph[2]
        return_codes["case"] = case_map[morph[3]]
        return_codes["number"] = number_map[morph[4]]
        if len(morph) == 6:
            return_codes["gender"] = gender_map[morph[5]]
        return format_return_codes(return_codes)
    elif logos_pos == "V":
        return_codes["tense"] = tense_map[morph[1]]
        return_codes["voice"] = voice_map[morph[2]]
        return_codes["mood"] = mood_map[morph[3]]
        if return_codes["mood"] == "N": # infinitive
            return format_return_codes(return_codes)
        elif return_codes["mood"] == "P": # participle
            # return_codes["person"] == morph[4]
            return_codes["case"] = case_map[morph[6]]
            return_codes["number"] = number_map[morph[5]]
            return_codes["gender"] = gender_map[morph[7]]
            return format_return_codes(return_codes)
        else:
            return_codes["person"] = morph[4]
            return_codes["number"] = number_map[morph[5]]
            return format_return_codes(return_codes)
    else:
        print(f"Unknown POS: {logos_pos} from {morph}")
        return format_return_codes(return_codes)

